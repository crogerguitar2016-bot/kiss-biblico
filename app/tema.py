# -*- coding: utf-8 -*-

from pathlib import Path

from kivy.metrics import dp
from kivy.graphics import (
    Color,
    Rectangle,
    RoundedRectangle
)

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


# ======================================================
# CAMINHOS
# ======================================================

from app.caminhos import LOGO_KISS as CAMINHO_LOGO_KISS

LOGO_KISS = str(CAMINHO_LOGO_KISS)

# ======================================================
# PALETA OFICIAL KISS
# ======================================================

# Fundo azul-anil
ANIL = (
    0.10,
    0.17,
    0.52,
    1
)

# Azul mais escuro para profundidade
ANIL_ESCURO = (
    0.045,
    0.075,
    0.28,
    1
)

# Bege/dourado dos botões
BEGE = (
    0.66,
    0.48,
    0.25,
    1
)

# Bege mais claro para detalhes
BEGE_CLARO = (
    0.83,
    0.67,
    0.39,
    1
)

# Sombra do efeito 3D
BEGE_SOMBRA = (
    0.34,
    0.23,
    0.10,
    1
)

BRANCO = (
    1,
    1,
    1,
    1
)

BRANCO_SUAVE = (
    0.96,
    0.96,
    0.96,
    1
)

VERDE = (
    0.18,
    0.52,
    0.26,
    1
)

VERDE_SOMBRA = (
    0.08,
    0.28,
    0.12,
    1
)

VERMELHO = (
    0.65,
    0.16,
    0.15,
    1
)

VERMELHO_SOMBRA = (
    0.33,
    0.07,
    0.07,
    1
)

DOURADO_SELECIONADO = (
    0.88,
    0.66,
    0.25,
    1
)


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def escurecer(
    cor,
    fator=0.88
):

    return (
        cor[0] * fator,
        cor[1] * fator,
        cor[2] * fator,
        cor[3]
    )


# ======================================================
# FUNDO AZUL-ANIL
# ======================================================

def aplicar_fundo_anil(
    widget
):

    with widget.canvas.before:

        widget._cor_fundo_anil = Color(
            *ANIL
        )

        widget._fundo_anil = Rectangle(
            pos=widget.pos,
            size=widget.size
        )

    def atualizar(
        *args
    ):

        widget._fundo_anil.pos = (
            widget.pos
        )

        widget._fundo_anil.size = (
            widget.size
        )

    widget.bind(
        pos=atualizar,
        size=atualizar
    )


# ======================================================
# BOTÃO 3D OFICIAL
# ======================================================

class Botao3D(Button):

    def __init__(
        self,
        cor=BEGE,
        cor_sombra=BEGE_SOMBRA,
        raio=16,
        **kwargs
    ):

        kwargs.setdefault(
            "background_normal",
            ""
        )

        kwargs.setdefault(
            "background_down",
            ""
        )

        kwargs.setdefault(
            "background_color",
            (
                0,
                0,
                0,
                0
            )
        )

        kwargs.setdefault(
            "color",
            BRANCO
        )

        kwargs.setdefault(
            "disabled_color",
            BRANCO
        )

        kwargs.setdefault(
            "font_size",
            "16sp"
        )

        kwargs.setdefault(
            "bold",
            True
        )

        super().__init__(
            **kwargs
        )

        self.cor_base = tuple(
            cor
        )

        self.cor_sombra = tuple(
            cor_sombra
        )

        self.raio_3d = raio


        with self.canvas.before:

            self._cor_sombra = Color(
                *self.cor_sombra
            )

            self._sombra = (
                RoundedRectangle(
                    pos=(
                        self.x,
                        self.y - dp(5)
                    ),

                    size=self.size,

                    radius=[
                        dp(
                            self.raio_3d
                        )
                    ]
                )
            )


            self._cor_frente = Color(
                *self.cor_base
            )

            self._frente = (
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,

                    radius=[
                        dp(
                            self.raio_3d
                        )
                    ]
                )
            )


        self.bind(
            pos=self._atualizar_3d,
            size=self._atualizar_3d,
            state=self._alterar_estado
        )


    def _atualizar_3d(
        self,
        *args
    ):

        self._sombra.pos = (
            self.x,
            self.y - dp(5)
        )

        self._sombra.size = (
            self.size
        )

        self._frente.pos = (
            self.pos
        )

        self._frente.size = (
            self.size
        )


    def _alterar_estado(
        self,
        *args
    ):

        if self.state == "down":

            self._cor_frente.rgba = (
                escurecer(
                    self.cor_base,
                    0.84
                )
            )

        else:

            self._cor_frente.rgba = (
                self.cor_base
            )


    def definir_cor(
        self,
        cor,
        cor_sombra=None
    ):

        self.cor_base = tuple(
            cor
        )

        if cor_sombra is not None:

            self.cor_sombra = tuple(
                cor_sombra
            )

            self._cor_sombra.rgba = (
                self.cor_sombra
            )

        self._cor_frente.rgba = (
            self.cor_base
        )


    def normal(self):

        self.definir_cor(
            BEGE,
            BEGE_SOMBRA
        )


    def selecionado(self):

        self.definir_cor(
            DOURADO_SELECIONADO,
            BEGE_SOMBRA
        )


    def correto(self):

        self.definir_cor(
            VERDE,
            VERDE_SOMBRA
        )


    def errado(self):

        self.definir_cor(
            VERMELHO,
            VERMELHO_SOMBRA
        )


