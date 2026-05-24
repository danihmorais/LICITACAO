import customtkinter as ctk
from tkinter import messagebox
import os
import tkinter as tk

import config


class Etapa3View(ctk.CTkFrame):
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
            text="Secretarias Demandantes",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.SECTION_TITLE_COLOR
        ).pack(anchor="w", padx=35, pady=(25, 8))

        ctk.CTkLabel(
            self.container,
            text="Escolha as unidades demandantes e registre os contatos responsáveis por cada uma.",
            font=ctk.CTkFont(size=13),
            text_color=self.SECTION_HELP_COLOR,
            wraplength=640,
            justify="left"
        ).pack(anchor="w", padx=35, pady=(0, 12))

        self.scroll_sec = ctk.CTkScrollableFrame(
            self.container,
            height=230,
            corner_radius=14,
            fg_color=("gray95", "#1F2937"),
            border_width=1,
            border_color=("gray90", "#374151"),
            scrollbar_button_color=("#D1D5DB", "#4B5563"),
            scrollbar_button_hover_color=("#9CA3AF", "#6B7280"),
            scrollbar_fg_color="transparent"
        )
        self.scroll_sec.pack(fill="x", padx=35, pady=(0, 12))
        self.scroll_sec._scrollbar.grid_configure(padx=(0, 6))

        self.check_secretarias = {}

        for sec in config.SECRETARIAS_DEFAULT:
            var = ctk.BooleanVar(value=False)

            chk = ctk.CTkCheckBox(
                self.scroll_sec,
                text=sec,
                font=ctk.CTkFont(size=13),
                variable=var,
                command=self.atualizar_campos_contato,
                border_width=1
            )

            chk.pack(anchor="w", pady=2, padx=12)

            self.check_secretarias[sec] = var

        ctk.CTkLabel(
            self.container,
            text="Dados de Contato por Secretaria",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray15", "gray85")
        ).pack(anchor="w", padx=35, pady=(8, 8))

        self.scroll_contatos = ctk.CTkScrollableFrame(
            self.container,
            height=230,
            corner_radius=14,
            fg_color=("gray95", "#1F2937"),
            border_width=1,
            border_color=("gray90", "#374151"),
            scrollbar_button_color=("#D1D5DB", "#4B5563"),
            scrollbar_button_hover_color=("#9CA3AF", "#6B7280"),
            scrollbar_fg_color="transparent"
        )

        self.scroll_contatos.pack(fill="x", padx=35, pady=(0, 20))
        self.scroll_contatos._scrollbar.grid_configure(padx=(0, 6))

        self.contatos_adicionados = {}
        self.entradas_contato = {}

    def atualizar_campos_contato(self):
        rascunhos = {}
        for sec, campos in self.entradas_contato.items():
            rascunhos[sec] = {
                "email": campos["email"].get(),
                "tel":   campos["tel"].get(),
            }

        for widget in self.scroll_contatos.winfo_children():
            widget.destroy()

        self.entradas_contato.clear()

        contatos_salvos = self.controller.dados_model.dados.get(
            "contatos_secretarias", {}
        )

        for sec, var in self.check_secretarias.items():
            if var.get():
                self._criar_campo_contato(sec, contatos_salvos)

                if sec in rascunhos:
                    self.entradas_contato[sec]["email"].insert(0, rascunhos[sec]["email"])
                    self.entradas_contato[sec]["tel"].insert(0, rascunhos[sec]["tel"])

    def _criar_campo_contato(self, sec, contatos_salvos):
        frame_sec = ctk.CTkFrame(
            self.scroll_contatos,
            corner_radius=12,
            fg_color=("white", "#111827"),
            border_width=1,
            border_color=("gray85", "#374151")
        )

        frame_sec.pack(fill="x", pady=6, padx=8)
        frame_sec.pack_propagate(False)
        frame_sec.configure(height=200)

        header_frame = ctk.CTkFrame(frame_sec, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            header_frame,
            text=sec,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("gray15", "gray85")
        ).pack(side="left", padx=(0, 15))

        entry_email = ctk.CTkEntry(
            header_frame,
            width=180,
            height=30,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(size=11),
            placeholder_text="E-mail"
        )
        entry_email.pack(side="left", padx=(0, 6))

        entry_tel = ctk.CTkEntry(
            header_frame,
            width=120,
            height=30,
            corner_radius=8,
            border_width=1,
            font=ctk.CTkFont(size=11),
            placeholder_text="Telefone"
        )
        entry_tel.pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            header_frame,
            text="+ Adicionar",
            width=100,
            height=30,
            corner_radius=8,
            fg_color=self.ACCENT_COLOR,
            hover_color="#1D4ED8",
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda s=sec, e=entry_email, t=entry_tel:
                self.adicionar_contato_lista(s, e, t)
        ).pack(side="left")

        ctk.CTkButton(
            header_frame,
            text="↓ Usar salvo",
            width=90,
            height=30,
            corner_radius=8,
            fg_color=("#6B7280", "#4B5563"),
            hover_color=("#4B5563", "#374151"),
            font=ctk.CTkFont(size=10, weight="bold"),
            command=lambda s=sec: self._abrir_popup_contatos_salvos(s)
        ).pack(side="left", padx=(4, 0))

        scroll_contatos_list = ctk.CTkScrollableFrame(
            frame_sec,
            height=60,
            corner_radius=8,
            fg_color=("gray92", "#0F172A"),
            border_width=1,
            border_color=("gray88", "#1F2937"),
            scrollbar_button_color=("#D1D5DB", "#4B5563"),
            scrollbar_button_hover_color=("#9CA3AF", "#6B7280"),
            scrollbar_fg_color="transparent"
        )
        scroll_contatos_list.pack(fill="x", padx=12, pady=(4, 10))
        scroll_contatos_list._scrollbar.grid_configure(padx=(0, 4))

        self.entradas_contato[sec] = {
            "email":       entry_email,
            "tel":         entry_tel,
            "scroll_list": scroll_contatos_list,
        }

        if sec not in self.contatos_adicionados:
            self.contatos_adicionados[sec] = []

        for dados in self.contatos_adicionados[sec]:
            self._renderizar_item_contato(sec, dados, scroll_contatos_list, salvo=False)
    
    def _abrir_popup_contatos_salvos(self, sec):
        todos_salvos = self.controller.dados_model.dados.get(
            "contatos_secretarias", {}
        )

        lista_unica = todos_salvos.get(sec, [])

        if not lista_unica:
            messagebox.showinfo(
                "Contatos salvos",
                "Nenhum contato salvo encontrado."
            )
            return

        width = 860
        height = 620

        popup = tk.Toplevel(self)
        popup.title("Selecionar contato salvo")
        popup.resizable(False, False)
        popup.withdraw()
        popup.configure(bg="#EDEDED")

        def centralizar_popup():

            self.update_idletasks()

            parent_x = self.winfo_rootx()
            parent_y = self.winfo_rooty()
            parent_w = self.winfo_width()
            parent_h = self.winfo_height()

            x = parent_x + (parent_w - width) // 2
            y = parent_y + (parent_h - height) // 2

            popup.geometry(f"{width}x{height}+{x}+{y}")
            popup.deiconify()

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
            popup,
            corner_radius=24,
            fg_color=("white", "#111827"),
            border_width=1,
            border_color=("gray85", "#1F2937")
        )

        card.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=14
        )

        ctk.CTkLabel(
            card,
            text="Selecionar contato salvo",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray15", "gray85")
        ).pack(
            anchor="w",
            padx=28,
            pady=(24, 4)
        )

        subtitulo_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        subtitulo_frame.pack(
            fill="x",
            padx=28,
            pady=(0, 18)
        )

        ctk.CTkLabel(
            subtitulo_frame,
            text=(
                "Escolha um contato previamente salvo "
                "para preencher automaticamente."
            ),
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65"),
            justify="left",
            anchor="w"
        ).pack(
            anchor="w"
        )

        scroll = ctk.CTkScrollableFrame(
            card,
            corner_radius=14,
            fg_color=("gray95", "#0F172A"),
            border_width=1,
            border_color=("gray88", "#1F2937")
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 22)
        )

        scroll._scrollbar.grid_configure(padx=(0, 6))

        def usar(contato):
            entry_e = self.entradas_contato[sec]["email"]
            entry_t = self.entradas_contato[sec]["tel"]

            entry_e.delete(0, "end")
            entry_t.delete(0, "end")

            entry_e.insert(0, contato.get("email", ""))
            entry_t.insert(0, contato.get("tel", ""))

            self.adicionar_contato_lista(
                sec,
                entry_e,
                entry_t
            )
            
            popup.destroy()

        for c in lista_unica:

            row = ctk.CTkFrame(
                scroll,
                corner_radius=12,
                fg_color=("gray90", "#1F2937"),
                border_width=1,
                border_color=("gray85", "#374151")
            )

            row.pack(
                fill="x",
                pady=5,
                padx=4
            )

            info_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            info_frame.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(14, 8),
                pady=12
            )

            ctk.CTkLabel(
                info_frame,
                text=c.get("email", "—"),
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color=("gray10", "gray90")
            ).pack(anchor="w")

            ctk.CTkLabel(
                info_frame,
                text=c.get("tel", "—"),
                font=ctk.CTkFont(size=12),
                anchor="w",
                text_color=("gray40", "gray70")
            ).pack(anchor="w", pady=(2, 0))

            ctk.CTkButton(
                row,
                text="Usar",
                width=90,
                height=36,
                corner_radius=10,
                fg_color=self.ACCENT_COLOR,
                hover_color="#1D4ED8",
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda c=c: usar(c)
            ).pack(
                side="right",
                padx=14,
                pady=14
            )

    def adicionar_contato_lista(self, sec, entry_email, entry_tel):
        email = entry_email.get().strip()
        telefone = entry_tel.get().strip()

        if not email and not telefone:
            return

        dados = {"email": email, "tel": telefone}

        self.contatos_adicionados[sec].append(dados)

        scroll_list = self.entradas_contato[sec]["scroll_list"]
        self._renderizar_item_contato(sec, dados, scroll_list, salvo=False)

        entry_email.delete(0, "end")
        entry_tel.delete(0, "end")

    # ------------------------------------------------------------------
    # Extrai a renderização de um item para poder reusar ao recriar widgets
    # ------------------------------------------------------------------
    def _renderizar_item_contato(self, sec, dados, scroll_list, salvo=False):
        item = ctk.CTkFrame(
            scroll_list,
            corner_radius=6,
            fg_color=("white", "#0F172A"),
            border_width=1,
            border_color=("gray85", "#1F2937")
        )
        item.pack(fill="x", pady=1, padx=2)

        ctk.CTkLabel(
            item,
            text=f"{dados['email']} — {dados['tel']}",
            font=ctk.CTkFont(size=11),
            text_color=("gray15", "gray85")
        ).pack(side="left", padx=6, pady=4)

        btn_frame = ctk.CTkFrame(item, fg_color="transparent")
        btn_frame.pack(side="right", padx=5)

        salvar_btn = ctk.CTkButton(
            btn_frame,
            text="✓ Salvo" if salvo else "Salvar",
            font=ctk.CTkFont(size=10, weight="bold"),
            width=55,
            height=22,
            corner_radius=5,
            fg_color="#6B7280" if salvo else "#10B981",
            state="disabled" if salvo else "normal",
        )
        salvar_btn.pack(side="left", padx=1)

        def ao_salvar(d=dados, w=item, s=sec, btn=salvar_btn):
            self.salvar_contato_individual(s, d)
            # Apenas atualiza aparência — não destrói o widget
            btn.configure(text="✓ Salvo", fg_color="#6B7280", state="disabled")

        if not salvo:
            salvar_btn.configure(command=ao_salvar)

        ctk.CTkButton(
            btn_frame,
            text="Remover",
            font=ctk.CTkFont(size=10, weight="bold"),
            width=60,
            height=22,
            corner_radius=5,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=lambda w=item, d=dados, s=sec:
                self.remover_contato(s, w, d)
        ).pack(side="left", padx=1, pady=2)

    def salvar_contato_individual(self, secretaria, dados):
        contatos = self.controller.dados_model.dados.setdefault(
            "contatos_secretarias", {}
        )
        lista = contatos.setdefault(secretaria, [])

        novo = {"email": dados["email"], "tel": dados["tel"]}

        existe = any(
            c.get("email") == novo["email"] and c.get("tel") == novo["tel"]
            for c in lista
        )

        if not existe:
            lista.append(novo)

            if hasattr(self.controller.dados_model, "salvar"):
                self.controller.dados_model.salvar()

            messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")
        else:
            messagebox.showinfo("Info", "Este contato já está salvo.")

    def remover_contato(self, secretaria, widget, dados):
        widget.destroy()

        if dados in self.contatos_adicionados[secretaria]:
            self.contatos_adicionados[secretaria].remove(dados)

    def coletar_dados(self):
        secretarias = [
            sec for sec, var in self.check_secretarias.items()
            if var.get()
        ]

        emails = []
        telefones = []

        for sec in secretarias:
            for contato in self.contatos_adicionados.get(sec, []):
                if contato.get("email"):
                    emails.append(contato["email"])
                if contato.get("tel"):
                    telefones.append(contato["tel"])

        return {
            "{{SECRETARIA}}":
                ", ".join(secretarias) if secretarias else "Não especificada",
            "{{EMAIL_SEC}}":
                ", ".join(emails) if emails else "[E-mail não informado]",
            "{{TELEFONE_SEC}}":
                ", ".join(telefones) if telefones else "[Telefone não informado]",
        }