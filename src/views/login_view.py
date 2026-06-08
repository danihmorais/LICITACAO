import os
import json
import threading
import customtkinter as ctk
import tkinter as tk 
from tkinter import messagebox
from PIL import Image
import config
import webbrowser
import pyperclip
from updater import verificar_e_atualizar

class LoginView(ctk.CTkFrame):
    CARD_WIDTH = 760
    CARD_BG = ("white", "#111827")
    CARD_BORDER = ("gray85", "#1F2937")
    PRIMARY_COLOR = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    SECONDARY_TEXT = ("gray45", "gray65")

    def __init__(self, master, controller):
        super().__init__(master, fg_color=("gray92", "gray10"))
        self.controller = controller
        self.dev_signature = "@danih.morais"
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_ui()
        self._build_theme_selector()
    
    def _build_ui(self):
        self.card = ctk.CTkFrame(
            self,
            width=self.CARD_WIDTH,
            corner_radius=24,
            fg_color=self.CARD_BG,
            border_width=1,
            border_color=self.CARD_BORDER
        )
        self.card.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        self.card.grid_columnconfigure(0, weight=1)
        
        self._build_header()
        self._build_provider_section()
        self._build_api_section()
        self._build_action_button()
        self._build_footer()

    def _build_theme_selector(self):
        tema_atual = self.controller.get_tema_atual()
        mapa = {"Light": "Claro", "Dark": "Escuro", "System": "Auto"}

        self.theme_selector = ctk.CTkSegmentedButton(
            self.card,
            values=["Claro", "Escuro", "Auto"],
            command=self.mudar_tema,
            font=ctk.CTkFont(size=12)
        )

        self.theme_selector.set(mapa.get(tema_atual, "Auto"))
        self.theme_selector.grid(row=0, column=0, sticky="ne", padx=18, pady=18)

    def mudar_tema(self, valor):
        mapa_inverso = {
            "Claro": "Light",
            "Escuro": "Dark",
            "Auto": "System"
        }
        novo_tema = mapa_inverso.get(valor, "System")
        self.controller.alternar_tema(novo_tema)

    def _build_header(self):
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "logo.png"
        )
        if os.path.exists(logo_path):
            image = Image.open(logo_path)
            self.img_logo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(90, 90)
            )
            ctk.CTkLabel(
                self.card,
                text="",
                image=self.img_logo
            ).grid(row=0, column=0, pady=(40, 10))
        else:
            ctk.CTkLabel(
                self.card,
                text="🏛️",
                font=ctk.CTkFont(size=64)
            ).grid(row=0, column=0, pady=(40, 10))
        ctk.CTkLabel(
            self.card,
            text=config.APP_NAME,
            font=ctk.CTkFont(size=34, weight="bold")
        ).grid(row=1, column=0, pady=(0, 8))
        ctk.CTkLabel(
            self.card,
            text="Automatize a criação de DFD, ETP e TR com Inteligência Artificial",
            font=ctk.CTkFont(size=15),
            text_color=self.SECONDARY_TEXT,
            wraplength=self.CARD_WIDTH - 120,
            justify="center"
        ).grid(row=2, column=0, pady=(0, 35))

    def _build_provider_section(self):
        ultimo_provedor = config.DEFAULT_PROVIDER
        try:
            if os.path.exists(config.ARQUIVO_DADOS):
                with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    ultimo_provedor = dados.get("ultimo_provedor", ultimo_provedor)
        except Exception:
            pass

        self.provedor_var = ctk.StringVar(value=ultimo_provedor)
        self.chave_var = ctk.StringVar()
        ctk.CTkLabel(
            self.card,
            text="Selecione o motor de Inteligência Artificial",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray15", "gray85")
        ).grid(row=3, column=0, pady=(0, 18))
        radio_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        radio_frame.grid(row=4, column=0, pady=(0, 35))
        for val, text in config.PROVEDORES_IA.items():
            rb = ctk.CTkRadioButton(
                radio_frame,
                text=text,
                variable=self.provedor_var,
                value=val,
                command=self.on_provedor_change,
                state="normal",
                font=ctk.CTkFont(size=15),
                border_width_checked=6,
                border_width_unchecked=2
            )
            rb.pack(side="left", padx=25)

    def _build_api_section(self):
        cor_texto = ("gray15", "gray85")
        container = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        container.grid(row=5, column=0, padx=110, sticky="ew")
        container.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            container,
            text="Chave de API",
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=cor_texto
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.entry_chave = ctk.CTkEntry(
            container,
            textvariable=self.chave_var,
            height=48,
            corner_radius=14,
            font=ctk.CTkFont(size=14),
            placeholder_text="Cole sua chave de API aqui",
            state="normal"
        )
        self.entry_chave.grid(row=1, column=0, sticky="ew")
        ctk.CTkButton(
            container,
            text="Não tem uma chave? Saiba como obter gratuitamente.",
            fg_color="transparent",
            hover=False,
            text_color="#2563EB",
            font=ctk.CTkFont(size=13),
            command=self.mostrar_ajuda,
            state="normal"
        ).grid(row=2, column=0, pady=(10, 0))

    def _build_action_button(self):
        ctk.CTkButton(
            self.card,
            text="Acessar Sistema",
            command=self.fazer_login,
            height=52,
            width=320,
            corner_radius=14,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.PRIMARY_COLOR,
            hover_color=self.PRIMARY_HOVER
        ).grid(row=6, column=0, pady=(45, 45))

    def _build_footer(self):
        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        footer.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 14))
        
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=0)
        footer.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(
            footer,
            text="CONECTADO À API",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#22C55E"
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkButton(
            footer,
            text="Verificar Atualizações",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="transparent",
            text_color=self.PRIMARY_COLOR,
            hover=False,
            command=self.verificar_atualizacao_manual
        ).grid(row=0, column=1)
        
        ctk.CTkLabel(
            footer,
            text=self.dev_signature,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray55", "gray45")
        ).grid(row=0, column=2, sticky="e")
        self.on_provedor_change()

    def verificar_atualizacao_manual(self):
        def check():
            tem_atualizacao = verificar_e_atualizar(config.APP_VERSION)
            if not tem_atualizacao:
                messagebox.showinfo("Atualização", "O sistema já está na versão mais recente.")
        threading.Thread(target=check, daemon=True).start()

    def on_provedor_change(self):
        provedor = self.provedor_var.get()
        self.chave_var.set("")
        chave_salva = self.controller.carregar_chave_keyring(provedor)
        if chave_salva:
            self.chave_var.set(chave_salva)

    def mostrar_ajuda(self):
        provider = self.provedor_var.get()
        if provider == "openrouter":
            titulo = "Obter chave da OpenRouter"
            url = "https://openrouter.ai/settings/keys"
            texto = (
                "1. Faça login na plataforma OpenRouter.\n"
                "2. Acesse a seção API Keys.\n"
                "3. Gere uma nova chave secreta.\n"
                "4. Copie e cole no sistema."
            )
        else:
            titulo = "Obter chave do Google Gemini"
            url = "https://aistudio.google.com/app/apikey"
            texto = (
                "1. Faça login com sua conta Google.\n"
                "2. Gere uma nova chave de API.\n"
                "3. Copie e cole no sistema."
            )
            
        janela = tk.Toplevel(self)
        janela.title(titulo)
        janela.resizable(False, False)
        janela.withdraw()
        janela.configure(bg="#1F2937")
        
        width = 600
        height = 320
    
        def centralizar_janela():
            parent = self.winfo_toplevel()
            parent.update_idletasks()
            
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_w = parent.winfo_width()
            parent_h = parent.winfo_height()
            
            x = parent_x + (parent_w - width) // 2
            y = parent_y + (parent_h - height) // 2
            
            janela.geometry(f"{width}x{height}+{x}+{y}")
            janela.deiconify()

        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.ico")
        if os.path.exists(icon_path):
            janela.after(200, lambda: janela.iconbitmap(icon_path))
        
        janela.grab_set()
        
        frame = ctk.CTkFrame(janela, corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text=titulo,
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            frame,
            text=texto,
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color=("gray30", "gray70")
        ).pack(pady=(0, 20), padx=25)
        
        link_label = ctk.CTkLabel(
            frame,
            text=url,
            text_color="#2563EB",
            cursor="hand2",
            font=ctk.CTkFont(size=13, underline=True)
        )
        link_label.pack()
        link_label.bind(
            "<Button-1>",
            lambda e: webbrowser.open(url)
        )
        
        botoes = ctk.CTkFrame(frame, fg_color="transparent")
        botoes.pack(pady=25)
        
        ctk.CTkButton(
            botoes,
            text="Abrir no Navegador",
            width=180,
            command=lambda: webbrowser.open(url)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            botoes,
            text="Copiar Link",
            width=140,
            fg_color="gray25",
            hover_color="gray35",
            command=lambda: pyperclip.copy(url)
        ).pack(side="left", padx=10)
        
        janela.after(50, centralizar_janela)

    def fazer_login(self):
        self.controller.realizar_login(
            self.provedor_var.get(),
            self.chave_var.get().strip()
        )