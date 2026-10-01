# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import date, datetime
import hashlib
import json
import random


from app.caminhos import pasta_saves, QUIZ_JSON

BANCO_QUIZ = QUIZ_JSON

class DesafioDiario:

    QUANTIDADE = 10

    def __init__(
        self,
        arquivo=None
    ):

        self.arquivo = (
            Path(arquivo)
            if arquivo is not None
            else (
                pasta_saves()
                / "desafio_diario.json"
            )
        )

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.banco = (
            self._carregar_banco()
        )

        self.indice = {}

        self.referencias = []

        for livro in self.banco[
            "livros"
        ]:

            nome = livro[
                "nome"
            ]

            for pergunta in livro[
                "perguntas"
            ]:

                numero = pergunta[
                    "numero"
                ]

                chave = (
                    nome,
                    numero
                )

                self.indice[
                    chave
                ] = pergunta

                self.referencias.append(
                    chave
                )

        self.dados = (
            self._carregar()
        )


    # ==================================================
    # BANCO
    # ==================================================

    def _carregar_banco(self):

        if not BANCO_QUIZ.exists():

            raise RuntimeError(
                "quiz_biblico.json "
                "não encontrado."
            )

        with BANCO_QUIZ.open(
            "r",
            encoding="utf-8"
        ) as arquivo:

            banco = json.load(
                arquivo
            )

        return banco


    # ==================================================
    # DATA
    # ==================================================

    @staticmethod
    def _normalizar_data(
        valor=None
    ):

        if valor is None:

            return date.today()


        if isinstance(
            valor,
            datetime
        ):

            return valor.date()


        if isinstance(
            valor,
            date
        ):

            return valor


        if isinstance(
            valor,
            str
        ):

            return date.fromisoformat(
                valor
            )


        raise ValueError(
            "Data inválida."
        )


    # ==================================================
    # SAVE
    # ==================================================

    def _modelo_vazio(self):

        return {
            "versao": 1,
            "conclusoes": {}
        }


    def _carregar(self):

        if not self.arquivo.exists():

            dados = (
                self._modelo_vazio()
            )

            self._salvar_dados(
                dados
            )

            return dados


        try:

            with self.arquivo.open(
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(
                    arquivo
                )


            if not isinstance(
                dados,
                dict
            ):

                dados = {}


            dados.setdefault(
                "versao",
                1
            )

            dados.setdefault(
                "conclusoes",
                {}
            )


            if not isinstance(
                dados["conclusoes"],
                dict
            ):

                dados[
                    "conclusoes"
                ] = {}


            return dados


        except Exception:

            corrompido = (
                self.arquivo.with_name(
                    self.arquivo.stem
                    + "_CORROMPIDO"
                    + self.arquivo.suffix
                )
            )

            try:

                self.arquivo.replace(
                    corrompido
                )

            except Exception:
                pass


            dados = (
                self._modelo_vazio()
            )

            self._salvar_dados(
                dados
            )

            return dados


    def _salvar_dados(
        self,
        dados
    ):

        temporario = (
            self.arquivo.with_name(
                self.arquivo.name
                + ".tmp"
            )
        )

        temporario.write_text(
            json.dumps(
                dados,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        temporario.replace(
            self.arquivo
        )


    def salvar(self):

        self._salvar_dados(
            self.dados
        )


    # ==================================================
    # GERAR AS 10 PERGUNTAS DO DIA
    # ==================================================

    def perguntas_do_dia(
        self,
        data_referencia=None
    ):

        dia = (
            self._normalizar_data(
                data_referencia
            )
        )

        texto_data = (
            dia.isoformat()
        )


        # SHA-256 garante que a mesma data
        # gere sempre a mesma semente,
        # mesmo fechando o aplicativo.

        digest = hashlib.sha256(
            texto_data.encode(
                "utf-8"
            )
        ).digest()


        semente = int.from_bytes(
            digest[:8],
            byteorder="big",
            signed=False
        )


        gerador = random.Random(
            semente
        )


        escolhidas = gerador.sample(
            self.referencias,
            self.QUANTIDADE
        )


        resultado = []


        for livro, numero in escolhidas:

            original = (
                self.indice[
                    (
                        livro,
                        numero
                    )
                ]
            )


            pergunta = dict(
                original
            )


            pergunta[
                "alternativas"
            ] = dict(
                original[
                    "alternativas"
                ]
            )


            pergunta[
                "livro"
            ] = livro


            resultado.append(
                pergunta
            )


        return resultado


    # ==================================================
    # CONCLUSÃO
    # ==================================================

    def registrar_conclusao(
        self,
        acertos,
        data_referencia=None
    ):

        if not isinstance(
            acertos,
            int
        ):

            raise ValueError(
                "Quantidade de acertos inválida."
            )


        if not 0 <= acertos <= 10:

            raise ValueError(
                "Acertos do desafio devem "
                "estar entre 0 e 10."
            )


        dia = (
            self._normalizar_data(
                data_referencia
            )
        )

        chave = (
            dia.isoformat()
        )


        conclusoes = (
            self.dados[
                "conclusoes"
            ]
        )


        # Se já foi concluído naquele dia,
        # não duplicamos o registro.

        if chave in conclusoes:

            existente = dict(
                conclusoes[
                    chave
                ]
            )

            existente[
                "ja_concluido"
            ] = True

            return existente


        percentual = round(
            (
                acertos
                / self.QUANTIDADE
            )
            * 100,
            1
        )


        registro = {
            "data":
                chave,

            "acertos":
                acertos,

            "erros":
                self.QUANTIDADE
                - acertos,

            "total":
                self.QUANTIDADE,

            "percentual":
                percentual
        }


        conclusoes[
            chave
        ] = registro


        self.salvar()


        retorno = dict(
            registro
        )

        retorno[
            "ja_concluido"
        ] = False


        return retorno


    # ==================================================
    # JÁ CONCLUIU HOJE?
    # ==================================================

    def concluido_em(
        self,
        data_referencia=None
    ):

        dia = (
            self._normalizar_data(
                data_referencia
            )
        )

        return (
            dia.isoformat()
            in self.dados[
                "conclusoes"
            ]
        )


    # ==================================================
    # RESUMO
    # ==================================================

    def resumo(self):

        conclusoes = list(
            self.dados[
                "conclusoes"
            ].values()
        )


        total = len(
            conclusoes
        )


        if total == 0:

            return {
                "dias_concluidos": 0,
                "melhor_acertos": 0,
                "media_acertos": 0.0,
                "media_percentual": 0.0
            }


        melhor = max(
            item[
                "acertos"
            ]
            for item in conclusoes
        )


        soma_acertos = sum(
            item[
                "acertos"
            ]
            for item in conclusoes
        )


        media_acertos = round(
            soma_acertos
            / total,
            1
        )


        media_percentual = round(
            (
                soma_acertos
                / (
                    total
                    * self.QUANTIDADE
                )
            )
            * 100,
            1
        )


        return {
            "dias_concluidos":
                total,

            "melhor_acertos":
                melhor,

            "media_acertos":
                media_acertos,

            "media_percentual":
                media_percentual
        }
