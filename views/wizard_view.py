import os
import traceback
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from views.prompt_view import PromptView
from views.steps.etapa_1_view import Etapa1View
from views.steps.etapa_2_view import Etapa2View
from views.steps.etapa_3_view import Etapa3View
from views.steps.etapa_4_view import Etapa4View
from views.steps.etapa_5_view import Etapa5View
from views.missing_placeholders_view import MissingPlaceholdersDialog

class WizardView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color=("gray92", "gray10"))
        self.controller = controller
        self.dev_signature = "@danih.morais"
        self.dados_cache = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(18, 8))
        self.header_frame.grid_columnconfigure(1, weight=1)

        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "logo.png"
        )
        if os.path.exists(logo_path):
            img_logo = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(44, 44)
            )
            self.lbl_logo = ctk.CTkLabel(self.header_frame, text="", image=img_logo)

        self.lbl_logo.grid(row=0, column=0, rowspan=2, sticky="nsw", padx=(0, 15))

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray15", "gray85"),
            padx=0, pady=0
        )
        self.lbl_titulo.grid(row=0, column=1, sticky="sw", pady=(4, 0))

        self.lbl_subtitulo = ctk.CTkLabel(
            self.header_frame,
            text="Forneça os dados do processo com clareza para gerar os artefatos corretamente.",
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65"),
            wraplength=640,
            justify="left"
        )
        self.lbl_subtitulo.grid(row=1, column=1, sticky="nw", pady=(1, 0))

        self.lbl_step = ctk.CTkLabel(
            self.header_frame,
            text="Passo 1 de 5",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray50", "gray60")
        )
        self.lbl_step.grid(row=0, column=2, sticky="e")

        self.seletor_tema = ctk.CTkSegmentedButton(
            self.header_frame,
            values=["Claro", "Escuro", "Auto"],
            command=self.mudar_tema
        )
        self.seletor_tema.grid(row=1, column=2, sticky="e", pady=(4, 0))

        tema_atual = self.controller.get_tema_atual()
        mapa_temas = {"Light": "Claro", "Dark": "Escuro", "System": "Auto"}
        self.seletor_tema.set(mapa_temas.get(tema_atual, "Auto"))

        container_padding = ctk.CTkFrame(self, fg_color="transparent")
        container_padding.grid(row=1, column=0, sticky="nsew", padx=40, pady=(0, 4))
        container_padding.grid_columnconfigure(0, weight=1)
        container_padding.grid_rowconfigure(0, weight=1)

        container_styled = ctk.CTkFrame(
            container_padding,
            corner_radius=24,
            fg_color="transparent",
            border_width=0,
            border_color=("gray85", "#1F2937")
        )
        container_styled.grid(row=0, column=0, sticky="nsew")
        container_styled.grid_columnconfigure(0, weight=1)
        container_styled.grid_rowconfigure(0, weight=1)

        self.container_etapas = ctk.CTkScrollableFrame(
            container_styled,
            fg_color="transparent",
            corner_radius=24,
            border_width=1,
            scrollbar_button_color=("#D1D5DB", "#374151"),
            scrollbar_button_hover_color=("#9CA3AF", "#4B5563"),
            scrollbar_fg_color="transparent"
        )
        self.container_etapas._scrollbar.grid_configure(padx=(0, 6))
        self.container_etapas.grid(row=0, column=0, sticky="nsew")
        self.container_etapas.grid_columnconfigure(0, weight=1)

        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=(8, 8))
        self.nav_frame.grid_columnconfigure(1, weight=1)

        self.btn_voltar = ctk.CTkButton(
            self.nav_frame,
            text="Voltar",
            width=140, height=44, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent", border_width=2,
            border_color=("gray70", "#374151"),
            text_color=("gray20", "gray80"),
            hover_color=("gray85", "gray20"),
            command=self.voltar
        )
        self.btn_voltar.grid(row=0, column=0, sticky="w")

        self.btn_avancar = ctk.CTkButton(
            self.nav_frame,
            text="Avançar",
            width=140, height=44, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.avancar
        )
        self.btn_avancar.grid(row=0, column=2, sticky="e")

        self.lbl_watermark = ctk.CTkLabel(
            self, text=self.dev_signature,
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray45")
        )
        self.lbl_watermark.grid(row=3, column=0, sticky="e", padx=40, pady=(0, 12))

        self.etapas = [
            Etapa1View(self.container_etapas, self.controller),
            Etapa2View(self.container_etapas, self.controller),
            Etapa3View(self.container_etapas, self.controller),
            Etapa4View(self.container_etapas, self.controller),
            Etapa5View(self.container_etapas, self.controller)
        ]

        self.etapa_atual = 0
        self.mostrar_etapa(0)

    def mudar_tema(self, valor):
        mapa_inverso = {"Claro": "Light", "Escuro": "Dark", "Auto": "System"}
        novo_tema = mapa_inverso.get(valor, "System")
        self.controller.alternar_tema(novo_tema)

    def mostrar_etapa(self, index):
        for frame in self.etapas:
            frame.grid_forget()
        self.etapas[index].grid(row=0, column=0, sticky="nsew")
        self.container_etapas._parent_canvas.yview_moveto(0)
        titulos = [
            "Etapa 1: Objeto e Justificativa",
            "Etapa 2: Condições de Execução",
            "Etapa 3: Unidade Demandante",
            "Etapa 4: Equipe de Planejamento",
            "Etapa 5: Definição do Instrumento",
            
        ]
        self.lbl_titulo.configure(text=titulos[index])
        self.lbl_step.configure(text=f"Passo {index + 1} de {len(self.etapas)}")
        self.btn_voltar.configure(state="normal" if index > 0 else "disabled")
        if index == len(self.etapas) - 1:
            self.btn_avancar.configure(text="Confeccionar", fg_color="#22C55E", hover_color="#16A34A")
        else:
            self.btn_avancar.configure(text="Avançar", fg_color="#2563EB", hover_color="#1D4ED8")

    def avancar(self):
        dados_etapa = self.etapas[self.etapa_atual].coletar_dados()
        if dados_etapa is None:
            return
        self.dados_cache.update(dados_etapa)

        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.mostrar_etapa(self.etapa_atual)
        else:
            self.confeccionar_documentos()

    def voltar(self):
        if self.etapa_atual > 0:
            self.etapa_atual -= 1
            self.mostrar_etapa(self.etapa_atual)

    def confeccionar_documentos(self):
        try:
            dados_usuario = self.dados_cache.copy()

            self.view = PromptView(self.master, dados_usuario)
            self.master.wait_window(self.view.janela)

            if self.view.resultado is not None:
                self.pack_forget()
                self.mostrar_tela_carregamento()

                dados_usuario["INSTRUCOES_EXTRAS"] = self.view.resultado
                meepp_exclusivo = (dados_usuario.get("{{ME_EPP}}") == "SIM")

                def on_error(msg):
                    if self.winfo_exists():
                        self.master.after(0, lambda: self._on_geracao_erro(msg))

                def on_success(dados_ia, dados_usu):
                    if self.winfo_exists():
                        self.master.after(0, lambda: self._on_geracao_sucesso(dados_ia, dados_usu))

                def on_progress(msg):
                    if (
                        self.winfo_exists()
                        and hasattr(self, "lbl_loading")
                        and self.lbl_loading.winfo_exists()
                    ):
                        self.master.after(0, lambda: self.lbl_loading.configure(text=msg))

                self.controller.executar_geracao(
                    dados_usuario, meepp_exclusivo,
                    on_progress, on_success, on_error
                )

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro ao Preparar Dados", f"Ocorreu um erro interno:\n{str(e)}")

    def mostrar_tela_carregamento(self):
        self.frame_loading = ctk.CTkFrame(self.master, fg_color=("gray92", "gray10"))
        self.frame_loading.pack(fill="both", expand=True)

        self.card_loading = ctk.CTkFrame(
            self.frame_loading,
            corner_radius=24,
            fg_color=("white", "#111827"),
            border_width=1,
            border_color=("gray85", "#1F2937"),
            width=950, height=350
        )
        self.card_loading.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.card_loading,
            text="Gerando Artefatos com IA",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray15", "gray85")
        ).pack(pady=(45, 15))

        self.lbl_loading = ctk.CTkLabel(
            self.card_loading,
            text="Iniciando...",
            font=ctk.CTkFont(size=14),
            text_color=("gray45", "gray65")
        )
        self.lbl_loading.pack(pady=5)

        self.progress = ctk.CTkProgressBar(
            self.card_loading,
            width=340, height=6,
            mode="indeterminate",
            progress_color="#2563EB"
        )
        self.progress.pack(pady=35)
        self.progress.start()

    def _on_geracao_erro(self, msg):
        if hasattr(self, "frame_loading") and self.frame_loading.winfo_exists():
            self.frame_loading.pack_forget()
        if hasattr(self, "progress") and self.progress.winfo_exists():
            self.progress.stop()
        messagebox.showerror(
            "Erro na Geração",
            f"Ocorreu um erro durante a geração:\n{msg}\n\nVocê pode revisar os dados e tentar novamente."
        )
        self.pack(fill="both", expand=True)

    def _on_geracao_sucesso(self, dados_ia, dados_usu):
        if hasattr(self, "frame_loading") and self.frame_loading.winfo_exists():
            self.frame_loading.pack_forget()
        if hasattr(self, "progress") and self.progress.winfo_exists():
            self.progress.stop()

        try:
            modificacoes = self.controller.montar_modificacoes_preliminares(dados_ia, dados_usu)
            pendentes = self.controller.placeholders_pendentes(modificacoes)
            preenchimentos_manuais = {}

            if pendentes:
                dialog = MissingPlaceholdersDialog(self.master, pendentes)
                self.master.wait_window(dialog)

                if dialog.resultado is None:
                    self.pack(fill="both", expand=True)
                    return

                preenchimentos_manuais = dialog.resultado

            pasta = self.controller.salvar_documentos(
                dados_ia,
                dados_usu,
                preenchimentos_manuais=preenchimentos_manuais
            )

            messagebox.showinfo(
                "Sucesso",
                f"Documentos confeccionados com sucesso!\nSalvos na pasta:\n{pasta}"
            )

            import os
            os.startfile(pasta)
            if hasattr(self, "dados_cache"):
                self.dados_cache.clear()
                self.dados_cache = {}

            self.pack(fill="both", expand=True)
            self.etapa_atual = 0
            self.mostrar_etapa(0)

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(
                "Erro ao Salvar",
                f"A IA processou os textos, mas houve um erro ao criar os arquivos DOCX:\n{str(e)}"
            )
            self.pack(fill="both", expand=True)