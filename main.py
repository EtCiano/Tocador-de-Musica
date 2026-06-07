import customtkinter as ctk
import os
from os import listdir
from os.path import isfile, join
import pygame
from mutagen.mp3 import MP3

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_musicas = os.path.join(diretorio_atual, 'musicas')
musicas = [f for f in listdir(caminho_musicas) if isfile(join(caminho_musicas, f))]

for i, musica in enumerate(musicas):
    print(f'> {i} - {musica}')

FIM_DA_MUSICA = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(FIM_DA_MUSICA)

pygame.mixer.init()
pygame.display.init()

class AudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.musicaAtualIndex = 0

        self.pausado = True
        self.musica_carregada = False

        self.title("Player de Áudio")
        self.geometry("400x200")

        self.label = ctk.CTkLabel(self, text="Clique em Play para começar", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)
        
        self.label_tempo = ctk.CTkLabel(self, text="00:00 / 00:00", font=("Arial", 14))
        self.label_tempo.pack(pady=5)

        self.barra_progresso = ctk.CTkProgressBar(self, width=300)
        self.barra_progresso.set(0)
        self.barra_progresso.pack(pady=10)

        self.frame_botoes = ctk.CTkFrame(self, height=50, width=300)
        self.frame_botoes.pack(pady=10)
        self.frame_botoes.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.btn_before = ctk.CTkButton(self.frame_botoes, text="⏪",width=50 , command=self.musica_anterior)
        self.btn_before.grid(row=0, column=0, padx=10, pady=10)

        self.btn_play = ctk.CTkButton(self.frame_botoes, text="▶️",width=50 , command=self.dar_play)
        self.btn_play.grid(row=0, column=1, padx=10, pady=10)

        self.btn_next = ctk.CTkButton(self.frame_botoes, text="⏩",width=50 , command=self.proxima_musica)
        self.btn_next.grid(row=0, column=2, padx=10, pady=10)

        self.verificar_eventos_som()

    def formatar_tempo(self, segundos_totais):
        minutos = int(segundos_totais // 60)
        segundos = int(segundos_totais % 60)
        return f"{minutos:02d}:{segundos:02d}"

    def dar_play(self):
        if self.pausado == False:
            pygame.mixer.music.pause()
            self.pausado = True
            self.btn_play.configure(text="▶️ Play")
            return

        elif self.pausado == True and self.musica_carregada:
            self.pausado = False
            self.btn_play.configure(text="⏸️ Pause")
            pygame.mixer.music.unpause()
            return
        
        try:
            musicaAtual = os.path.join(caminho_musicas, musicas[self.musicaAtualIndex])
            audio = MP3(musicaAtual)
            self.tempo_total_segundos = audio.info.length
            self.passo_tempo = 1 / (self.tempo_total_segundos)

            pygame.mixer.music.load(musicaAtual)
            pygame.mixer.music.play()
            self.musica_carregada = True
            self.pausado = False
            self.btn_play.configure(text="⏸️ Pause")

            self.label.configure(text=musicas[self.musicaAtualIndex].strip('.mp3'))
            print(f'tocando {musicas[self.musicaAtualIndex]}')

            self.atualizar_relogio()
        except pygame.error as e:
            self.label.configure(text="Erro ao carregar arquivo")
    
    def atualizar_relogio(self):
        if pygame.mixer.music.get_busy():
            self.tempo_atual_segundos = pygame.mixer.music.get_pos() / 1000
            atual_formatado = self.formatar_tempo(self.tempo_atual_segundos)
            total_formatado = self.formatar_tempo(self.tempo_total_segundos)
            self.barra_progresso.set(self.tempo_atual_segundos / self.tempo_total_segundos)
            self.label_tempo.configure(text=f"{atual_formatado} / {total_formatado}")

            self.after(1000, self.atualizar_relogio)

    def verificar_eventos_som(self):
        for evento in pygame.event.get():
            if evento.type == FIM_DA_MUSICA:
                self.musica_terminou()

        self.after(100, self.verificar_eventos_som)

    def musica_terminou(self):
        self.musicaAtualIndex += 1
        self.dar_play()
        self.label_tempo.configure(text="00:00 / 00:00")
        self.barra_progresso.set(0)

    def proxima_musica(self):
        if self.musicaAtualIndex == len(musicas)-1:
            self.musicaAtualIndex = 0
        else:
            self.musicaAtualIndex += 1
        
        self.musica_carregada = False
        self.pausado = True
        self.dar_play()

    def musica_anterior(self):
        if self.musicaAtualIndex == 0:
            self.musicaAtualIndex = len(musicas) - 1
        else:
            self.musicaAtualIndex -= 1
        
        self.musica_carregada = False
        self.pausado = True
        self.dar_play()

if __name__ == "__main__":
    app = AudioApp()
    app.mainloop()