# -*- coding: utf-8 -*-

import json


from app.caminhos import QUIZ_JSON

ARQUIVO_JSON = QUIZ_JSON


class MotorQuiz:

    def __init__(self):

        with ARQUIVO_JSON.open(
            "r",
            encoding="utf-8"
        ) as f:
            self.banco = json.load(f)

        self.livro_atual = None
        self.indice_pergunta = 0

        self.resposta_selecionada = None
        self.resposta_confirmada = False

        self.acertos = 0
        self.erros = 0


    def listar_livros(self):

        return [
            livro["nome"]
            for livro in self.banco["livros"]
        ]


    def abrir_livro(self, nome):

        for livro in self.banco["livros"]:

            if livro["nome"] == nome:

                self.livro_atual = livro
                self.indice_pergunta = 0

                self.resposta_selecionada = None
                self.resposta_confirmada = False

                self.acertos = 0
                self.erros = 0

                return True

        return False


    def pergunta_atual(self):

        if self.livro_atual is None:
            return None

        perguntas = self.livro_atual[
            "perguntas"
        ]

        if self.indice_pergunta >= len(
            perguntas
        ):
            return None

        return perguntas[
            self.indice_pergunta
        ]


    def selecionar_resposta(self, letra):

        letra = letra.upper().strip()

        if letra not in {
            "A", "B", "C", "D"
        }:
            raise ValueError(
                "Resposta deve ser A, B, C ou D."
            )

        if self.resposta_confirmada:
            raise RuntimeError(
                "A resposta desta pergunta "
                "já foi confirmada."
            )

        self.resposta_selecionada = letra

        return {
            "estado": "aguardando_confirmacao",
            "pergunta":
                "Deseja mudar sua resposta?",
            "opcoes": [
                "SIM",
                "NÃO"
            ]
        }


    def decidir_mudar(self, decisao):

        if self.resposta_selecionada is None:

            raise RuntimeError(
                "Nenhuma resposta foi selecionada."
            )

        if self.resposta_confirmada:

            raise RuntimeError(
                "A resposta já foi confirmada."
            )

        decisao = (
            decisao
            .strip()
            .casefold()
        )

        if decisao in {
            "sim",
            "s"
        }:

            resposta_anterior = (
                self.resposta_selecionada
            )

            self.resposta_selecionada = None

            return {
                "estado": "mudar_resposta",
                "resposta_anterior":
                    resposta_anterior,
                "mensagem":
                    "Escolha outra alternativa."
            }

        if decisao not in {
            "não",
            "nao",
            "n"
        }:

            raise ValueError(
                "Use SIM ou NÃO."
            )

        pergunta = self.pergunta_atual()

        correta = pergunta["correta"]

        escolhida = self.resposta_selecionada

        acertou = (
            escolhida == correta
        )

        self.resposta_confirmada = True

        if acertou:
            self.acertos += 1
        else:
            self.erros += 1

        return {
            "estado": "confirmada",
            "acertou": acertou,
            "escolhida": escolhida,
            "correta": correta,
            "resposta_correta":
                pergunta[
                    "resposta_correta"
                ],
            "dica":
                pergunta["dica"]
        }


    def proxima_pergunta(self):

        if not self.resposta_confirmada:

            raise RuntimeError(
                "Confirme a resposta atual "
                "antes de avançar."
            )

        self.indice_pergunta += 1

        self.resposta_selecionada = None
        self.resposta_confirmada = False

        if self.pergunta_atual() is None:

            return {
                "estado": "livro_concluido",
                "acertos": self.acertos,
                "erros": self.erros,
                "total":
                    self.acertos
                    + self.erros
            }

        return {
            "estado": "proxima_pergunta",
            "numero":
                self.pergunta_atual()[
                    "numero"
                ]
        }


    def progresso_livro(self):

        if self.livro_atual is None:
            return None

        total = len(
            self.livro_atual[
                "perguntas"
            ]
        )

        respondidas = (
            self.acertos
            + self.erros
        )

        return {
            "livro":
                self.livro_atual[
                    "nome"
                ],
            "respondidas":
                respondidas,
            "total":
                total,
            "acertos":
                self.acertos,
            "erros":
                self.erros
        }
