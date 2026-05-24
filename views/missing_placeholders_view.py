import os
import customtkinter as ctk
from tkinter import messagebox


class MissingPlaceholdersDialog(ctk.CTkToplevel):
    def __init__(self, master, placeholders):
        super().__init__(master)
        self.title("Informações pendentes")

        width = 720
        height = 560
        parent = self.master
        try:
            parent.update_idletasks()
        except Exception:
            pass
        self.update_idletasks()
        try:
            p_x = parent.winfo_rootx()
            p_y = parent.winfo_rooty()
            p_w = parent.winfo_width()
            p_h = parent.winfo_height()
            if p_w <= 1 or p_h <= 1:
                screen_w = self.winfo_screenwidth()
                screen_h = self.winfo_screenheight()
                x = (screen_w // 2) - (width // 2)
                y = (screen_h // 2) - (height // 2)
            else:
                x = p_x + (p_w // 2) - (width // 2)
                y = p_y + (p_h // 2) - (height // 2)
        except Exception:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w // 2) - (width // 2)
            y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.minsize(640, 420)

        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "logo.ico"
        )
        if os.path.exists(icon_path):
            self.after(200, lambda: self.iconbitmap(icon_path))

        self.transient(master)
        self.grab_set()
        self.resultado = None
        self.entries = {}

        # FIX #2 — layout corrigido: scroll ocupa row=2 com weight, botões em
        # row=3 separado — antes ambos estavam em row=2, sobrepondo-se.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)   # scroll expande
        self.grid_rowconfigure(3, weight=0)   # botões fixos embaixo

        ctk.CTkLabel(
            self,
            text="Dados pendentes para completar os documentos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("gray15", "gray85")
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 6))

        ctk.CTkLabel(
            self,
            text=(
                "Preencha todos os campos abaixo para que os placeholders sejam "
                "substituídos corretamente no documento final."
            ),
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65"),
            wraplength=660,
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 12))

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=("white", "#111827"),
            corner_radius=18,
            border_width=1,
            border_color=("gray85", "#1F2937")
        )
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 8))
        self.scroll.grid_columnconfigure(0, weight=1)

        for i, chave in enumerate(placeholders):
            ctk.CTkLabel(
                self.scroll,
                text=chave,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("gray15", "gray85")
            ).grid(row=i * 2, column=0, sticky="w", pady=(12, 4), padx=16)
            campo = ctk.CTkTextbox(
                self.scroll,
                height=78,
                corner_radius=14,
                border_width=1,
                border_color=("gray80", "#374151"),
                font=ctk.CTkFont(size=13)
            )
            campo.grid(row=i * 2 + 1, column=0, sticky="ew", pady=(0, 10), padx=16)
            self.entries[chave] = campo

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.grid(row=3, column=0, sticky="e", padx=24, pady=(0, 22))

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            width=120,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray85"),
            command=self.cancelar,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes,
            text="Continuar",
            width=130,
            fg_color="#22C55E",
            hover_color="#16A34A",
            command=self.confirmar,
        ).pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.after(100, self._focar_primeiro)

    def _focar_primeiro(self):
        if self.entries:
            next(iter(self.entries.values())).focus_set()

    def confirmar(self):
        resultado = {}
        vazios = []
        for chave, campo in self.entries.items():
            valor = campo.get("0.0", "end").strip()
            if not valor:
                vazios.append(chave)
            else:
                resultado[chave] = valor
        if vazios:
            messagebox.showwarning(
                "Campos pendentes",
                "Preencha todos os campos antes de continuar:\n" + "\n".join(vazios),
                parent=self,
            )
            return
        self.resultado = resultado
        self.destroy()

    def cancelar(self):
        self.resultado = None
        self.destroy()
