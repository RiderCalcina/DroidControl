# 📱 DroidControl

![Versión](https://img.shields.io/badge/version-1.3.0-cyan.svg)
![Base](https://img.shields.io/badge/GUI_for-SCRCPY-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Plataforma](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**DroidControl** es una interfaz gráfica (GUI) ligera y elegante diseñada específicamente para potenciar el uso de **[scrcpy](https://github.com/Genymobile/scrcpy)**. Permite controlar y visualizar tus dispositivos Android desde el PC con un solo clic, eliminando la complejidad de la consola de comandos.

---

## 🚀 ¿Por qué DroidControl?

Aunque `scrcpy` es la herramienta más potente para el mirroring de Android, su uso a través de la terminal puede ser tedioso para muchos usuarios. **DroidControl** actúa como un panel de control intuitivo que centraliza las funciones más utilizadas en una ventana ultra-compacta de solo **145px** de altura.

---

## ✨ Características Destacadas

### 📺 Control Total vía SCRCPY
- **Mirroring Instantáneo**: Lanzamiento optimizado de `scrcpy` con un solo botón.
- **Detección USB**: Identificación automática de dispositivos conectados por cable.
- **Conexión Inalámbrica (WiFi)**: Gestión de conexiones ADB inalámbricas con historial de IP.

### 🎥 Multimedia y Captura
- **Grabación de Video**: Graba la pantalla de tu móvil en formato `.mkv`.
- **Audio Integrado**: Soporte para grabación de audio en dispositivos con Android 11+.
- **Capturas de Pantalla**: Toma fotos instantáneas de la pantalla en formato `.png`.

### 🎨 Experiencia de Usuario Premium
- **Diseño Minimalista**: Interfaz oscura profesional con efectos de animación "Pulse".
- **Tooltips Dinámicos**: Ayuda contextual al pasar el ratón por cada botón.
- **Atajos de Teclado**: Controla la aplicación sin soltar el teclado.

---

## ⌨️ Atajos de Teclado

| Teclas | Acción |
| :--- | :--- |
| `Ctrl + M` | Abrir Espejo (Mirroring) |
| `Ctrl + S` | Capturar Pantalla |
| `Ctrl + R` | Grabar Pantalla |
| `Ctrl + F` | Abrir Carpeta de Destino |

---

## 🛠️ Instalación y Uso

### Requisitos
1. Tener **Python 3.8+** instalado.
2. Descargar los binarios de `adb` y `scrcpy` y colocarlos en la carpeta `bin/`.

### Pasos rápidos
1. Instala las librerías necesarias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```bash
   python DroidControl.py
   ```
   *(O utiliza el archivo `lanzador.bat`)*

---

## 📂 Estructura del Proyecto

```text
DroidControl/
├── adbappkiller/          # Lógica interna y UI
├── assets/                # Recursos visuales (iconos)
├── bin/                   # Ejecutables de ADB y SCRCPY
├── captures/              # Carpeta de salida por defecto
├── DroidControl.py        # Lanzador principal de la app
├── HELP.md                # Guía detallada de funciones
└── settings.json          # Archivo de configuración
```

---

## 📖 Documentación Adicional
Para más detalles sobre cómo configurar la conexión inalámbrica o solucionar problemas comunes, consulta nuestra **[Guía de Ayuda Detallada (HELP.md)](HELP.md)**.

---

## 🤝 Créditos
Este proyecto es posible gracias a:
- [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)
- [TomSchimansky/CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

Desarrollado por [QwertyAserty](https://qwertyaserty.com/).
