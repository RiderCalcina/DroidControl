# 📖 Guía de Uso - DroidControl

**DroidControl** es una interfaz gráfica (GUI) minimalista diseñada para facilitar el uso de **scrcpy** (Screen Copy). Esta herramienta permite visualizar y controlar dispositivos Android de forma sencilla, eliminando la necesidad de interactuar directamente con la consola de comandos.

---

## 🎮 Interfaz de Usuario

La interfaz se divide en tres bloques principales diseñados para ser compactos y eficientes:

### 1. Bloque USB (Conectividad Directa)
*   **Selector de Dispositivo**: Muestra una lista de los dispositivos Android conectados mediante cable USB. Si no hay ninguno, mostrará "SIN CONEXIÓN USB".
*   **Info del Dispositivo**: Muestra el modelo del dispositivo y la versión de Android detectada.
*   **Botón CONECTAR**: Inicia el modo espejo (Mirroring) utilizando los binarios de `scrcpy` incluidos en la carpeta `bin/`.

### 2. Bloque WIFI (Conectividad Inalámbrica)
*   **IP y Puerto**: Permite ingresar la dirección IP del dispositivo (ej. `192.168.1.5`) y el puerto ADB (por defecto `5555`).
*   **Botón CONECTAR/DESCONECTAR**: Gestiona la conexión inalámbrica. Al conectar, se intentará abrir el espejo automáticamente.
*   **Indicador de Estado**: Un punto dinámico que muestra **● ONLINE** (en cyan) cuando hay una sesión WiFi activa, o **● OFFLINE** cuando no la hay.

### 3. Bloque de Controles (Gestión y Captura)
*   **💾 GUARDAR**: Permite seleccionar la carpeta donde se guardarán las capturas de pantalla y las grabaciones.
*   **📁 ABRIR**: Abre instantáneamente la carpeta de salida en el explorador de archivos de Windows.
*   **📸 CAPTURAR**: Toma una foto de la pantalla actual del dispositivo y la guarda como `.png`. 

*   **🎥 GRABAR**: Inicia o detiene la grabación de video. 
    *   Si el dispositivo tiene **Android 11 o superior**, se intentará grabar audio automáticamente.
    *   Los videos se guardan en formato `.mkv` para asegurar la compatibilidad y calidad.
*   **ℹ️ INFO**: Créditos del desarrollador.

---

## ⌨️ Atajos de Teclado (Hotkeys)

| Combinación | Acción |
| :--- | :--- |
| `Ctrl + M` | Iniciar / Reintentar Espejo (Mirroring) |
| `Ctrl + S` | Tomar Captura de Pantalla |
| `Ctrl + R` | Iniciar / Detener Grabación de Video |
| `Ctrl + F` | Abrir Carpeta de Capturas |

---

## 🛠️ Resolución de Problemas

### 1. El dispositivo no aparece en la lista USB
*   Asegúrate de que la **Depuración USB** esté activada en las "Opciones de Desarrollador" de tu Android.
*   Verifica que el cable USB sea de datos y no solo de carga.
*   Instala los drivers ADB universales si Windows no reconoce el dispositivo.

### 2. Error al conectar por WiFi
*   El PC y el dispositivo Android deben estar en la **misma red WiFi**.

### 3. No se escucha el audio al grabar
*   La grabación de audio nativa a través de `scrcpy` requiere **Android 11 (API 30)** o superior.
*   Asegúrate de que la pantalla del dispositivo no esté bloqueada al iniciar la grabación.

---

## 📂 Archivos del Proyecto
*   `DroidControl.py`: El corazón de la aplicación.
*   `bin/`: Contiene `adb.exe` y `scrcpy.exe`. **No borres estos archivos.**
*   `assets/`: Iconos y recursos necesarios para la interfaz visual.
*   `settings.json`: Guarda tus preferencias (IP, carpeta de guardado) automáticamente.

---
Desarrollado por [QwertyAserty](https://qwertyaserty.com/)
