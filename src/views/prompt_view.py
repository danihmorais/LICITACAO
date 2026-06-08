import os
import customtkinter as ctk
import tkinter as tk

class PromptView:

    def __init__(self, master, dados_usuario):

        self.resultado = None
        self.dados_usuario = dados_usuario

        titulo = "Instruções Complementares"

        self.janela = tk.Toplevel(master)
        self.janela.title(titulo)
        self.janela.resizable(False, False)
        self.janela.withdraw()
        self.janela.configure(bg="#EDEDED")

        width = 1000
        height = 720

        def centralizar_janela():

            master.update_idletasks()

            parent_x = master.winfo_x()
            parent_y = master.winfo_y()
            parent_w = master.winfo_width()
            parent_h = master.winfo_height()

            x = parent_x + (parent_w - width) // 2
            y = parent_y + (parent_h - height) // 2

            self.janela.geometry(f"{width}x{height}+{x}+{y}")
            self.janela.deiconify()

        self.janela.after(10, centralizar_janela)

        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "logo.ico"
        )

        if os.path.exists(icon_path):
            self.janela.after(
                200,
                lambda: self.janela.iconbitmap(icon_path)
            )

        self.janela.grab_set()

        self.card = ctk.CTkFrame(
            self.janela,
            corner_radius=24,
            fg_color=("white", "#111827"),
            border_width=1,
            border_color=("gray85", "#1F2937")
        )
        self.card.pack(fill="both", expand=True, padx=30, pady=30)

        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.card,
            text="Instruções Adicionais para a IA",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("gray15", "gray85")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=30,
            pady=(30, 5)
        )

        ctk.CTkLabel(
            self.card,
            text=(
                "Precise melhor o foco para a geração. "
                "Adicione regras específicas, pontos de atenção "
                "e referências importantes."
            ),
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65"),
            wraplength=730,
            justify="left"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 15)
        )

        self.text_prompt = ctk.CTkTextbox(
            self.card,
            corner_radius=14,
            border_width=1,
            border_color=("gray85", "#1F2937"),
            font=ctk.CTkFont(size=14)
        )
        self.text_prompt.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 20)
        )

        self.frame_botoes = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.frame_botoes.grid(
            row=3,
            column=0,
            sticky="e",
            padx=30,
            pady=(0, 30)
        )

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes,
            text="Ignorar",
            width=110,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            border_width=2,
            border_color=("gray70", "#374151"),
            text_color=("gray20", "gray80"),
            hover_color=("gray85", "gray20"),
            command=self.cancelar
        )
        self.btn_cancelar.pack(side="left", padx=(0, 10))

        self.btn_confirmar = ctk.CTkButton(
            self.frame_botoes,
            text="Enviar e Gerar",
            width=140,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.confirmar
        )
        self.btn_confirmar.pack(side="left")

    def confirmar(self):
        self.resultado = self.text_prompt.get("0.0", "end").strip()
        self.janela.destroy()

    def cancelar(self):
        self.resultado = ""
        self.janela.destroy()