# ======================================================
# PAINEL / QUADRADO 3D
# ======================================================

class Bloco3D(BoxLayout):

    def __init__(
        self,
        cor=BEGE,
        cor_sombra=BEGE_SOMBRA,
        raio=16,
        **kwargs
    ):

        super().__init__(
            **kwargs
        )

        self.cor_base = tuple(
            cor
        )

        self.cor_sombra = tuple(
            cor_sombra
        )

        self.raio_3d = raio


        with self.canvas.before:

            self._cor_sombra = Color(
                *self.cor_sombra
            )

            self._sombra = (
                RoundedRectangle(
                    pos=(
                        self.x,
                        self.y - dp(5)
                    ),

                    size=self.size,

                    radius=[
                        dp(
                            self.raio_3d
                        )
                    ]
                )
            )


            self._cor_frente = Color(
                *self.cor_base
            )

            self._frente = (
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,

                    radius=[
                        dp(
                            self.raio_3d
                        )
                    ]
                )
            )


        self.bind(
            pos=self._atualizar_3d,
            size=self._atualizar_3d
        )


    def _atualizar_3d(
        self,
        *args
    ):

        self._sombra.pos = (
            self.x,
            self.y - dp(5)
        )

        self._sombra.size = (
            self.size
        )

        self._frente.pos = (
            self.pos
        )

        self._frente.size = (
            self.size
        )


# ======================================================
# CAMPO DO NOME DO JOGADOR
# ======================================================

class CampoNome3D(TextInput):

    def __init__(
        self,
        **kwargs
    ):

        kwargs.setdefault(
            "multiline",
            False
        )

        kwargs.setdefault(
            "background_normal",
            ""
        )

        kwargs.setdefault(
            "background_active",
            ""
        )

        kwargs.setdefault(
            "background_color",
            (
                0,
                0,
                0,
                0
            )
        )

        kwargs.setdefault(
            "foreground_color",
            BRANCO
        )

        kwargs.setdefault(
            "hint_text_color",
            (
                1,
                1,
                1,
                0.70
            )
        )

        kwargs.setdefault(
            "cursor_color",
            BRANCO
        )

        kwargs.setdefault(
            "font_size",
            "18sp"
        )

        super().__init__(
            **kwargs
        )


        with self.canvas.before:

            self._campo_sombra_cor = Color(
                *BEGE_SOMBRA
            )

            self._campo_sombra = (
                RoundedRectangle(
                    pos=(
                        self.x,
                        self.y - dp(4)
                    ),

                    size=self.size,

                    radius=[
                        dp(14)
                    ]
                )
            )


            self._campo_cor = Color(
                *BEGE
            )

            self._campo_frente = (
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,

                    radius=[
                        dp(14)
                    ]
                )
            )


        self.bind(
            pos=self._atualizar,
            size=self._atualizar
        )


    def _atualizar(
        self,
        *args
    ):

        self._campo_sombra.pos = (
            self.x,
            self.y - dp(4)
        )

        self._campo_sombra.size = (
            self.size
        )

        self._campo_frente.pos = (
            self.pos
        )

        self._campo_frente.size = (
            self.size
        )


# ======================================================
# LOGO OFICIAL K / KISS
# ======================================================

def criar_logo(
    altura=200
):

    return Image(
        source=LOGO_KISS,

        size_hint_y=None,

        height=dp(
            altura
        ),

        fit_mode="contain"
    )
