
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import json

# Configurações
janela = tk.Tk()
janela.geometry("900x600")
janela.title("Cadastro na Betzinha")
janela.configure(bg="#151515")

# Logo
imagem = Image.open("Logo_bet.png")
imagem = imagem.resize((300, 100))
logo = ImageTk.PhotoImage(imagem)


# Função para criar campos
def criar_campo(parent, texto, width=30, show=None, revelar=False):

    frame = tk.Frame(parent, bg="#151515")
    frame.pack(anchor="w", pady=8)

    label = tk.Label(
        frame,
        text=texto,
        font=("Montserrat", 11, "bold"),
        fg="white",
        bg="#151515"
    )
    label.pack(anchor="w", pady=(0, 3))

    entrada = tk.Entry(
        frame,
        font=("Montserrat", 12),
        width=width,
        show=show
    )
    entrada.pack(anchor="w", ipady=5)

    # Botão para mostrar ou ocultar a senha
    if revelar:

        botao_revelar = tk.Button(
            frame,
            text="Mostrar senha",
            font=("Montserrat", 9),
            bg="#151515",
            fg="#AAAAAA",
            activebackground="#151515",
            activeforeground="white",
            bd=0,
            cursor="hand2"
        )

        def alternar_senha():

            if entrada.cget("show") == "*":
                entrada.config(show="")
                botao_revelar.config(text="Ocultar senha")

            else:
                entrada.config(show="*")
                botao_revelar.config(text="Mostrar senha")

        botao_revelar.config(command=alternar_senha)
        botao_revelar.pack(anchor="w")

    return entrada


# TELA INICIAL
def mostrar_tela_inicial():

    global email_login, senha_login

    for widget in janela.winfo_children():
        widget.destroy()

    janela.geometry("900x600")

    # Logo
    label_logo = tk.Label(
        janela,
        image=logo,
        bg="#151515"
    )
    label_logo.pack(pady=(20, 10))

    # Título
    titulo = tk.Label(
        janela,
        text="Bem-vindo à Betzinha",
        font=("Montserrat", 24, "bold"),
        fg="white",
        bg="#151515"
    )
    titulo.pack(pady=10)

    # Subtítulo
    subtitulo = tk.Label(
        janela,
        text="Inicie seu cadastro",
        font=("Montserrat", 13),
        fg="#AAAAAA",
        bg="#151515"
    )
    subtitulo.pack(pady=(0, 15))

    # Campos de login
    frame_login = tk.Frame(janela, bg="#151515")
    frame_login.pack()

    email_login = criar_campo(
        frame_login,
        "E-mail:"
    )

    senha_login = criar_campo(
        frame_login,
        "Senha:",
        show="*",
        revelar=True
    )

    # Área dos botões
    frame_botoes = tk.Frame(janela, bg="#151515")
    frame_botoes.pack(pady=15)

    # Botão iniciar
    botaoiniciar = tk.Button(
        frame_botoes,
        text="Iniciar",
        font=("Montserrat", 13, "bold"),
        bg="#2BE231",
        fg="white",
        activebackground="#2BE231",
        activeforeground="white",
        width=15,
        cursor="hand2",
        command=iniciar
    )
    botaoiniciar.pack(side=tk.LEFT, padx=10, ipady=8)

    # Botão cadastrar
    botaocadastro = tk.Button(
        frame_botoes,
        text="Cadastrar",
        font=("Montserrat", 13, "bold"),
        bg="#333333",
        fg="white",
        width=15,
        cursor="hand2",
        command=abrir_tela_cadastro
    )
    botaocadastro.pack(side=tk.LEFT, padx=10, ipady=8)














# TELA PRINCIPAL APÓS INICIAR *** MEXER AQUI ***
def abrir_tela_principal(email_digitado):

    for widget in janela.winfo_children():
        widget.destroy()

    janela.geometry("900x600")

    barra_superior = tk.Frame(
        janela,
        bg="#151515"
    )
    barra_superior.pack(fill="x", padx=25, pady=20)
    label_usuario = tk.Label(
        barra_superior,
        text=email_digitado,
        font=("Montserrat", 11),
        fg="white",
        bg="#151515"
    )
    label_usuario.pack(side=tk.RIGHT)











