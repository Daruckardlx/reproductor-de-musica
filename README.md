# 🎵 Reproductor de Música 3D Style - Python

Un reproductor de música ligero y estilizado construido completamente en Python. Utiliza **Tkinter** para la interfaz gráfica y **Pygame** como motor de audio. Destaca por incluir una visualización pseudo-3D de barras de ecualización animadas al estilo de los reproductores clásicos como Windows Media Player.


## ✨ Características Principales

*   **Visualizador 3D Isométrico:** Barras de ecualización animadas en tiempo real creadas directamente sobre el Canvas de Tkinter, sin necesidad de motores gráficos pesados.
*   **Gestor de Carpetas:** Agrega directorios completos. El programa escanea recursivamente buscando archivos de audio compatibles.
*   **Reproducción Continua (Auto-Play):** Detecta automáticamente cuando una canción termina y reproduce la siguiente en la lista.
*   **Sistema de Favoritos Persistente:** Añade tus canciones preferidas a una pestaña especial. Los favoritos se guardan localmente en un archivo `favoritos.json`, por lo que no los perderás al cerrar la aplicación.
*   **Controles Clásicos:** Botones intuitivos para Anterior, Play, Pausa y Siguiente.
*   **Soporte de Formatos:** Compatible con `.mp3`, `.wav` y `.ogg`.

## 🛠️ Requisitos Previos

Para ejecutar este proyecto, necesitas tener instalado **Python 3.x** en tu sistema y la librería `pygame` para el procesamiento de audio.

## 🚀 Instalación y Uso

1. **Clona o descarga el repositorio:**
   Si descargaste el archivo ZIP, extráelo en una carpeta de tu elección.

2. **Instala las dependencias necesarias:**
   Abre tu terminal o símbolo del sistema y ejecuta el siguiente comando para instalar Pygame:
   ```bash
   pip install pygame

   > **Nota importante:** Este proyecto requiere **`pygame-ce`** (*Community Edition*) en lugar de la versión clásica de `pygame`, debido a problemas de compatibilidad y compilación en versiones recientes de Python (Python 3.12+ / 3.14).
