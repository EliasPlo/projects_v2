import os
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Musiikkisoitin")
        self.root.geometry("500x400")

        # Alusta pygame-mixer
        pygame.mixer.init()

        # Tilan muuttujat
        self.current_file = None
        self.is_playing = False
        self.playlists = self.load_playlists()
        self.selected_playlist = None

        # Päävalikko
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Soittolistavalikko
        self.playlist_frame = tk.Frame(self.root)

        # Käyttöliittymä
        self.create_main_ui()
        self.create_playlist_ui()

    def create_main_ui(self):
        # Kappalelista
        self.song_label = tk.Label(self.main_frame, text="Kappaleet")
        self.song_label.pack(pady=5)

        self.song_box = tk.Listbox(self.main_frame, height=10)
        self.song_box.pack(pady=5)
        self.song_box.bind('<<ListboxSelect>>', self.select_song)

        # Painikkeet
        self.play_button = tk.Button(self.main_frame, text="Toista", command=self.play_music, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.main_frame, text="Pysäytä", command=self.pause_music, state=tk.DISABLED)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(self.main_frame, text="Lopeta", command=self.stop_music, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Palaa soittolistanäkymään
        self.back_to_playlists_button = tk.Button(self.main_frame, text="Takaisin Soittolistoihin", command=self.show_playlists)
        self.back_to_playlists_button.pack(pady=10)

    def create_playlist_ui(self):
        # Soittolistat
        self.playlist_label = tk.Label(self.playlist_frame, text="Soittolistat")
        self.playlist_label.pack(pady=5)

        self.playlist_box = tk.Listbox(self.playlist_frame, height=6)
        self.playlist_box.pack(pady=5)
        self.playlist_box.bind('<<ListboxSelect>>', self.load_playlist)

        self.add_playlist_button = tk.Button(self.playlist_frame, text="Lisää Soittolista", command=self.add_playlist)
        self.add_playlist_button.pack(pady=5)

        self.load_playlists_into_listbox()

    def show_playlists(self):
        self.main_frame.pack_forget()
        self.playlist_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_ui(self):
        self.playlist_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def add_playlist(self):
        directory = filedialog.askdirectory(title="Valitse kansio")
        if directory:
            name = os.path.basename(directory)
            self.playlists[name] = directory
            self.save_playlists()
            self.load_playlists_into_listbox()

    def load_playlists_into_listbox(self):
        self.playlist_box.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_box.insert(tk.END, playlist)

    def load_playlist(self, event):
        selection = self.playlist_box.curselection()
        if selection:
            playlist_name = self.playlist_box.get(selection[0])
            self.selected_playlist = self.playlists[playlist_name]
            self.load_songs_into_listbox()
            self.show_main_ui()

    def load_songs_into_listbox(self):
        self.song_box.delete(0, tk.END)
        if self.selected_playlist:
            for file in os.listdir(self.selected_playlist):
                if file.endswith(".mp3"):
                    self.song_box.insert(tk.END, file)

    def select_song(self, event):
        selection = self.song_box.curselection()
        if selection:
            song_name = self.song_box.get(selection[0])
            self.current_file = os.path.join(self.selected_playlist, song_name)
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

    def save_playlists(self):
        with open("playlists.json", "w") as f:
            json.dump(self.playlists, f)

    def load_playlists(self):
        if os.path.exists("playlists.json"):
            with open("playlists.json", "r") as f:
                return json.load(f)
        return {}

# Luo pääikkuna ja käynnistä sovellus
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    app.show_playlists()
    root.mainloop()