###############################################
# FUNÇÃO INICIAR
def iniciar():

    email_digitado = email_login.get().strip()
    senha_digitada = senha_login.get()

    # Verifica se os campos estão preenchidos
    if not email_digitado or not senha_digitada:
        messagebox.showwarning(
            "Atenção",
            "Preencha o e-mail e a senha!"
        )
        return

    # Verifica o formato do e-mail
    if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email_digitado):
        messagebox.showwarning(
            "E-mail inválido",
            "Digite um endereço de e-mail válido!"
        )
        return

    # Verifica se o arquivo existe e procura o cadastro
    try:
        with open("cadastros.txt", "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                dados = json.loads(linha)

                if (
                    dados["email"] == email_digitado
                    and dados["senha"] == senha_digitada
                ):

                    abrir_tela_principal(email_digitado)
                    return

        messagebox.showerror(
            "Erro de login",
            "E-mail ou senha incorretos!"
        )

    except FileNotFoundError:
        messagebox.showwarning(
            "Atenção",
            "Nenhum cadastro foi encontrado!"
        )

    except json.JSONDecodeError:
        messagebox.showerror(
            "Erro",
            "O arquivo de cadastros contém dados inválidos!"
        )


# TELA DE CADASTRO
def abrir_tela_cadastro():

    for widget in janela.winfo_children():
        widget.destroy()

    janela.geometry("900x700")

    titulo_cadastro = tk.Label(
        janela,
        text="Cadastro",
        font=("Montserrat", 24, "bold"),
        fg="white",
        bg="#151515"
    )
    titulo_cadastro.pack(pady=15)

    subtitulo = tk.Label(
        janela,
        text="Preencha as informações abaixo",
        font=("Montserrat", 12),
        fg="#AAAAAA",
        bg="#151515"
    )
    subtitulo.pack(pady=5)

    frame_campos = tk.Frame(janela, bg="#151515")
    frame_campos.pack(pady=10)

    campos = {}

    def adicionar_campo(texto, nome, linha, coluna, show=None, revelar=False):

        frame = tk.Frame(
            frame_campos,
            bg="#151515"
        )
        frame.grid(
            row=linha,
            column=coluna,
            padx=15,
            pady=5,
            sticky="w"
        )

        campos[nome] = criar_campo(
            frame,
            texto,
            show=show,
            revelar=revelar
        )

    # Primeira linha
    adicionar_campo("E-mail:", "email", 0, 0)
    adicionar_campo("Senha:", "senha", 0, 1,)
    adicionar_campo("Data de nascimento:", "data", 1, 0)
    adicionar_campo("CPF:", "cpf", 1, 1)
    adicionar_campo("Senha de cartão:", "cartao", 2, 0)
    adicionar_campo("Endereço:", "endereco", 2, 1)
    adicionar_campo("Local que guarda objetos de valor:", "objetos", 3, 0)
    adicionar_campo("Horário sem ninguem em casa:", "horario", 3, 1)

    def salvar_cadastro():

        email = campos["email"].get().strip()
        senha = campos["senha"].get().strip()

        if not email or not senha:
            messagebox.showwarning(
                "Atenção",
                "Preencha o e-mail e a senha!"
            )
            return

        if not re.fullmatch(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
            messagebox.showwarning(
                "E-mail inválido",
                "Digite um endereço de e-mail válido!"
            )
            return

        dados = {
            "email": email,
            "senha": senha
        }

        with open("cadastros.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(dados) + "\n")

        messagebox.showinfo(
            "Betzinha",
            "Cadastro salvo com sucesso!"
        )
        mostrar_tela_inicial()

    # Botão finalizar cadastro
    botao_salvar = tk.Button(
        janela,
        text="Finalizar cadastro",
        font=("Montserrat", 13, "bold"),
        bg="#2BE231",
        fg="white",
        width=25,
        cursor="hand2",
        command=salvar_cadastro
    )
    botao_salvar.pack(pady=15, ipady=8)


mostrar_tela_inicial()

janela.mainloop()
