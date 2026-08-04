import os
import json
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pygame

# Archivo para guardar los favoritos
FAV_FILE = "favoritos.json"

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor 3D Style - Python")
        self.root.geometry("800x650")
        self.root.configure(bg="#1e1e1e")

        # Inicializar Pygame Mixer para el audio
        pygame.mixer.init()
        
        self.playlist = []
        self.favorites = self.load_favorites()
        self.current_song_index = -1
        self.is_paused = False
        self.is_playing = False

        self.setup_ui()
        self.update_clock() # Iniciar loop de chequeo (para auto-play y visualizador)

    def setup_ui(self):
        # --- PANEL DE VISUALIZACIÓN "3D" ---
        self.canvas = tk.Canvas(self.root, bg="black", height=200, highlightthickness=0)
        self.canvas.pack(fill=tk.X, padx=10, pady=10)
        self.bars = []
        # Crear barras pseudo-3D
        for i in range(12):
            x = 50 + (i * 55)
            # Guardamos coordenadas base (x, y)
            self.bars.append({"x": x, "y": 180, "height": 10})

        # --- PANEL DE CONTROLES ---
        control_frame = tk.Frame(self.root, bg="#1e1e1e")
        control_frame.pack(pady=10)

        btn_style = {"bg": "#333333", "fg": "white", "font": ("Arial", 10, "bold"), "width": 10, "bd": 0, "padx": 5, "pady": 5}

        tk.Button(control_frame, text="⏮ Anterior", command=self.prev_song, **btn_style).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="▶ Play", command=self.play_music, **btn_style).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="⏸ Pausa", command=self.pause_music, **btn_style).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="⏭ Siguiente", command=self.next_song, **btn_style).grid(row=0, column=3, padx=5)

        # --- ETIQUETA DE CANCIÓN ACTUAL ---
        self.lbl_current = tk.Label(self.root, text="Ninguna canción reproduciéndose", bg="#1e1e1e", fg="#00ffcc", font=("Arial", 12))
        self.lbl_current.pack(pady=5)

        # --- PANEL DE ACCIONES ---
        action_frame = tk.Frame(self.root, bg="#1e1e1e")
        action_frame.pack(pady=5)
        
        tk.Button(action_frame, text="📁 Agregar Carpeta", command=self.add_folder, bg="#0066cc", fg="white", bd=0, padx=10, pady=5).grid(row=0, column=0, padx=10)
        tk.Button(action_frame, text="⭐ Añadir a Favoritos", command=self.add_to_favorites, bg="#cc9900", fg="white", bd=0, padx=10, pady=5).grid(row=0, column=1, padx=10)

        # --- PESTAÑAS (LISTA GENERAL Y FAVORITOS) ---
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#333", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#0066cc")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame Lista Principal
        self.frame_playlist = tk.Frame(self.notebook, bg="#2b2b2b")
        self.listbox_playlist = tk.Listbox(self.frame_playlist, bg="#2b2b2b", fg="white", selectbackground="#0066cc", bd=0, font=("Arial", 11))
        self.listbox_playlist.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll1 = tk.Scrollbar(self.frame_playlist, command=self.listbox_playlist.yview)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_playlist.config(yscrollcommand=scroll1.set)
        self.notebook.add(self.frame_playlist, text="🎵 Todas las Canciones")

        # Frame Favoritos
        self.frame_favs = tk.Frame(self.notebook, bg="#2b2b2b")
        self.listbox_favs = tk.Listbox(self.frame_favs, bg="#2b2b2b", fg="gold", selectbackground="#0066cc", bd=0, font=("Arial", 11))
        self.listbox_favs.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scroll2 = tk.Scrollbar(self.frame_favs, command=self.listbox_favs.yview)
        scroll2.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_favs.config(yscrollcommand=scroll2.set)
        self.notebook.add(self.frame_favs, text="⭐ Favoritos")

        self.refresh_favorites_list()

    # --- LÓGICA DE REPRODUCCIÓN ---
    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            for root_dir, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(('.mp3', '.wav', '.ogg')):
                        full_path = os.path.join(root_dir, file)
                        self.playlist.append(full_path)
                        self.listbox_playlist.insert(tk.END, os.path.basename(file))

    def play_music(self):
        # Determinar de qué lista reproducir
        current_tab = self.notebook.index(self.notebook.select())
        active_listbox = self.listbox_playlist if current_tab == 0 else self.listbox_favs
        source_list = self.playlist if current_tab == 0 else self.favorites

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
            return

        try:
            selected_idx = active_listbox.curselection()[0]
            self.current_song_index = selected_idx
            song_path = source_list[self.current_song_index]
            
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            
            self.lbl_current.config(text=f"Sonando: {os.path.basename(song_path)}")
            self.is_playing = True
            self.is_paused = False
            
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una canción primero.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reproducir: {e}")

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False

    def next_song(self):
        current_tab = self.notebook.index(self.notebook.select())
        active_listbox = self.listbox_playlist if current_tab == 0 else self.listbox_favs
        source_list = self.playlist if current_tab == 0 else self.favorites

        if not source_list: return

        self.current_song_index = (self.current_song_index + 1) % len(source_list)
        active_listbox.selection_clear(0, tk.END)
        active_listbox.selection_set(self.current_song_index)
        active_listbox.activate(self.current_song_index)
        
        # Resetear estado y reproducir
        self.is_paused = False
        self.play_music()

    def prev_song(self):
        current_tab = self.notebook.index(self.notebook.select())
        active_listbox = self.listbox_playlist if current_tab == 0 else self.listbox_favs
        source_list = self.playlist if current_tab == 0 else self.favorites

        if not source_list: return

        self.current_song_index = (self.current_song_index - 1) % len(source_list)
        active_listbox.selection_clear(0, tk.END)
        active_listbox.selection_set(self.current_song_index)
        active_listbox.activate(self.current_song_index)
        
        self.is_paused = False
        self.play_music()

    # --- LÓGICA DE FAVORITOS ---
    def load_favorites(self):
        if os.path.exists(FAV_FILE):
            with open(FAV_FILE, "r") as file:
                return json.load(file)
        return []

    def save_favorites(self):
        with open(FAV_FILE, "w") as file:
            json.dump(self.favorites, file)

    def add_to_favorites(self):
        try:
            # Solo permitimos añadir desde la lista principal
            selected_idx = self.listbox_playlist.curselection()[0]
            song_path = self.playlist[selected_idx]
            
            if song_path not in self.favorites:
                self.favorites.append(song_path)
                self.save_favorites()
                self.refresh_favorites_list()
                messagebox.showinfo("Éxito", "¡Canción añadida a favoritos!")
            else:
                messagebox.showinfo("Info", "La canción ya está en favoritos.")
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una canción de la pestaña principal.")

    def refresh_favorites_list(self):
        self.listbox_favs.delete(0, tk.END)
        for song in self.favorites:
            self.listbox_favs.insert(tk.END, os.path.basename(song))

    # --- BUCLE DE ACTUALIZACIÓN Y VISUALIZADOR 3D ---
    def update_clock(self):
        # 1. Chequeo de Auto-Play (si la canción terminó naturalmente)
        if self.is_playing and not pygame.mixer.music.get_busy() and not self.is_paused:
            self.next_song()

        # 2. Actualizar visualizador 3D
        self.draw_3d_visualizer()

        # Volver a llamar esta función cada 50 milisegundos
        self.root.after(50, self.update_clock)

    def draw_3d_visualizer(self):
        self.canvas.delete("all")
        
        # Si está sonando, las barras varían su altura al azar (simulando audio)
        # Si no, bajan hasta su posición mínima (10)
        for bar in self.bars:
            if self.is_playing:
                target_height = random.randint(20, 150)
                # Suavizado de animación
                bar["height"] += (target_height - bar["height"]) * 0.3
            else:
                bar["height"] += (10 - bar["height"]) * 0.3

            x = bar["x"]
            y = bar["y"]
            h = bar["height"]
            w = 20  # Ancho de la barra
            d = 15  # Profundidad (efecto 3D isométrico)

            # Colores estilo neón
            color_front = "#00b3ff"
            color_top = "#66d9ff"
            color_side = "#007acc"

            # Cara frontal
            self.canvas.create_rectangle(x, y - h, x + w, y, fill=color_front, outline="")
            
            # Cara superior (polígono)
            self.canvas.create_polygon(
                x, y - h,
                x + w, y - h,
                x + w + d, y - h - d,
                x + d, y - h - d,
                fill=color_top, outline=""
            )
            
            # Cara lateral derecha (polígono)
            self.canvas.create_polygon(
                x + w, y,
                x + w, y - h,
                x + w + d, y - h - d,
                x + w + d, y - d,
                fill=color_side, outline=""
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()