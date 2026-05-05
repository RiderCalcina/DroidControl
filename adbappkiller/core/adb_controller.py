import os
import subprocess
import logging
import time
import re
import signal
import adbutils

class ADBController:
    def __init__(self):
        self._adb_executable = None
        self._ensure_adb_server()

    def get_adb_executable(self):
        if self._adb_executable:
            return self._adb_executable
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Intentar en la carpeta bin/ del proyecto
        local_adb = os.path.join(base_dir, "bin", "adb.exe")
        if os.path.isfile(local_adb):
            self._adb_executable = local_adb
            return self._adb_executable
            
        return None

    def _ensure_adb_server(self):
        adb_path = self.get_adb_executable()
        if not adb_path:
            return
        
        try:
            subprocess.run(
                [adb_path, "start-server"],
                capture_output=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception:
            pass

    def run_adb(self, args, timeout=5):
        adb_path = self.get_adb_executable()
        if not adb_path:
            return -2, "", "ADB no encontrado"
        
        try:
            result = subprocess.run(
                [adb_path] + args,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)

    def connect_wireless(self, ip_port):
        return self.run_adb(["connect", ip_port])

    def disconnect_wireless(self, ip_port=None):
        args = ["disconnect"]
        if ip_port:
            args.append(ip_port)
        return self.run_adb(args)

    def get_connected_devices(self):
        try:
            devices = []
            for d in adbutils.adb.device_list():
                serial = d.serial
                status = d.info.get('state', 'unknown')
                is_wifi = ":" in serial and "." in serial
                devices.append({
                    "serial": serial,
                    "status": status,
                    "type": "WiFi" if is_wifi else "USB"
                })
            return devices
        except Exception:
            code, out, _ = self.run_adb(["devices"], timeout=5)
            if code != 0: return []
            devices = []
            for line in out.splitlines()[1:]:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        serial, status = parts[0], parts[1]
                        is_wifi = ":" in serial and "." in serial
                        devices.append({
                            "serial": serial,
                            "status": status,
                            "type": "WiFi" if is_wifi else "USB"
                        })
            return devices

    def get_device_info(self, serial=None):
        info = {
            "brand": "Desconocida",
            "model": "Desconocido",
            "android_version": "Desconocida",
            "android_sdk": 0,
            "screen": "1080x1920"
        }
        try:
            d = adbutils.adb.device(serial=serial) if serial else adbutils.adb.device()
            info["brand"] = d.prop.get("ro.product.brand") or d.prop.get("ro.product.manufacturer") or "Desconocida"
            info["model"] = d.prop.get("ro.product.model") or "Desconocido"
            info["android_version"] = d.prop.get("ro.build.version.release") or "Desconocida"
            try:
                info["android_sdk"] = int(d.prop.get("ro.build.version.sdk") or 0)
            except:
                info["android_sdk"] = 0
            
            screen_out = d.shell("wm size")
            match_screen = re.search(r"Override size: (\d+x\d+)", screen_out) or re.search(r"Physical size: (\d+x\d+)", screen_out)
            if match_screen:
                info["screen"] = match_screen.group(1)
        except Exception:
            pass
        return info

    def take_screenshot(self, serial, local_path):
        remote_path = "/data/local/tmp/screen.png"
        args_cap = ["-s", serial, "shell", "screencap", "-p", remote_path] if serial else ["shell", "screencap", "-p", remote_path]
        code, out, err = self.run_adb(args_cap, timeout=15)
        if code == 0:
            code_p, out_p, err_p = self.pull_file(serial, remote_path, local_path)
            self.run_adb(["-s", serial, "shell", "rm", remote_path] if serial else ["shell", "rm", remote_path])
            return code_p, out_p, err_p
        return code, out, err

    def pull_file(self, serial, remote, local):
        return self.run_adb(["-s", serial, "pull", remote, local] if serial else ["pull", remote, local], timeout=60)

    def start_mirroring(self, serial, window_title="DroidControl", x=None, y=None, max_size=1024):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scrcpy_path = os.path.join(base_dir, "bin", "scrcpy.exe")
        
        if not os.path.exists(scrcpy_path):
            return None

        args = [
            scrcpy_path,
            "--stay-awake",
            f"--max-size={max_size}",
            "--video-bit-rate=4M",
            f"--window-title={window_title}",
            "--audio-buffer=100",
            "--audio-codec=raw"
        ]

        if serial: args.extend(["-s", serial])
        if x is not None: args.append(f"--window-x={x}")
        if y is not None: args.append(f"--window-y={y}")

        env = os.environ.copy()
        adb_path = self.get_adb_executable()
        if adb_path: env["ADB"] = adb_path

        try:
            process = subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
                env=env
            )
            return process
        except Exception:
            return None

    def start_recording(self, serial, local_path, record_audio=True):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scrcpy_path = os.path.join(base_dir, "bin", "scrcpy.exe")
        
        if not os.path.exists(scrcpy_path):
            return None

        if not local_path.lower().endswith('.mkv'):
            local_path = os.path.splitext(local_path)[0] + ".mkv"

        # Obtener información del dispositivo para parches de compatibilidad
        info = self.get_device_info(serial)
        brand = info.get("brand", "").lower()

        args = [
            scrcpy_path,
            "--no-video-playback",
            "--no-window",
            "--record", local_path,
            "--stay-awake",
            "--video-codec=h264",
            "--audio-codec=aac",
            "--max-size=1280",
            "--video-bit-rate=4M",
            "--audio-bit-rate=128K"
        ]

        # PARCHE ESPECÍFICO PARA XIAOMI / REDMI / POCO (Audio Fix)
        if "xiaomi" in brand or "redmi" in brand or "poco" in brand:
            args.extend([
                "--audio-source=playback",
                "--audio-codec=raw",
                "--audio-buffer=100"
            ])

        if serial: args.extend(["-s", serial])
        if not record_audio: args.append("--no-audio")
            
        env = os.environ.copy()
        adb_path = self.get_adb_executable()
        if adb_path: env["ADB"] = adb_path

        try:
            process = subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
                env=env
            )
            return process
        except Exception:
            return None

    def stop_recording(self, process):
        if not process: return 0
        try:
            if process.poll() is None:
                os.kill(process.pid, signal.CTRL_C_EVENT)
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    process.wait(timeout=1)
        except Exception:
            try: process.terminate()
            except: pass
        return 0
