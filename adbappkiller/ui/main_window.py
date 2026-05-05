import customtkinter as ctk
import threading
import time
import os
import datetime
import webbrowser
from tkinter import messagebox, filedialog
from PIL import Image
from ..core.adb_controller import ADBController
from ..utils.history import HistoryManager

THEME = {
    "BG": "#050505",
    "CARD": "#1A1C1E",
    "TEXT_MAIN": "#FFFFFF",
    "TEXT_SEC": "#71717A",
    "ACCENT": "#00F0FF",
    "SUCCESS": "#32D74B",
    "DANGER": "#FF3B30",
    "DANGER_HOVER": "#CC2F26",
    "BORDER": "#2A2D31",
    "BORDER_LIGHT": "#3A3F44", # Para efecto 3D
    "BUTTON_SECONDARY": "#1A1C1E",
    "BUTTON_SECONDARY_HOVER": "#25282B",
}

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DroidControl")
        
        # Icono
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            
        self.geometry("480x145")
        self.resizable(False, False)
        self.configure(fg_color=THEME["BG"])
        ctk.set_appearance_mode("dark")
        
        self.adb = ADBController()
        self.history = HistoryManager()
        
        self.running = True
        self.active_serial = None
        self.recording_processes = {}
        self.mirror_processes = {}
        
        # Animación
        self.pulse_val = 0
        self.pulse_dir = 1
        
        self.setup_ui()
        self.load_wifi_settings()
        self.bind_shortcuts()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Threads
        threading.Thread(target=self.device_monitor, daemon=True).start()
        self.pulse_animation()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Configuración de fuentes
        font_style = ("Inter", 9)
        font_bold = ("Inter", 9, "bold")
        font_tiny = ("Inter", 8, "bold")
        try:
            from tkinter import font
            if "Inter" not in font.families():
                font_style = ("Segoe UI", 9)
                font_bold = ("Segoe UI", 9, "bold")
                font_tiny = ("Segoe UI", 8, "bold")
        except: pass

        # --- Bloque 1: USB ---
        self.header = ctk.CTkFrame(self, fg_color="#0A0A0B", height=40, corner_radius=0, border_width=0)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_propagate(False)

        ctk.CTkLabel(self.header, text="(USB)", font=font_tiny, text_color=THEME["ACCENT"]).pack(side="left", padx=(10, 0))

        self.device_combo = ctk.CTkOptionMenu(
            self.header, values=["SIN CONEXIÓN USB"], command=self.on_device_selected,
            width=160, height=26, font=font_style, fg_color=THEME["BUTTON_SECONDARY"],
            button_color=THEME["BUTTON_SECONDARY"], button_hover_color=THEME["BUTTON_SECONDARY_HOVER"], corner_radius=6
        )
        self.device_combo.pack(side="left", padx=10, pady=7)

        self.specs_label = ctk.CTkLabel(self.header, text="ESPERANDO DISPOSITIVO...", font=font_tiny, text_color=THEME["TEXT_SEC"])
        self.specs_label.pack(side="left", padx=5)

        self.btn_mirror = ctk.CTkButton(
            self.header, text="CONECTAR", width=80, height=26, font=font_bold,
            fg_color=THEME["CARD"], border_width=1, border_color=THEME["BORDER_LIGHT"],
            text_color=THEME["TEXT_MAIN"], command=self.launch_mirror
        )
        self.btn_mirror.pack(side="right", padx=10, pady=7)

        # Separador 1 (Discreto)
        ctk.CTkFrame(self, height=2, fg_color=THEME["BORDER"], border_width=0).grid(row=1, column=0, sticky="ew", padx=20, pady=(2, 5))

        # --- Bloque 2: WIFI ---
        self.wifi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.wifi_container.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(self.wifi_container, text="(WIFI)", font=font_tiny, text_color=THEME["ACCENT"]).pack(side="left", padx=(5, 10))

        ctk.CTkLabel(self.wifi_container, text="IP:", font=font_bold, text_color=THEME["TEXT_SEC"]).pack(side="left", padx=2)
        self.wifi_ip_entry = ctk.CTkEntry(self.wifi_container, placeholder_text="192.168.1.x", width=115, height=28, font=font_style, fg_color=THEME["CARD"], border_width=1, border_color=THEME["BORDER_LIGHT"])
        self.wifi_ip_entry.pack(side="left", padx=2)

        ctk.CTkLabel(self.wifi_container, text=":", font=font_bold, text_color=THEME["TEXT_SEC"]).pack(side="left")
        self.wifi_port_entry = ctk.CTkEntry(self.wifi_container, placeholder_text="5555", width=55, height=28, font=font_style, fg_color=THEME["CARD"], border_width=1, border_color=THEME["BORDER_LIGHT"])
        self.wifi_port_entry.pack(side="left", padx=2)

        self.btn_wifi_toggle = ctk.CTkButton(self.wifi_container, text="CONECTAR", width=95, height=28, font=font_bold, fg_color=THEME["CARD"], border_width=1, border_color=THEME["BORDER_LIGHT"], command=self.toggle_wifi)
        self.btn_wifi_toggle.pack(side="left", padx=12)

        self.indicator_dot = ctk.CTkLabel(self.wifi_container, text="● OFFLINE", font=font_bold, text_color="#333")
        self.indicator_dot.pack(side="left", padx=5, expand=True)

        # Separador 2 (Discreto)
        ctk.CTkFrame(self, height=2, fg_color=THEME["BORDER"], border_width=0).grid(row=3, column=0, sticky="ew", padx=20, pady=(5, 5))

        # --- Bloque 3: CONTROLES ---
        self.controls = ctk.CTkFrame(self, fg_color="transparent")
        self.controls.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 15))
        self.controls.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        btn_style = {"height": 32, "font": font_bold, "corner_radius": 6, "border_width": 1, "border_color": THEME["BORDER_LIGHT"], "fg_color": THEME["CARD"]}

        self.btn_save_path = ctk.CTkButton(self.controls, text="💾 GUARDAR", command=self.select_output_dir, **btn_style)
        self.btn_save_path.grid(row=0, column=0, padx=1)

        self.btn_folder = ctk.CTkButton(self.controls, text="📁 ABRIR", command=self.open_output_dir, **btn_style)
        self.btn_folder.grid(row=0, column=1, padx=1)

        self.btn_capture = ctk.CTkButton(self.controls, text="📸 CAPTURAR", command=self.capture_screen, **btn_style)
        self.btn_capture.grid(row=0, column=2, padx=1)

        self.btn_record = ctk.CTkButton(self.controls, text="🎥 GRABAR", command=self.toggle_recording, **btn_style)
        self.btn_record.grid(row=0, column=3, padx=1)

        self.btn_about = ctk.CTkButton(self.controls, text="ℹ️ INFO", command=lambda: webbrowser.open("https://qwertyaserty.com/"), **btn_style)
        self.btn_about.grid(row=0, column=4, padx=1)

        self.setup_tooltips()

    def setup_tooltips(self):
        from .tooltip import CTKTooltip # Asumiendo que lo creamos o lo integramos
        tips = {
            self.device_combo: "Seleccionar dispositivo USB",
            self.btn_mirror: "Conectar vía USB",
            self.wifi_ip_entry: "IP del dispositivo Android",
            self.wifi_port_entry: "Puerto del dispositivo Android",
            self.btn_wifi_toggle: "Conectar vía WiFi",
            self.btn_save_path: "Cambiar carpeta de guardado",
            self.btn_folder: "Abrir carpeta de guardado",
            self.btn_capture: "Tomar captura de pantalla",
            self.btn_record: "Iniciar/Detener grabación",
            self.btn_about: "Acerca del proyecto"
        }
        for widget, text in tips.items():
            CTKTooltip(widget, text)


    def on_device_selected(self, choice):
        if choice == "SIN CONEXIÓN USB":
            self.active_serial = None
            self.specs_label.configure(text="ESPERANDO DISPOSITIVO...")
            return
        
        self.active_serial = choice.split(" (")[0]
        self.update_device_info()

    def update_device_info(self):
        if not self.active_serial: return
        def task():
            info = self.adb.get_device_info(self.active_serial)
            text = f"{info['brand']} {info['model']} | ANDROID {info['android_version']}".upper()
            title = f"DroidControl - {info['model']}"
            self.after(0, lambda: self.specs_label.configure(text=text, text_color=THEME["TEXT_MAIN"]))
            self.after(0, lambda: self.title(title))
        threading.Thread(target=task, daemon=True).start()

    def load_wifi_settings(self):
        ip, port = self.history.get_wifi_settings()
        if ip: self.wifi_ip_entry.insert(0, ip)
        if port: 
            self.wifi_port_entry.delete(0, 'end')
            self.wifi_port_entry.insert(0, port)

    def bind_shortcuts(self):
        self.bind("<Control-m>", lambda e: self.launch_mirror())
        self.bind("<Control-M>", lambda e: self.launch_mirror())
        self.bind("<Control-s>", lambda e: self.capture_screen())
        self.bind("<Control-S>", lambda e: self.capture_screen())
        self.bind("<Control-r>", lambda e: self.toggle_recording())
        self.bind("<Control-R>", lambda e: self.toggle_recording())
        self.bind("<Control-f>", lambda e: self.open_output_dir())
        self.bind("<Control-F>", lambda e: self.open_output_dir())

    def device_monitor(self):
        last_devs = []
        while self.running:
            devs = self.adb.get_connected_devices()
            if devs != last_devs:
                last_devs = devs
                valid_devs = [d for d in devs if d['status'] == 'device']
                
                if not valid_devs:
                    self.after(0, lambda: self.device_combo.configure(values=["SIN CONEXIÓN USB"]))
                    self.after(0, lambda: self.device_combo.set("SIN CONEXIÓN USB"))
                    self.after(0, lambda: self.specs_label.configure(text="SIN DISPOSITIVOS CONECTADOS", text_color=THEME["TEXT_SEC"]))
                    self.after(0, lambda: self.title("DroidControl"))
                    self.active_serial = None
                else:
                    combo_values = [f"{d['serial']} ({d['type']})" for d in valid_devs]
                    self.after(0, lambda: self.device_combo.configure(values=combo_values))
                    
                    if not self.active_serial or not any(d['serial'] == self.active_serial for d in valid_devs):
                        self.active_serial = valid_devs[0]['serial']
                        self.after(0, lambda: self.device_combo.set(combo_values[0]))
                        self.update_device_info()
                    
                    types = [d['type'] for d in valid_devs]
                    def update_button():
                        current_text = self.btn_wifi_toggle.cget("text")
                        if current_text not in ["CONECTANDO...", "CERRANDO..."]:
                            if "WiFi" in types:
                                self.btn_wifi_toggle.configure(text="DESCONECTAR")
                            else:
                                self.btn_wifi_toggle.configure(text="CONECTAR")
                    self.after(0, update_button)
            time.sleep(2)

    def open_output_dir(self):
        path = self.history.get_output_dir()
        if os.path.exists(path):
            os.startfile(path)

    def select_output_dir(self):
        current = self.history.get_output_dir()
        path = filedialog.askdirectory(initialdir=current, title="Seleccionar Carpeta de Guardado")
        if path:
            self.history.set_output_dir(path)

    def toggle_wifi(self):
        text = self.btn_wifi_toggle.cget("text")
        if text == "CONECTAR":
            self.connect_wifi()
        elif text == "DESCONECTAR":
            self.disconnect_wifi()

    def connect_wifi(self):
        ip = self.wifi_ip_entry.get().strip()
        port = self.wifi_port_entry.get().strip() or "5555"
        if not ip:
            messagebox.showwarning("Aviso", "Ingresa una dirección IP.")
            return
        
        self.history.set_wifi_settings(ip, port)
        full_endpoint = f"{ip}:{port}"
        
        self.btn_wifi_toggle.configure(state="disabled", text="CONECTANDO...")
        
        def task():
            try:
                code, out, err = self.adb.connect_wireless(full_endpoint)
                success = "connected" in out.lower() or "already connected" in out.lower()
                
                if success:
                    self.active_serial = full_endpoint
                    self.after(0, lambda: self.btn_wifi_toggle.configure(text="DESCONECTAR", state="normal"))
                    self.after(0, self.update_device_info)
                    self.after(500, lambda: self.launch_mirror(full_endpoint))
                else:
                    self.after(0, lambda: messagebox.showerror("Error", f"No se pudo conectar a {full_endpoint}\n\n{out or err}"))
                    self.after(0, lambda: self.btn_wifi_toggle.configure(text="CONECTAR", state="normal"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"Error inesperado: {str(e)}"))
                self.after(0, lambda: self.btn_wifi_toggle.configure(text="CONECTAR", state="normal"))
            
        threading.Thread(target=task, daemon=True).start()

    def disconnect_wifi(self):
        ip = self.wifi_ip_entry.get().strip()
        port = self.wifi_port_entry.get().strip() or "5555"
        full_endpoint = f"{ip}:{port}" if ip else None
        
        self.btn_wifi_toggle.configure(state="disabled", text="CERRANDO...")
        
        def task():
            try:
                self.adb.disconnect_wireless(full_endpoint)
                if self.active_serial == full_endpoint or (full_endpoint and full_endpoint in str(self.active_serial)):
                    self.active_serial = None
                
                self.after(0, lambda: self.btn_wifi_toggle.configure(state="normal", text="CONECTAR"))
            except Exception:
                self.after(0, lambda: self.btn_wifi_toggle.configure(state="normal", text="CONECTAR"))
            
        threading.Thread(target=task, daemon=True).start()

    def pulse_animation(self):
        if not self.running: return
        self.pulse_val += 15 * self.pulse_dir
        if self.pulse_val >= 255:
            self.pulse_val = 255
            self.pulse_dir = -1
        elif self.pulse_val <= 100:
            self.pulse_val = 100
            self.pulse_dir = 1
        
        # Color Cyan: R=0, G=val, B=val
        color = f"#{0:02x}{self.pulse_val:02x}{self.pulse_val:02x}"
        
        # Solo mostrar ONLINE si hay una conexión WiFi activa
        is_wifi = self.active_serial and ":" in str(self.active_serial)
        
        if is_wifi:
            self.indicator_dot.configure(text_color=color, text="● ONLINE")
        else:
            self.indicator_dot.configure(text_color="#333", text="● OFFLINE")
            
        self.after(50, self.pulse_animation)

    def launch_mirror(self, serial=None):
        target_serial = serial or self.active_serial
        if not target_serial:
            messagebox.showwarning("Aviso", "Conecta un dispositivo primero.")
            return
        
        # Evitar abrir múltiples espejos para el mismo dispositivo
        if target_serial in self.mirror_processes:
            proc = self.mirror_processes[target_serial]
            if proc.poll() is None: # Sigue en ejecución
                return
        
        info = self.adb.get_device_info(target_serial)
        title = f"DroidControl - {info['model']}"
        proc = self.adb.start_mirroring(target_serial, window_title=title)
        if proc:
            self.mirror_processes[target_serial] = proc

    def capture_screen(self):
        if not self.active_serial: return
        
        out_dir = self.history.get_output_dir()
        filename = f"cap_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(out_dir, filename)
        
        def task():
            code, out, err = self.adb.take_screenshot(self.active_serial, path)
            if code == 0:
                self.after(0, self._capture_feedback_success)
        
        threading.Thread(target=task, daemon=True).start()

    def _capture_feedback_success(self):
        original_text = "📸 CAPTURAR"
        original_color = THEME["CARD"]
        
        self.btn_capture.configure(text="✅ ¡LISTO!", fg_color=THEME["SUCCESS"], text_color="#000000")
        self.after(1000, lambda: self.btn_capture.configure(text=original_text, fg_color=original_color, text_color=THEME["TEXT_MAIN"]))

    def toggle_recording(self):
        if not self.active_serial: return
        active = self.active_serial

        if active not in self.recording_processes:
            # Iniciar
            out_dir = self.history.get_output_dir()
            filename = f"rec_{active.replace(':', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mkv"
            path = os.path.join(out_dir, filename)
            
            info = self.adb.get_device_info(active)
            record_audio = info.get("android_sdk", 0) >= 30
            
            proc = self.adb.start_recording(active, path, record_audio=record_audio)
            if proc:
                self.recording_processes[active] = (proc, path)
                self.btn_record.configure(text="⏹ DETENER", fg_color=THEME["DANGER"], hover_color=THEME["DANGER_HOVER"])
        else:
            # Detener
            self.btn_record.configure(state="disabled", text="FINALIZANDO...")
            def task():
                proc, path = self.recording_processes[active]
                self.adb.stop_recording(proc)
                del self.recording_processes[active]
                self.after(0, lambda: self.btn_record.configure(state="normal", text="🎥 GRABAR", fg_color=THEME["CARD"], hover_color=THEME["BUTTON_SECONDARY_HOVER"]))
            threading.Thread(target=task, daemon=True).start()

    def on_closing(self):
        self.running = False
        for serial, (proc, path) in self.recording_processes.items():
            self.adb.stop_recording(proc)
        self.destroy()
