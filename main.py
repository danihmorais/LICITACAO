import ctypes
import json
import os
import sys
import threading
import time

import customtkinter as ctk

from controllers.app_controller import AppController
from updater import (
    verificar_e_atualizar,
    perguntar_atualizacao,
    executar_modo_update,
)

import config


def checar_update_background(app_root):
    try:
        data = verificar_e_atualizar()

        if not data:
            return

        app_root.after(
            0,
            lambda: perguntar_atualizacao(data)
        )

    except Exception:
        pass


if __name__ == "__main__":

    if "--apply-update" in sys.argv:
        executar_modo_update()
        sys.exit()

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    tema_salvo = "System"

    if os.path.exists(config.ARQUIVO_DADOS):
        try:
            with open(config.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                tema_salvo = dados.get("tema", "System")
        except Exception:
            pass

    ctk.set_appearance_mode(tema_salvo)
    ctk.set_default_color_theme("blue")

    app = AppController()

    threading.Thread(
        target=lambda: (
            time.sleep(2),
            checar_update_background(app.app)
        ),
        daemon=True
    ).start()

    app.iniciar()