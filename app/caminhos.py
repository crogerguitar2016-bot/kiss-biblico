# -*- coding: utf-8 -*-

from pathlib import Path
import os


# ======================================================
# RAIZ DO PROJETO
#
# Funciona no Termux/X11 e também dentro do APK.
# ======================================================

APP_DIR = Path(
    __file__
).resolve().parent

BASE = APP_DIR.parent

DATA_DIR = (
    BASE
    / "data"
)

ASSETS_DIR = (
    BASE
    / "assets"
)

IMAGENS_DIR = (
    ASSETS_DIR
    / "imagens"
)

QUIZ_JSON = (
    DATA_DIR
    / "quiz_biblico.json"
)

LOGO_KISS = (
    IMAGENS_DIR
    / "kiss_logo.png"
)


# ======================================================
# PASTA GRAVÁVEL
# ======================================================

def pasta_saves():

    # Permite sobrescrever durante testes.
    personalizada = os.environ.get(
        "KISS_SAVE_DIR"
    )

    if personalizada:

        caminho = Path(
            personalizada
        )

        caminho.mkdir(
            parents=True,
            exist_ok=True
        )

        return caminho


    # Dentro do Kivy/Android, usa o diretório
    # privado e gravável do aplicativo.

    try:

        from kivy.app import App

        app = App.get_running_app()

        if (
            app is not None
            and app.user_data_dir
        ):

            caminho = Path(
                app.user_data_dir
            )

            caminho.mkdir(
                parents=True,
                exist_ok=True
            )

            return caminho

    except Exception:
        pass


    # Termux / Ubuntu / testes.
    caminho = (
        BASE
        / "saves"
    )

    caminho.mkdir(
        parents=True,
        exist_ok=True
    )

    return caminho
