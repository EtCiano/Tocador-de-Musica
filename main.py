import customtkinter as ctk
import os
from os import listdir
from os.path import isfile, join
import pygame

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Junta a pasta com o nome do arquivo de áudio
caminho_musicas = os.path.join(diretorio_atual, 'musicas')
musicas = sorted([f for f in listdir(caminho_musicas) if isfile(join(caminho_musicas, f))], key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
for musica in musicas:
    print(f'> {musica}, {type(musica)}')

pygame.mixer.init()

class AudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Player de Áudio")
        self.geometry("300x200")

        # Configuração da interface
        self.label = ctk.CTkLabel(self, text="Pygame + CustomTkinter", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)

        self.btn_play = ctk.CTkButton(self, text="▶️ Play", command=self.dar_play)
        self.btn_play.pack(pady=10)

        self.btn_stop = ctk.CTkButton(self, text="⏹️ Stop", command=self.dar_stop, fg_color="crimson", hover_color="darkred")
        self.btn_stop.pack(pady=10)

    def dar_play(self):
        try:
            # pygame.mixer.music.load(caminho_completo)
            pygame.mixer.music.play()
            self.label.configure(text="Tocando música... 🎶")
        except pygame.error as e:
            self.label.configure(text="Erro ao carregar arquivo")

    def dar_stop(self):
        pygame.mixer.music.stop()
        self.label.configure(text="Música parada.")

# Executa o aplicativo
if __name__ == "__main__":
    app = AudioApp()
    app.mainloop()