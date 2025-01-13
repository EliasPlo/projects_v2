import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Musiikkisoitin")
        self.root.geometry("400x300")

        # Alusta pygame-mixer
        pygame.mixer.init()

        # Tilan muuttujat
        self.current_file = None
        self.is_playing = False

        # Käyttöliittymä
        self.create_ui()

    def create_ui(self):
        # Otsikko
        self.label = tk.Label(self.root, text="Ei kappaletta valittuna", wraplength=300)
        self.label.pack(pady=10)

        # Painikkeet
        self.play_button = tk.Button(self.root, text="Toista", command=self.play_music, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pysäytä", command=self.pause_music, state=tk.DISABLED)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Lopeta", command=self.stop_music, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.open_button = tk.Button(self.root, text="Avaa tiedosto", command=self.open_file)
        self.open_button.pack(pady=20)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Valitse MP3-tiedosto", filetypes=[("MP3-tiedostot", "*.mp3")]
        )
        if file_path:
            self.current_file = file_path
            self.label.config(text=f"Valittu tiedosto: {os.path.basename(file_path)}")
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)

    def play_music(self):
        if self.current_file:
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.pause_button.config(text="Jatka", command=self.resume_music)
        else:
            self.resume_music()

    def resume_music(self):
        pygame.mixer.music.unpause()
        self.is_playing = True
        self.pause_button.config(text="Pysäytä", command=self.pause_music)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Pysäytä")

# Luo pääikkuna ja käynnistä sovellus
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
