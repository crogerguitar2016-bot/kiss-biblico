# -*- coding: utf-8 -*-


class Estatisticas:

    TOTAL_PERGUNTAS = 1980
    TOTAL_LIVROS = 66


    def __init__(
        self,
        progresso,
        revisao,
        desafio,
        sequencia
    ):

        self.progresso = progresso
        self.revisao = revisao
        self.desafio = desafio
        self.sequencia = sequencia


    # ==================================================
    # PERGUNTAS APRENDIDAS
    # ==================================================

    def perguntas_aprendidas(self):

        total = 0

        livros = (
            self.progresso
            .dados
            .get(
                "livros",
                {}
            )
        )

        for dados_livro in livros.values():

            total += len(
                dados_livro.get(
                    "acertos_unicos",
                    []
                )
            )

        return total


    # ==================================================
    # RESUMO COMPLETO
    # ==================================================

    def resumo(
        self,
        data_referencia=None
    ):

        progresso = (
            self.progresso
            .resumo()
        )

        revisao = (
            self.revisao
            .resumo()
        )

        desafio = (
            self.desafio
            .resumo()
        )

        sequencia = (
            self.sequencia
            .resumo(
                data_referencia
            )
        )

        aprendidas = (
            self.perguntas_aprendidas()
        )

        percentual_banco = round(
            (
                aprendidas
                / self.TOTAL_PERGUNTAS
            )
            * 100,
            1
        )

        return {

            "jogador":
                progresso[
                    "nome"
                ],

            "xp":
                progresso[
                    "xp"
                ],

            "moedas":
                progresso[
                    "moedas"
                ],

            "livros_concluidos":
                progresso[
                    "livros_concluidos"
                ],

            "total_livros":
                self.TOTAL_LIVROS,

            "respostas_confirmadas":
                progresso[
                    "respostas_confirmadas"
                ],

            "acertos":
                progresso[
                    "acertos"
                ],

            "erros":
                progresso[
                    "erros"
                ],

            "percentual_acertos":
                progresso[
                    "percentual_acertos"
                ],

            "perguntas_aprendidas":
                aprendidas,

            "total_perguntas":
                self.TOTAL_PERGUNTAS,

            "percentual_banco_aprendido":
                percentual_banco,

            "perguntas_para_revisar":
                revisao[
                    "total_pendentes"
                ],

            "livros_com_erros":
                revisao[
                    "livros_com_erros"
                ],

            "desafios_concluidos":
                desafio[
                    "dias_concluidos"
                ],

            "melhor_desafio":
                desafio[
                    "melhor_acertos"
                ],

            "media_desafio":
                desafio[
                    "media_acertos"
                ],

            "sequencia_atual":
                sequencia[
                    "sequencia_atual"
                ],

            "maior_sequencia":
                sequencia[
                    "maior_sequencia"
                ],

            "dias_estudados":
                sequencia[
                    "dias_estudados"
                ],

            "marcos_sequencia":
                sequencia[
                    "marcos_alcancados"
                ]
        }
