import customtkinter as ctk

class Etapa2View(ctk.CTkFrame):
    SECTION_TITLE_COLOR = ("gray15", "gray85")
    SECTION_HELP_COLOR = ("gray45", "gray65")
    ACCENT_COLOR = "#2563EB"

    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=("white", "#111827"),
            border_width=1,
            border_color=("gray85", "#1F2937")
        )
        self.container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.container,
            text="Condições de Execução e Prazos",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=0, column=0, sticky="w", padx=35, pady=(25, 8))

        ctk.CTkLabel(
            self.container,
            text="Informe os principais requisitos de execução, prazos e medidas de controle de qualidade.",
            font=ctk.CTkFont(size=13),
            text_color=self.SECTION_HELP_COLOR,
            wraplength=680,
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=35, pady=(0, 18))

        self.options_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.options_frame.grid(row=2, column=0, sticky="w", padx=35, pady=(0, 15))

        self.var_amostra = ctk.BooleanVar(value=False)
        self.var_vistoria = ctk.BooleanVar(value=False)

        self.check_amostra = ctk.CTkCheckBox(
            self.options_frame,
            text="Exigir amostra",
            variable=self.var_amostra
        )
        self.check_amostra.grid(row=0, column=0, padx=(0, 20), pady=0)

        self.check_vistoria = ctk.CTkCheckBox(
            self.options_frame,
            text="Exigir vistoria",
            variable=self.var_vistoria
        )
        self.check_vistoria.grid(row=0, column=1, pady=0)

        self.text_execucao = ctk.CTkTextbox(
            self.container,
            height=180,
            corner_radius=12,
            border_width=1,
            border_color=("gray85", "#1F2937"),
            font=ctk.CTkFont(size=14)
        )
        self.text_execucao.grid(row=3, column=0, sticky="ew", padx=35, pady=(0, 20))
        self.text_execucao._y_scrollbar.grid_configure(padx=(0, 6))

    def coletar_dados(self):
        execucao_raw = self.text_execucao.get("0.0", "end").strip() or "[Condições de execução não informadas]"

        return {
            "RAW_EXECUCAO": execucao_raw,
            "{{AMOST}}": "sim" if self.var_amostra.get() else "nao",
            "{{VIST}}": "sim" if self.var_vistoria.get() else "nao"
        }