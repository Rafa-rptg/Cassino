from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from random import randint
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk

CENTAVOS = Decimal("0.01")
MAX_JOGADAS = 100

# Paleta de cores baseada no main.py
COR_FUNDO = "#151515"
COR_CARD = "#202020"
COR_BORDA = "#333333"
COR_VERDE = "#2BE231"
COR_VERMELHO = "#FF4444"
COR_TEXTO = "#FFFFFF"
COR_SUBTEXTO = "#AAAAAA"


def dinheiro(valor):
    return Decimal(valor).quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def parse_valor(texto):
    try:
        valor = Decimal(texto.strip().replace(",", "."))
        if valor.is_finite() and valor >= 0:
            return dinheiro(valor)
    except (InvalidOperation, AttributeError):
        pass
    return None


class BetzinhaApp:
    def __init__(self, root, email_usuario=None):
        self.root = root
        self.email_usuario = email_usuario
        self.root.title("Betzinha — Jogo")
        self.root.geometry("900x720")
        self.root.configure(bg=COR_FUNDO)

        self.saldo = Decimal("0.00")
        self.balan = 0
        self.jogadas = 0
        self.jogo_ativo = False

        # Carrega a logo mantendo referência no objeto para não sumir da tela
        try:
            img = Image.open("Logo_bet.png").resize((210, 70))
            self.logo_img = ImageTk.PhotoImage(img)
        except Exception:
            self.logo_img = None

        self._montar_interface()

    def _montar_interface(self):
        # Cabeçalho com Logo e Boas-vindas
        frame_header = tk.Frame(self.root, bg=COR_FUNDO)
        frame_header.pack(fill=tk.X, padx=30, pady=(15, 5))

        if self.logo_img:
            lbl_logo = tk.Label(frame_header, image=self.logo_img, bg=COR_FUNDO)
            lbl_logo.pack(side=tk.LEFT)

        info_usuario = f"Jogador: {self.email_usuario}" if self.email_usuario else "Bem-vindo à Betzinha"
        lbl_user = tk.Label(
            frame_header,
            text=info_usuario,
            font=("Montserrat", 10),
            fg=COR_SUBTEXTO,
            bg=COR_FUNDO,
        )
        lbl_user.pack(side=tk.RIGHT, anchor="s", pady=10)

        # Barra de Status (Saldo e Rodadas)
        frame_status = tk.Frame(
            self.root, bg=COR_CARD, padx=20, pady=12, highlightbackground=COR_BORDA, highlightthickness=1
        )
        frame_status.pack(fill=tk.X, padx=30, pady=8)

        self.lbl_saldo = tk.Label(
            frame_status,
            text="Saldo: R$ 0,00",
            font=("Montserrat", 15, "bold"),
            fg=COR_VERDE,
            bg=COR_CARD,
        )
        self.lbl_saldo.pack(side=tk.LEFT)

        self.lbl_jogadas = tk.Label(
            frame_status,
            text=f"Jogada: 0/{MAX_JOGADAS}",
            font=("Montserrat", 11, "bold"),
            fg=COR_SUBTEXTO,
            bg=COR_CARD,
        )
        self.lbl_jogadas.pack(side=tk.RIGHT)

        # Seção 1: Depósito Inicial
        frame_topo = tk.Frame(
            self.root, bg=COR_CARD, padx=20, pady=12, highlightbackground=COR_BORDA, highlightthickness=1
        )
        frame_topo.pack(fill=tk.X, padx=30, pady=6)

        tk.Label(
            frame_topo,
            text="Depósito Inicial (R$):",
            font=("Montserrat", 11, "bold"),
            fg=COR_TEXTO,
            bg=COR_CARD,
        ).pack(side=tk.LEFT)

        self.entry_deposito = tk.Entry(
            frame_topo,
            width=14,
            font=("Montserrat", 12),
            bg="#2A2A2A",
            fg=COR_TEXTO,
            insertbackground=COR_TEXTO,
            bd=0,
        )
        self.entry_deposito.pack(side=tk.LEFT, padx=12, ipady=5)

        self.btn_depositar = tk.Button(
            frame_topo,
            text="Iniciar Jogo",
            command=self.iniciar_jogo,
            font=("Montserrat", 11, "bold"),
            bg=COR_VERDE,
            fg=COR_TEXTO,
            activebackground="#24C229",
            activeforeground=COR_TEXTO,
            bd=0,
            padx=18,
            pady=6,
            cursor="hand2",
        )
        self.btn_depositar.pack(side=tk.LEFT)

        # Visor dos Números Sorteados
        frame_numeros = tk.Frame(
            self.root, bg=COR_CARD, padx=20, pady=15, highlightbackground=COR_BORDA, highlightthickness=1
        )
        frame_numeros.pack(fill=tk.X, padx=30, pady=6)

        tk.Label(
            frame_numeros,
            text="RESULTADO DA RODADA",
            font=("Montserrat", 9, "bold"),
            fg=COR_SUBTEXTO,
            bg=COR_CARD,
        ).pack()

        self.lbl_numeros = tk.Label(
            frame_numeros,
            text="-   -   -",
            font=("Consolas", 34, "bold"),
            fg=COR_TEXTO,
            bg=COR_CARD,
        )
        self.lbl_numeros.pack(pady=6)

        self.lbl_resultado = tk.Label(
            frame_numeros,
            text="Faça um depósito para começar.",
            font=("Montserrat", 11, "bold"),
            fg=COR_SUBTEXTO,
            bg=COR_CARD,
        )
        self.lbl_resultado.pack()

        # Seção 2: Fazer Aposta
        frame_aposta = tk.Frame(
            self.root, bg=COR_CARD, padx=20, pady=12, highlightbackground=COR_BORDA, highlightthickness=1
        )
        frame_aposta.pack(fill=tk.X, padx=30, pady=6)

        tk.Label(
            frame_aposta,
            text="Valor da Aposta (R$):",
            font=("Montserrat", 11, "bold"),
            fg=COR_TEXTO,
            bg=COR_CARD,
        ).pack(side=tk.LEFT)

        self.entry_aposta = tk.Entry(
            frame_aposta,
            width=14,
            font=("Montserrat", 12),
            bg="#2A2A2A",
            fg=COR_TEXTO,
            disabledbackground="#1A1A1A",
            insertbackground=COR_TEXTO,
            bd=0,
            state=tk.DISABLED,
        )
        self.entry_aposta.pack(side=tk.LEFT, padx=12, ipady=5)

        self.btn_apostar = tk.Button(
            frame_aposta,
            text="Apostar",
            command=self.jogar_rodada,
            state=tk.DISABLED,
            bg=COR_VERDE,
            fg=COR_TEXTO,
            activebackground="#24C229",
            activeforeground=COR_TEXTO,
            font=("Montserrat", 11, "bold"),
            bd=0,
            padx=20,
            pady=6,
            cursor="hand2",
        )
        self.btn_apostar.pack(side=tk.LEFT)

        self.btn_encerrar = tk.Button(
            frame_aposta,
            text="Encerrar",
            command=self.encerrar_jogo,
            state=tk.DISABLED,
            bg=COR_BORDA,
            fg=COR_TEXTO,
            activebackground="#444444",
            activeforeground=COR_TEXTO,
            font=("Montserrat", 10, "bold"),
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
        )
        self.btn_encerrar.pack(side=tk.RIGHT)

        # Histórico / Log
        frame_log = tk.Frame(
            self.root, bg=COR_CARD, padx=15, pady=10, highlightbackground=COR_BORDA, highlightthickness=1
        )
        frame_log.pack(fill=tk.BOTH, expand=True, padx=30, pady=(6, 20))

        tk.Label(
            frame_log,
            text="HISTÓRICO DE JOGADAS",
            font=("Montserrat", 9, "bold"),
            fg=COR_SUBTEXTO,
            bg=COR_CARD,
        ).pack(anchor="w", pady=(0, 5))

        self.txt_log = scrolledtext.ScrolledText(
            frame_log,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#121212",
            fg="#DDDDDD",
            bd=0,
            height=6,
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def log(self, mensagem):
        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.insert(tk.END, mensagem + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.configure(state=tk.DISABLED)

    def atualizar_status(self):
        self.lbl_saldo.config(text=f"Saldo: R$ {dinheiro(self.saldo):.2f}")
        self.lbl_jogadas.config(text=f"Jogada: {self.jogadas}/{MAX_JOGADAS}")

    def iniciar_jogo(self):
        valor = parse_valor(self.entry_deposito.get())
        if valor is None or valor <= 0:
            messagebox.showwarning("Valor inválido", "Digite um valor maior que R$ 0,00 (ex.: 50,00).")
            return

        self.saldo = dinheiro(valor)
        self.balan = 0
        self.jogadas = 0
        self.jogo_ativo = True

        self.txt_log.configure(state=tk.NORMAL)
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.configure(state=tk.DISABLED)

        self.entry_deposito.config(state=tk.DISABLED)
        self.btn_depositar.config(state=tk.DISABLED)
        self.entry_aposta.config(state=tk.NORMAL)
        self.btn_apostar.config(state=tk.NORMAL)
        self.btn_encerrar.config(state=tk.NORMAL)

        self.atualizar_status()
        self.lbl_resultado.config(text="Boa sorte! Faça sua aposta.", fg=COR_TEXTO)
        self.log("É A BETZINHA COM AS MELHORES ODDS DO BRASIL")
        self.log(f"Depósito inicial realizado: R$ {dinheiro(self.saldo):.2f}")

    def calcular_sorte_e_multi(self, valor):
        if self.jogadas == 0 and valor <= 10:
            return 1, Decimal("0.5")
        if self.jogadas == 1 and valor <= 10:
            return randint(0, 1), Decimal("1.5")
        if self.jogadas == 2 and valor >= 10:
            return randint(0, 9), Decimal("2.5")

        if valor <= 20:
            if self.balan <= 3:
                return randint(0, 2), Decimal("1.3")
            return randint(0, 3), Decimal("1.5")
        if valor <= 50:
            if self.balan >= 10:
                return 1, Decimal("1.2")
            return randint(0, 4), Decimal("1.25")
        if valor <= 100:
            return randint(0, 9), Decimal("1.2")
        if valor <= 500:
            return randint(0, 25), Decimal("1.5")
        return randint(0, 30), Decimal("1.25")

    def jogar_rodada(self):
        if not self.jogo_ativo:
            return

        aposta = parse_valor(self.entry_aposta.get())
        if aposta is None:
            messagebox.showwarning("Valor inválido", "Digite um valor válido com duas casas decimais.")
            return
        if aposta <= 0:
            messagebox.showwarning("Aposta inválida", "A aposta deve ser maior que R$ 0,00.")
            return
        if aposta > self.saldo:
            messagebox.showwarning("Saldo insuficiente", "Você não pode apostar mais do que possui.")
            return

        sorte, multi = self.calcular_sorte_e_multi(aposta)

        teste = randint(0, 5)
        teste1 = randint(0, 5)
        teste2 = randint(0, 5)

        if sorte == 1:
            teste1 = teste
            teste2 = teste

        self.lbl_numeros.config(text=f"{teste}   {teste1}   {teste2}")

        if teste == teste1 and teste == teste2:
            ganho = dinheiro(aposta * multi)
            self.saldo = dinheiro(self.saldo + ganho)
            self.balan = 0
            msg = f"Parabéns! Você ganhou R$ {ganho:.2f} (odd {multi}x)."
            self.lbl_numeros.config(fg=COR_VERDE)
            self.lbl_resultado.config(text=msg, fg=COR_VERDE)
            self.log(f"[Rodada {self.jogadas + 1}] Números: {teste} {teste1} {teste2} -> {msg}")
        else:
            self.saldo = dinheiro(self.saldo - aposta)
            self.balan += 1
            msg = f"Poxa, não foi dessa vez (-R$ {aposta:.2f}). Vamos outra?"
            self.lbl_numeros.config(fg=COR_TEXTO)
            self.lbl_resultado.config(text=msg, fg=COR_VERMELHO)
            self.log(f"[Rodada {self.jogadas + 1}] Números: {teste} {teste1} {teste2} -> {msg}")

        self.jogadas += 1
        self.atualizar_status()
        self.entry_aposta.delete(0, tk.END)

        if self.saldo <= 0:
            self._tratar_saldo_zerado()
            return

        if self.jogadas >= MAX_JOGADAS:
            self.encerrar_jogo()

    def _tratar_saldo_zerado(self):
        while self.saldo <= 0:
            quer_add = messagebox.askyesno(
                "Saldo zerado ou negativo",
                f"Seu saldo atual é R$ {dinheiro(self.saldo):.2f}.\nDeseja adicionar mais saldo?",
            )
            if not quer_add:
                self.encerrar_jogo()
                return

            dialogo = tk.Toplevel(self.root)
            dialogo.title("Adicionar Saldo")
            dialogo.geometry("340x150")
            dialogo.configure(bg=COR_FUNDO)
            dialogo.transient(self.root)
            dialogo.grab_set()

            tk.Label(
                dialogo,
                text="Quanto deseja adicionar? (R$)",
                font=("Montserrat", 10, "bold"),
                fg=COR_TEXTO,
                bg=COR_FUNDO,
            ).pack(pady=(15, 6))

            entrada = tk.Entry(
                dialogo,
                width=14,
                font=("Montserrat", 12),
                bg="#2A2A2A",
                fg=COR_TEXTO,
                insertbackground=COR_TEXTO,
                bd=0,
            )
            entrada.pack(ipady=4)
            entrada.focus()

            resultado_add = {"valor": None}

            def confirmar():
                val = parse_valor(entrada.get())
                if val is None or val <= 0:
                    messagebox.showwarning("Valor inválido", "Digite um valor maior que R$ 0,00.", parent=dialogo)
                    return
                resultado_add["valor"] = val
                dialogo.destroy()

            tk.Button(
                dialogo,
                text="Adicionar",
                command=confirmar,
                font=("Montserrat", 10, "bold"),
                bg=COR_VERDE,
                fg=COR_TEXTO,
                bd=0,
                padx=16,
                pady=5,
                cursor="hand2",
            ).pack(pady=12)

            self.root.wait_window(dialogo)

            if resultado_add["valor"] is None:
                self.encerrar_jogo()
                return

            self.saldo = dinheiro(self.saldo + resultado_add["valor"])
            self.atualizar_status()
            self.log(f"Adicionado R$ {resultado_add['valor']:.2f}. Saldo atual: R$ {dinheiro(self.saldo):.2f}")

    def encerrar_jogo(self):
        self.jogo_ativo = False
        self.btn_apostar.config(state=tk.DISABLED)
        self.entry_aposta.config(state=tk.DISABLED)
        self.btn_encerrar.config(state=tk.DISABLED)
        self.entry_deposito.config(state=tk.NORMAL)
        self.btn_depositar.config(state=tk.NORMAL)

        self.atualizar_status()
        self.lbl_resultado.config(text="Jogo encerrado. Faça um novo depósito para jogar novamente.", fg=COR_SUBTEXTO)
        self.log("-" * 55)
        self.log(f"Jogo encerrado! Seu saldo final foi: R$ {dinheiro(self.saldo):.2f}")
        self.log("É A BETZINHA COM AS MELHORES ODDS DO BRASIL")


def iniciar_jogo(root, email_usuario=None):
    BetzinhaApp(root, email_usuario)


if __name__ == "__main__":
    root = tk.Tk()
    iniciar_jogo(root)
    root.mainloop()