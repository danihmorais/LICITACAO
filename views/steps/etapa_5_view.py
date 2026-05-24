import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox

class Etapa5View(ctk.CTkFrame):
    SECTION_TITLE_COLOR = ("gray15", "gray85")
    SECTION_HELP_COLOR = ("gray45", "gray65")
    ACCENT_COLOR = "#2563EB"

    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.caminho_imagem_dotacao = ""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.var_instrumento = ctk.StringVar(value="CONTRATO")
        self.var_prorrogar = ctk.BooleanVar(value=False)
        self.var_meepp = ctk.StringVar(value="SIM")
        self.var_criterio = ctk.StringVar(value="ITEM")
        self.var_modalidade = ctk.StringVar(value="PREGAO_ELETRONICO")
        self.var_pac = ctk.StringVar(value="SIM")

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
            text="Tipo de Instrumento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=0, column=0, sticky="w", pady=(25, 8), padx=35)

        self.frame_radio = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_radio.grid(row=1, column=0, sticky="ew", padx=35, pady=(0, 10))

        ctk.CTkRadioButton(
            self.frame_radio,
            text="CONTRATO (Certeza da quantidade)",
            font=ctk.CTkFont(size=14),
            variable=self.var_instrumento,
            value="CONTRATO",
            command=self.atualizar_opcoes_contrato,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_radio,
            text="ATA DE REGISTRO DE PREÇOS (Sem certeza da quantidade)",
            font=ctk.CTkFont(size=14),
            variable=self.var_instrumento,
            value="ATA",
            command=self.atualizar_opcoes_contrato,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_radio,
            text="SEM CONTRATO (Dispensa pequeno valor)",
            font=ctk.CTkFont(size=14),
            variable=self.var_instrumento,
            value="SEM_CONTRATO",
            command=self.atualizar_opcoes_contrato,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)
        
        self.chk_prorroga = ctk.CTkCheckBox(
            self.container,
            text="Permitir prorrogação?",
            font=ctk.CTkFont(size=14),
            variable=self.var_prorrogar,
            border_width=2
        )
        self.chk_prorroga.grid(row=2, column=0, sticky="w", pady=(5, 15), padx=35)

        ctk.CTkLabel(
            self.container,
            text="Participação ME/EPP",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=3, column=0, sticky="w", pady=(10, 5), padx=35)

        self.frame_meepp = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_meepp.grid(row=4, column=0, sticky="ew", padx=35, pady=(0, 15))

        ctk.CTkRadioButton(
            self.frame_meepp,
            text="Exclusiva para ME/EPP (Até R$ 80.000,00)",
            font=ctk.CTkFont(size=14),
            variable=self.var_meepp,
            value="SIM",
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_meepp,
            text="Não Exclusiva (Maior que R$ 80.000,00 ou ampla participação)",
            font=ctk.CTkFont(size=14),
            variable=self.var_meepp,
            value="NAO",
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkLabel(
            self.container,
            text="Critério de Julgamento",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=5, column=0, sticky="w", pady=(10, 0), padx=35)

        self.lbl_regra_criterio = ctk.CTkLabel(
            self.container,
            text="Regra geral da Lei 14.133/21: A adjudicação deve ser preferencialmente por ITEM para ampliar a concorrência.",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=self.SECTION_HELP_COLOR,
            wraplength=660,
            justify="left"
        )
        self.lbl_regra_criterio.grid(row=6, column=0, sticky="w", padx=35, pady=(0, 5))

        self.frame_criterio = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_criterio.grid(row=7, column=0, sticky="ew", padx=35, pady=(0, 10))

        ctk.CTkRadioButton(
            self.frame_criterio,
            text="Menor preço por item",
            font=ctk.CTkFont(size=14),
            variable=self.var_criterio,
            value="ITEM",
            command=self.alternar_justificativa_criterio,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_criterio,
            text="Menor preço global",
            font=ctk.CTkFont(size=14),
            variable=self.var_criterio,
            value="GLOBAL",
            command=self.alternar_justificativa_criterio,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_criterio,
            text="Menor preço por lote",
            font=ctk.CTkFont(size=14),
            variable=self.var_criterio,
            value="LOTE",
            command=self.alternar_justificativa_criterio,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        self.frame_motivo_criterio = ctk.CTkFrame(self.container, fg_color="transparent")
        self.row_motivo_criterio = 8
        
        self.lbl_motivo_criterio = ctk.CTkLabel(
            self.frame_motivo_criterio,
            text="Motivação simples para o agrupamento (Global/Lote):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        )
        self.lbl_motivo_criterio.pack(anchor="w", padx=25, pady=(5, 2))
        
        self.txt_motivo_criterio = ctk.CTkTextbox(
            self.frame_motivo_criterio,
            height=60,
            width=500,
            corner_radius=12,
            border_width=1,
            border_color=("gray85", "#1F2937"),
            font=ctk.CTkFont(size=13)
        )
        self.txt_motivo_criterio.pack(anchor="w", padx=35, pady=(0, 10))

        ctk.CTkLabel(
            self.container,
            text="Modalidade",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=9, column=0, sticky="w", pady=(10, 0), padx=35)

        self.lbl_regra_modalidade = ctk.CTkLabel(
            self.container,
            text="Regra geral da Lei 14.133/21: O Pregão Eletrônico é a modalidade obrigatória padrão.",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=self.SECTION_HELP_COLOR,
            wraplength=660,
            justify="left"
        )
        self.lbl_regra_modalidade.grid(row=10, column=0, sticky="w", padx=35, pady=(0, 5))

        self.frame_modalidade = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_modalidade.grid(row=11, column=0, sticky="ew", padx=35, pady=(0, 10))

        ctk.CTkRadioButton(
            self.frame_modalidade,
            text="Pregão Eletrônico",
            font=ctk.CTkFont(size=14),
            variable=self.var_modalidade,
            value="PREGAO_ELETRONICO",
            command=self.alternar_justificativa_modalidade,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_modalidade,
            text="Dispensa por e-mail",
            font=ctk.CTkFont(size=14),
            variable=self.var_modalidade,
            value="DISPENSA_EMAIL",
            command=self.alternar_justificativa_modalidade,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_modalidade,
            text="Dispensa com lances na BLL",
            font=ctk.CTkFont(size=14),
            variable=self.var_modalidade,
            value="DISPENSA_BLL",
            command=self.alternar_justificativa_modalidade,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_modalidade,
            text="Pregão Presencial",
            font=ctk.CTkFont(size=14),
            variable=self.var_modalidade,
            value="PREGAO_PRESENCIAL",
            command=self.alternar_justificativa_modalidade,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        self.frame_motivo_modalidade = ctk.CTkFrame(self.container, fg_color="transparent")
        self.row_motivo_modalidade = 12
        
        self.lbl_motivo_modalidade = ctk.CTkLabel(
            self.frame_motivo_modalidade,
            text="Justificativa simples para a modalidade escolhida:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        )
        self.lbl_motivo_modalidade.pack(anchor="w", padx=35, pady=(5, 2))
        
        self.txt_motivo_modalidade = ctk.CTkTextbox(
            self.frame_motivo_modalidade,
            height=60,
            width=500,
            corner_radius=12,
            border_width=1,
            border_color=("gray85", "#1F2937"),
            font=ctk.CTkFont(size=13)
        )
        self.txt_motivo_modalidade.pack(anchor="w", padx=35, pady=(0, 10))

        ctk.CTkLabel(
            self.container,
            text="Vigência do Contrato/Ata (Máximo 1 ano)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=13, column=0, sticky="w", padx=35, pady=(10, 8))

        self.frame_vigencia = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_vigencia.grid(row=14, column=0, sticky="ew", padx=35, pady=(0, 15))

        self.var_num_vigencia = ctk.IntVar(value=1)
        
        self.btn_sub = ctk.CTkButton(
            self.frame_vigencia,
            text="-",
            width=36,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.decrementar_vigencia
        )
        self.btn_sub.pack(side="left", padx=(0, 5))

        self.entry_vigencia_num = ctk.CTkEntry(
            self.frame_vigencia,
            width=70,
            height=36,
            corner_radius=10,
            textvariable=self.var_num_vigencia,
            justify="center",
            font=ctk.CTkFont(size=14)
        )
        self.entry_vigencia_num.pack(side="left", padx=5)

        self.btn_add = ctk.CTkButton(
            self.frame_vigencia,
            text="+",
            width=36,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.incrementar_vigencia
        )
        self.btn_add.pack(side="left", padx=(5, 15))

        self.combo_unidade = ctk.CTkComboBox(
            self.frame_vigencia,
            values=["Dias", "Meses", "Ano(s)"],
            width=120,
            height=36,
            corner_radius=8,
            state="readonly"
        )
        self.combo_unidade.pack(side="left")
        self.combo_unidade.set("Meses")

        ctk.CTkLabel(
            self.container,
            text="Dotação Orçamentária (Texto ou Imagem)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=15, column=0, sticky="w", padx=35, pady=(10, 8))
        
        self.frame_dotacao = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_dotacao.grid(row=16, column=0, sticky="ew", padx=35, pady=(0, 15))
        
        self.text_dotacao = ctk.CTkTextbox(
            self.frame_dotacao,
            height=70,
            width=420,
            corner_radius=12,
            border_width=1,
            border_color=("gray85", "#1F2937"),
            font=ctk.CTkFont(size=14)
        )
        self.text_dotacao.pack(side="left", padx=(0, 12))
        
        self.btn_img_dotacao = ctk.CTkButton(
            self.frame_dotacao,
            text="Anexar Imagem",
            width=140,
            height=38,
            corner_radius=12,
            fg_color=self.ACCENT_COLOR,
            hover_color="#1D4ED8",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.anexar_imagem
        )
        self.btn_img_dotacao.pack(side="left", anchor="s")

        ctk.CTkLabel(
            self.container,
            text="Plano Anual de Contratações (PAC)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).grid(row=17, column=0, sticky="w", padx=35, pady=(10, 8))

        self.frame_pac = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_pac.grid(row=18, column=0, sticky="ew", padx=35, pady=(0, 10))

        ctk.CTkRadioButton(
            self.frame_pac,
            text="Sim, previsto no PAC",
            font=ctk.CTkFont(size=14),
            variable=self.var_pac,
            value="SIM",
            command=self.alternar_justificativa_pac,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        ctk.CTkRadioButton(
            self.frame_pac,
            text="Não previsto no PAC",
            font=ctk.CTkFont(size=14),
            variable=self.var_pac,
            value="NAO",
            command=self.alternar_justificativa_pac,
            border_width_checked=6,
            border_width_unchecked=2
        ).pack(anchor="w", pady=4)

        self.frame_motivo_pac = ctk.CTkFrame(self.container, fg_color="transparent")
        self.row_motivo_pac = 19
        
        self.lbl_motivo_pac = ctk.CTkLabel(
            self.frame_motivo_pac,
            text="Justificativa simples para a não inclusão no PAC:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        )
        self.lbl_motivo_pac.pack(anchor="w", padx=35, pady=(5, 2))
        
        self.txt_motivo_pac = ctk.CTkTextbox(
            self.frame_motivo_pac,
            height=60,
            width=500,
            corner_radius=12,
            border_width=1,
            border_color=("gray85", "#1F2937"),
            font=ctk.CTkFont(size=13)
        )
        self.txt_motivo_pac.pack(anchor="w", padx=35, pady=(0, 25))

    def alternar_justificativa_criterio(self):
        if self.var_criterio.get() in ["GLOBAL", "LOTE"]:
            self.frame_motivo_criterio.grid(row=self.row_motivo_criterio, column=0, sticky="ew", padx=20)
        else:
            self.frame_motivo_criterio.grid_forget()

    def alternar_justificativa_modalidade(self):
        sel = self.var_modalidade.get()
        if sel in ["DISPENSA_EMAIL", "DISPENSA_BLL"]:
            self.lbl_motivo_modalidade.configure(
                text="Justificativa (Atenção: Limite legal de até 65k ao todo ao longo do ano):"
            )
            self.frame_motivo_modalidade.grid(row=self.row_motivo_modalidade, column=0, sticky="ew", padx=20)
        elif sel == "PREGAO_PRESENCIAL":
            self.lbl_motivo_modalidade.configure(
                text="Justificativa simples (Atenção: Válido para municípios com até 20k habitantes até abril de 2027):"
            )
            self.frame_motivo_modalidade.grid(row=self.row_motivo_modalidade, column=0, sticky="ew", padx=20)
        else:
            self.frame_motivo_modalidade.grid_forget()

    def alternar_justificativa_pac(self):
        if self.var_pac.get() == "NAO":
            self.frame_motivo_pac.grid(row=self.row_motivo_pac, column=0, sticky="ew", padx=20)
        else:
            self.frame_motivo_pac.grid_forget()

    def decrementar_vigencia(self):
        atual = self.var_num_vigencia.get()
        if atual > 1:
            self.var_num_vigencia.set(atual - 1)

    def incrementar_vigencia(self):
        atual = self.var_num_vigencia.get()
        self.var_num_vigencia.set(atual + 1)

    def atualizar_opcoes_contrato(self):
        if self.var_instrumento.get() in ["CONTRATO", "ATA"]:
            self.chk_prorroga.configure(state="normal")
        else:
            self.var_prorrogar.set(False)
            self.chk_prorroga.configure(state="disabled")

    def anexar_imagem(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar Imagem da Dotação",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
        )
        if caminho:
            self.caminho_imagem_dotacao = caminho
            self.btn_img_dotacao.configure(text="Imagem Anexada", fg_color="#10B981", hover_color="#059669")

    def validar_vigencia(self):
        try:
            valor = int(self.var_num_vigencia.get())
            if valor <= 0:
                return False, "A vigência deve ser um número inteiro positivo."
        except ValueError:
            return False, "Insira um número válido para a vigência."

        unidade = self.combo_unidade.get()
        if unidade == "Ano(s)" and valor > 1:
            return False, "A vigência não pode ser superior a 1 ano."
        if unidade == "Meses" and valor > 12:
            return False, "A vigência não pode ser superior a 12 meses (1 ano)."
        if unidade == "Dias" and valor > 365:
            return False, "A vigência não pode ser superior a 365 dias (1 ano)."
        return True, f"{valor} {unidade.lower()}"

    def coletar_dados(self):
        valido, resultado_vigencia = self.validar_vigencia()
        if not valido:
            messagebox.showerror("Erro de Validação", resultado_vigencia)
            return None

        criterio_sel = self.var_criterio.get()
        motivo_criterio = ""
        if criterio_sel in ["GLOBAL", "LOTE"]:
            motivo_criterio = self.txt_motivo_criterio.get("0.0", "end").strip()
            if not motivo_criterio:
                messagebox.showerror("Erro de Validação", "Insira a motivação simples para agrupamento por Lote ou Global.")
                return None

        modalidade_sel = self.var_modalidade.get()
        motivo_modalidade = ""
        if modalidade_sel in ["DISPENSA_EMAIL", "DISPENSA_BLL", "PREGAO_PRESENCIAL"]:
            motivo_modalidade = self.txt_motivo_modalidade.get("0.0", "end").strip()
            if not motivo_modalidade:
                messagebox.showerror("Erro de Validação", "Insira a justificativa simples para a modalidade escolhida.")
                return None

        pac_sel = self.var_pac.get()
        if pac_sel == "SIM":
            motivo_pac = "A contratação está prevista no PAC (Plano Anual de Contratações) 2026, publicado na edição nº 854 do Diario Oficial do Municipio Eletrônico em 30/12/2025."
        else:
            just_pac = self.txt_motivo_pac.get("0.0", "end").strip()
            if not just_pac:
                messagebox.showerror("Erro de Validação", "Insira a justificativa para a não inclusão no PAC.")
                return None
            motivo_pac = f"A contratação não está prevista no PAC. Justificativa base para criar o texto: {just_pac}"

        dotacao = self.text_dotacao.get("0.0", "end").strip() or "[Dotação não informada]"
        if self.caminho_imagem_dotacao:
            dotacao_final = f"__IMG__{self.caminho_imagem_dotacao}"
        else:
            dotacao_final = dotacao

        return {
            "{{INSTRUMENTO}}": self.var_instrumento.get(),
            "{{PRORROGA}}": "SIM" if self.var_prorrogar.get() else "NÃO",
            "{{ME_EPP}}": self.var_meepp.get(),
            "{{CRITERIOS}}": criterio_sel,
            "RAW_MOTIVO_CRITERIO": motivo_criterio,
            "{{MODALIDADE}}": modalidade_sel,
            "RAW_MOTIVO_MODALIDADE": motivo_modalidade,
            "RAW_PAC": motivo_pac,
            "{{VIGENCIA}}": resultado_vigencia,
            "{{DOTACAO}}": dotacao_final
        }