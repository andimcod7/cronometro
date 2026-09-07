import tkinter as tk
import time


class Cronometro:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cronômetro")
        self.janela.geometry("430x290")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#f3f4f6")

        self.tempo_total = 0.0
        self.em_execucao = False
        self.ultimo_tempo = 0.0
        self.id_pos_execucao = None

        self.var_tempo = tk.StringVar(value="00:00:00")
        self.criar_interface()

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="Cronômetro",
            font=("Arial", 24, "bold"),
            fg="#111827",
            bg="#f3f4f6",
            pady=18,
        )
        titulo.pack()

        visor = tk.Label(
            self.janela,
            textvariable=self.var_tempo,
            font=("Arial", 36, "bold"),
            fg="#1f2937",
            bg="#ffffff",
            padx=20,
            pady=18,
            relief="solid",
            borderwidth=2,
        )
        visor.pack(pady=10)

        botoes = tk.Frame(self.janela, bg="#f3f4f6")
        botoes.pack(pady=10)

        tk.Button(
            botoes,
            text="Iniciar",
            width=12,
            height=2,
            bg="#22c55e",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.iniciar,
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            botoes,
            text="Pausar",
            width=12,
            height=2,
            bg="#f59e0b",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.pausar,
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            botoes,
            text="Resetar",
            width=12,
            height=2,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.resetar,
        ).grid(row=0, column=2, padx=8)

    def iniciar(self):
        if self.em_execucao:
            return

        self.em_execucao = True
        self.ultimo_tempo = time.monotonic()
        self.atualizar_tempo()

    def pausar(self):
        if not self.em_execucao:
            return

        agora = time.monotonic()
        self.tempo_total += agora - self.ultimo_tempo

        self.em_execucao = False
        self.atualizar_label()
        if self.id_pos_execucao is not None:
            self.janela.after_cancel(self.id_pos_execucao)
            self.id_pos_execucao = None

    def resetar(self):
        self.em_execucao = False
        if self.id_pos_execucao is not None:
            self.janela.after_cancel(self.id_pos_execucao)
            self.id_pos_execucao = None

        self.tempo_total = 0.0
        self.atualizar_label()

    def atualizar_tempo(self):
        if not self.em_execucao:
            return

        agora = time.monotonic()
        self.tempo_total += agora - self.ultimo_tempo
        self.ultimo_tempo = agora
        self.atualizar_label()

        self.id_pos_execucao = self.janela.after(100, self.atualizar_tempo)

    def atualizar_label(self):
        total_segundos = int(self.tempo_total)
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        self.var_tempo.set(f"{horas:02d}:{minutos:02d}:{segundos:02d}")


if __name__ == "__main__":
    janela = tk.Tk()
    app = Cronometro(janela)
    janela.mainloop()
