# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.3.0] - 2026-05-03

### Añadido
- **Tooltips Flotantes**: Sistema de ayuda contextual dinámica que aparece sobre los controles al pasar el mouse, eliminando la necesidad de una barra de estado fija.
- **Parche de Audio Universal**: Soporte mejorado para grabación de audio en dispositivos Xiaomi, Redmi y Poco mediante el uso automático del códec RAW y fuente de reproducción.
- **Indicadores Dinámicos**: Reubicación y centrado del indicador (ONLINE) para un balance visual perfecto en el bloque WiFi.

### Cambiado
- **Compactación Extrema**: Reducción de la altura de la ventana a **145px**, logrando el diseño más eficiente y minimalista hasta la fecha.
- **Unificación Estética**: El botón de conexión USB ahora comparte el estilo visual discreto del bloque WiFi, eliminando distracciones visuales.
- **Márgenes Inteligentes**: Ajuste de los paddings inferiores para evitar que los controles se sientan apretados contra el borde de la ventana.

### Corregido
- **Audio en Grabaciones**: Solucionado el problema donde algunos equipos grababan video sin sonido al utilizar códecs de compresión incompatibles con el hardware móvil.

## [1.2.0] - 2026-02-14

### Añadido
- **Diseño por Bloques**: Interfaz reorganizada en tres secciones delimitadas (Dispositivo, WiFi, Controles) para mayor claridad visual.
- **Estética 3D**: Botones y campos con bordes definidos y efectos de relieve para un diseño más moderno y profesional.
- **Feedback de Conexión**: Nuevos estados visuales ("CONECTANDO...", "CERRANDO...") en el botón de WiFi.

### Cambiado
- **Optimización de Espacio**: Aumento del ancho de la ventana a 480px y ajuste de fuentes (tamaño 9) para evitar textos truncados.
- **Claridad de Estado**: La etiqueta de dispositivo ahora indica explícitamente "SIN CONEXIÓN USB" para evitar confusiones en modo WiFi.
- **Estabilidad WiFi**: Corregido error crítico que bloqueaba el botón de conexión tras un fallo o desconexión; ahora el estado se reinicia correctamente.

## [1.1.0] - 2025-11-04

### Añadido
- **Conexión WiFi**: Nueva interfaz para conectar dispositivos de forma inalámbrica mediante IP y Puerto.
- **Atajos de Teclado**: Soporte para `Ctrl+M` (Espejo), `Ctrl+S` (Captura), `Ctrl+R` (Grabación) y `Ctrl+F` (Abrir carpeta).
- **Feedback Visual**: Animación de pulso en el indicador de estado y confirmación visual al capturar pantalla.
- **Títulos Dinámicos**: La ventana de mirroring ahora muestra el modelo del dispositivo.
- **Documentación**: Nueva documentación detallada en `README.md`, `LICENSE` y `CHANGELOG.md`.

### Cambiado
- **Renombramiento del Proyecto**: Migración de `scrcpy` a `DroidControl`.
- **Interfaz de Usuario**: Reorganización de botones para un flujo de trabajo más lógico (Guardar, Abrir, Espejo, Capturar, Grabar).
- **Optimización**: Mejoras en la detección de dispositivos y gestión de procesos en segundo plano.

## [1.0.0] - 2025-08-11

### Añadido
- Lanzamiento inicial de DroidControl.
- Soporte básico para Mirroring, Captura y Grabación.
- Integración con CustomTkinter para interfaz oscura.
- Sistema de persistencia para directorios de salida.
