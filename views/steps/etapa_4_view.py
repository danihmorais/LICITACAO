import customtkinter as ctk
import os
import tkinter as tk
from tkinter import messagebox

class Etapa4View(ctk.CTkFrame):
    SECTION_TITLE_COLOR = ("gray15", "gray85")
    SECTION_HELP_COLOR = ("gray45", "gray65")
    ACCENT_COLOR = "#2563EB"

    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller

        self.gestores_adicionados = []
        self.fiscais_adicionados = []

        self.container = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=("white", "#111827"),
            border_width=1,
            border_color=("gray85", "#1F2937")
        )
        self.container.pack(fill="x", padx=0, pady=0, anchor="n")

        ctk.CTkLabel(
            self.container,
            text="Gestores do Contrato",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).pack(anchor="w", padx=35, pady=(25, 8))

        ctk.CTkLabel(
            self.container,
            text="Adicione os responsáveis pelo contrato e mantenha o histórico de gestores disponíveis.",
            font=ctk.CTkFont(size=13),
            text_color=self.SECTION_HELP_COLOR,
            wraplength=640,
            justify="left"
        ).pack(anchor="w", padx=35, pady=(0, 10))

        self.frame_gestor = ctk.CTkFrame(
            self.container,
            height=250,
            fg_color=("gray98", "#0F172A"),
            corner_radius=14,
            border_width=1,
            border_color=("gray88", "#1E293B")
        )
        self.frame_gestor.pack(fill="x", padx=35, pady=(0, 15))
        self.frame_gestor.pack_propagate(False)

        input_area_gestor = ctk.CTkFrame(self.frame_gestor, fg_color="transparent")
        input_area_gestor.pack(fill="x", padx=20, pady=(15, 5))

        entradas_gestor_frame = ctk.CTkFrame(input_area_gestor, fg_color="transparent")
        entradas_gestor_frame.pack(side=tk.LEFT, fill="both", expand=True)

        bloco_nome_g = ctk.CTkFrame(entradas_gestor_frame, fg_color="transparent")
        bloco_nome_g.pack(side=tk.LEFT, padx=(0, 15))
        ctk.CTkLabel(
            bloco_nome_g, text="Nome", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        self.entry_gestor = ctk.CTkEntry(
            bloco_nome_g, width=280, height=38, corner_radius=10, border_width=1,
border_color=("gray82", "#374151"),
fg_color=("white", "#111827"), font=ctk.CTkFont(size=13)
        )
        self.entry_gestor.pack()

        bloco_cargo_g = ctk.CTkFrame(entradas_gestor_frame, fg_color="transparent")
        bloco_cargo_g.pack(side=tk.LEFT)
        ctk.CTkLabel(
            bloco_cargo_g, text="Cargo", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        self.entry_gestor_cargo = ctk.CTkEntry(
            bloco_cargo_g, width=240, height=38, corner_radius=10, border_width=1,
border_color=("gray82", "#374151"),
fg_color=("white", "#111827"), font=ctk.CTkFont(size=13)
        )
        self.entry_gestor_cargo.pack()

        botoes_gestor_frame = ctk.CTkFrame(input_area_gestor, fg_color="transparent")
        botoes_gestor_frame.pack(side=tk.RIGHT)

        self.btn_add_gestor = ctk.CTkButton(
            botoes_gestor_frame, text="Adicionar Gestor", width=180, height=38, corner_radius=10,
            fg_color=self.ACCENT_COLOR, hover_color="#1D4ED8", font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._adicionar_item_lista(
                self.entry_gestor, self.entry_gestor_cargo, self.scroll_gestores, self.gestores_adicionados, "gestores"
            )
        )
        self.btn_add_gestor.pack(pady=(24, 8))

        self.btn_usar_gestor = ctk.CTkButton(
            botoes_gestor_frame, text="↓ Usar salvo", width=180, height=34, corner_radius=10,
            fg_color=("#6B7280", "#4B5563"), hover_color=("#4B5563", "#374151"), font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self._abrir_popup_salvos(
                "gestores", self.entry_gestor, self.entry_gestor_cargo, self.scroll_gestores, self.gestores_adicionados
            )
        )
        self.btn_usar_gestor.pack()

        self.scroll_gestores = ctk.CTkScrollableFrame(
            self.frame_gestor,
            height=60, 
            corner_radius=10, fg_color=("gray95", "#111827"),
            border_width=1, border_color=("gray88", "#374151"), scrollbar_button_color=("#D1D5DB", "#4B5563"),
            scrollbar_button_hover_color=("#9CA3AF", "#6B7280"), scrollbar_fg_color="transparent"
        )
        self.scroll_gestores.pack(fill="x", padx=20, pady=(5, 20))
        self.scroll_gestores._scrollbar.grid_configure(padx=(0, 6))

        ctk.CTkLabel(
            self.container,
            text="Fiscais do Contrato",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).pack(anchor="w", padx=35, pady=(10, 4))

        ctk.CTkLabel(
            self.container,
            text="Registre os fiscais responsáveis pela fiscalização e pelo acompanhamento do processo.",
            font=ctk.CTkFont(size=13),
            text_color=self.SECTION_HELP_COLOR,
            wraplength=640,
            justify="left"
        ).pack(anchor="w", padx=35, pady=(0, 10))

        self.frame_fiscal = ctk.CTkFrame(
            self.container,
            height=250,
            fg_color=("gray98", "#0F172A"),
            corner_radius=14,
            border_width=1,
            border_color=("gray88", "#1E293B")
        )
        self.frame_fiscal.pack(fill="x", padx=35, pady=(0, 25))
        self.frame_fiscal.pack_propagate(False)

        input_area_fiscal = ctk.CTkFrame(self.frame_fiscal, fg_color="transparent")
        input_area_fiscal.pack(fill="x", padx=20, pady=(15, 5))

        entradas_fiscal_frame = ctk.CTkFrame(input_area_fiscal, fg_color="transparent")
        entradas_fiscal_frame.pack(side=tk.LEFT, fill="both", expand=True)

        bloco_nome_f = ctk.CTkFrame(entradas_fiscal_frame, fg_color="transparent")
        bloco_nome_f.pack(side=tk.LEFT, padx=(0, 15))
        ctk.CTkLabel(
            bloco_nome_f, text="Nome", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        self.entry_fiscal = ctk.CTkEntry(
            bloco_nome_f, width=280, height=38, corner_radius=10, border_width=1,
border_color=("gray82", "#374151"),
fg_color=("white", "#111827"), font=ctk.CTkFont(size=13)
        )
        self.entry_fiscal.pack()

        bloco_cargo_f = ctk.CTkFrame(entradas_fiscal_frame, fg_color="transparent")
        bloco_cargo_f.pack(side=tk.LEFT)
        ctk.CTkLabel(
            bloco_cargo_f, text="Cargo", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        self.entry_fiscal_cargo = ctk.CTkEntry(
            bloco_cargo_f, width=240, height=38, corner_radius=10, border_width=1,
            border_color=("gray82", "#374151"),
            fg_color=("white", "#111827"), font=ctk.CTkFont(size=13)
        )
        self.entry_fiscal_cargo.pack()

        botoes_fiscal_frame = ctk.CTkFrame(input_area_fiscal, fg_color="transparent")
        botoes_fiscal_frame.pack(side=tk.RIGHT)

        self.btn_add_fiscal = ctk.CTkButton(
            botoes_fiscal_frame, text="Adicionar Fiscal", width=180, height=38, corner_radius=10,
            fg_color=self.ACCENT_COLOR, hover_color="#1D4ED8", font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._adicionar_item_lista(
                self.entry_fiscal, self.entry_fiscal_cargo, self.scroll_fiscais, self.fiscais_adicionados, "fiscais"
            )
        )
        self.btn_add_fiscal.pack(pady=(24, 8))

        self.btn_usar_fiscal = ctk.CTkButton(
            botoes_fiscal_frame, text="↓ Usar salvo", width=180, height=34, corner_radius=10,
            fg_color=("#6B7280", "#4B5563"), hover_color=("#4B5563", "#374151"), font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self._abrir_popup_salvos(
                "fiscais", self.entry_fiscal, self.entry_fiscal_cargo, self.scroll_fiscais, self.fiscais_adicionados
            )
        )
        self.btn_usar_fiscal.pack()

        self.scroll_fiscais = ctk.CTkScrollableFrame(
            self.frame_fiscal,
            height=60,
            corner_radius=10, fg_color=("gray95", "#111827"),
            border_width=1, border_color=("gray88", "#374151"), scrollbar_button_color=("#D1D5DB", "#4B5563"),
            scrollbar_button_hover_color=("#9CA3AF", "#6B7280"), scrollbar_fg_color="transparent"
        )
        self.scroll_fiscais.pack(fill="x", padx=20, pady=(5, 20))
        self.scroll_fiscais._scrollbar.grid_configure(padx=(0, 6))

    def _adicionar_item_lista(self, entry_nome, entry_cargo, scroll, lista_adicionados, chave_dados):
        nome = entry_nome.get().strip()
        cargo = entry_cargo.get().strip()
        
        if not nome:
            return
            
        dados = {"nome": nome, "cargo": cargo}
        
        if any(d["nome"] == dados["nome"] and d["cargo"] == dados["cargo"] for d in lista_adicionados):
            return
            
        lista_adicionados.append(dados)
        self._renderizar_item(dados, scroll, lista_adicionados, chave_dados)
        
        entry_nome.delete(0, tk.END)
        entry_cargo.delete(0, tk.END)

    def _renderizar_item(self, dados, scroll, lista_adicionados, chave_dados, salvo=False):
        item = ctk.CTkFrame(
            scroll, corner_radius=6, fg_color=("white", "#0F172A"),
            border_width=1, border_color=("gray85", "#1F2937")
        )
        item.pack(fill="x", pady=2, padx=2)

        ctk.CTkLabel(
            item, text=f"{dados['nome']} — {dados['cargo']}",
            font=ctk.CTkFont(size=12), text_color=("gray15", "gray85")
        ).pack(side=tk.LEFT, padx=10, pady=6)

        btn_frame = ctk.CTkFrame(item, fg_color="transparent")
        btn_frame.pack(side=tk.RIGHT, padx=5)

        salvar_btn = ctk.CTkButton(
            btn_frame, text="✓ Salvo" if salvo else "Salvar",
            font=ctk.CTkFont(size=11, weight="bold"), width=60, height=24,
            corner_radius=6, fg_color="#6B7280" if salvo else "#10B981",
            state="disabled" if salvo else "normal"
        )
        salvar_btn.pack(side=tk.LEFT, padx=2)

        def ao_salvar(d=dados, btn=salvar_btn):
            self._salvar_individual(d, chave_dados)
            btn.configure(text="✓ Salvo", fg_color="#6B7280", state="disabled")

        if not salvo:
            salvar_btn.configure(command=ao_salvar)

        ctk.CTkButton(
            btn_frame, text="Remover", font=ctk.CTkFont(size=11, weight="bold"),
            width=65, height=24, corner_radius=6, fg_color="#DC2626",
            hover_color="#B91C1C", command=lambda w=item, d=dados: self._remover_item(w, d, lista_adicionados)
        ).pack(side=tk.LEFT, padx=2, pady=3)

    def _salvar_individual(self, dados, chave_dados):
        salvos = self.controller.dados_model.dados.setdefault(chave_dados, [])
        novo = {"nome": dados["nome"], "cargo": dados["cargo"]}
        tipo = "Gestor" if chave_dados == "gestores" else "Fiscal"

        existe = any(
            (
                isinstance(x, dict)
                and x.get("nome") == novo["nome"]
                and x.get("cargo") == novo["cargo"]
            )
            or
            (
                isinstance(x, str)
                and f"{novo['nome']} | {novo['cargo']}" == x
            )
            for x in salvos
        )

        if not existe:
            salvos.append(novo)
            if hasattr(self.controller.dados_model, "salvar"):
                self.controller.dados_model.salvar()
                
            messagebox.showinfo("Sucesso", f"{tipo} salvo com sucesso!")
        else:
            messagebox.showinfo("Info", f"Este {tipo.lower()} já está salvo.")

    def _remover_item(self, widget, dados, lista_adicionados):
        widget.destroy()
        if dados in lista_adicionados:
            lista_adicionados.remove(dados)

    def _abrir_popup_salvos(self, chave_dados, entry_nome, entry_cargo, scroll, lista_adicionados):
        dados_salvos = self.controller.dados_model.dados.get(chave_dados, [])
        lista_unica = []
        tipo = "gestor" if chave_dados == "gestores" else "fiscal"

        for d in dados_salvos:
            if isinstance(d, dict):
                lista_unica.append({"nome": d.get("nome", ""), "cargo": d.get("cargo", "")})
            elif isinstance(d, str) and "|" in d:
                nome, cargo = [x.strip() for x in d.split("|", 1)]
                lista_unica.append({"nome": nome, "cargo": cargo})

        if not lista_unica:
            messagebox.showinfo(f"{tipo.capitalize()}es salvos", f"Nenhum {tipo} salvo encontrado.")
            return

        width = 860
        height = 620
        
        root = self.winfo_toplevel()
        popup = tk.Toplevel(root)
        popup.title(f"Selecionar {tipo} salvo")
        popup.geometry(f"{width}x{height}")
        popup.resizable(False, False)
        popup.transient(root)
        popup.configure(bg="#111827" if ctk.get_appearance_mode() == "Dark" else "white")
        popup.withdraw()

        def fechar():
            popup.grab_release()
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", fechar)

        def centralizar_popup():
            self.update_idletasks()
            parent_x = root.winfo_rootx()
            parent_y = root.winfo_rooty()
            parent_w = root.winfo_width()
            parent_h = root.winfo_height()
            
            x = parent_x + (parent_w - width) // 2
            y = parent_y + (parent_h - height) // 2
            
            popup.geometry(f"{width}x{height}+{x}+{y}")
            popup.deiconify()
            popup.lift()
            popup.focus_force()
            popup.grab_set()

        popup.after(10, centralizar_popup)

        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "assets",
            "logo.ico"
        )

        if os.path.exists(icon_path):
            popup.after(
                200,
                lambda: popup.iconbitmap(icon_path)
            )

        popup.grab_set()

        card = ctk.CTkFrame(
            popup, corner_radius=0, fg_color=("white", "#111827")
        )
        card.pack(fill="both", expand=True)

        ctk.CTkLabel(
            card, text=f"Selecionar {tipo} salvo", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray15", "gray85")
        ).pack(anchor="w", padx=28, pady=(24, 4))

        ctk.CTkLabel(
            card, text=f"Escolha um {tipo} previamente salvo para preencher automaticamente.",
            font=ctk.CTkFont(size=13), text_color=("gray45", "gray65"), justify="left"
        ).pack(anchor="w", padx=28, pady=(0, 18))

        scroll_popup = ctk.CTkScrollableFrame(
            card, corner_radius=14, fg_color=("gray95", "#0F172A"),
            border_width=1, border_color=("gray88", "#1F2937")
        )
        scroll_popup.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        scroll_popup._scrollbar.grid_configure(padx=(0, 6))

        def usar(item):
            entry_nome.delete(0, tk.END)
            entry_cargo.delete(0, tk.END)
            entry_nome.insert(0, item.get("nome", ""))
            entry_cargo.insert(0, item.get("cargo", ""))
            self._adicionar_item_lista(entry_nome, entry_cargo, scroll, lista_adicionados, chave_dados)
            fechar()

        for d in lista_unica:
            row = ctk.CTkFrame(
                scroll_popup, corner_radius=12, fg_color=("gray90", "#1F2937"),
                border_width=1, border_color=("gray85", "#374151")
            )
            row.pack(fill="x", pady=5, padx=4)

            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(14, 8), pady=12)

            ctk.CTkLabel(
                info_frame, text=d.get("nome", "—"), font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w", text_color=("gray10", "gray90")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame, text=d.get("cargo", "—"), font=ctk.CTkFont(size=12),
                anchor="w", text_color=("gray40", "gray70")
            ).pack(anchor="w", pady=(2, 0))

            ctk.CTkButton(
                row, text="Usar", width=90, height=36, corner_radius=10,
                fg_color=self.ACCENT_COLOR, hover_color="#1D4ED8",
                font=ctk.CTkFont(size=12, weight="bold"), command=lambda i=d: usar(i)
            ).pack(side=tk.RIGHT, padx=14, pady=14)

    def coletar_dados(self):
        nomes_gestores = [g["nome"] for g in self.gestores_adicionados]
        cargos_gestores = [g["cargo"] for g in self.gestores_adicionados]
        nomes_fiscais = [f["nome"] for f in self.fiscais_adicionados]
        cargos_fiscais = [f["cargo"] for f in self.fiscais_adicionados]

        return {
            "{{GESTOR}}": ", ".join(nomes_gestores) if nomes_gestores else "[Não informado]",
            "{{GESTOR_CARGO}}": ", ".join(cargos_gestores) if cargos_gestores else "[Não informado]",
            "{{GESTORES}}": ", ".join(nomes_gestores) if nomes_gestores else "[Não informado]",
            "{{FISCAL}}": ", ".join(nomes_fiscais) if nomes_fiscais else "[Não informado]",
            "{{FISCAL_CARGO}}": ", ".join(cargos_fiscais) if cargos_fiscais else "[Não informado]",
            "{{FISCAIS}}": ", ".join(nomes_fiscais) if nomes_fiscais else "[Não informado]"
        }