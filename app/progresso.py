# -*- coding: utf-8 -*-

from pathlib import Path
import json


from app.caminhos import pasta_saves

class Progresso:

    XP_POR_ACERTO = 10
    MOEDAS_POR_ACERTO = 1

    def __init__(self, arquivo=None):

        self.arquivo = (
            Path(arquivo)
            if arquivo is not None
            else (
                pasta_saves()
                / "progresso.json"
            )
        )

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.dados = self._carregar()


    # ==================================================
    # MODELO INICIAL
    # ==================================================

    def _modelo_vazio(self):

        return {
            "versao": 1,

            "jogador": {
                "nome": ""
            },

            "xp": 0,

            "moedas": 0,

            "estatisticas": {
                "respostas_confirmadas": 0,
                "acertos": 0,
                "erros": 0
            },

            "livros": {}
        }


    # ==================================================
    # COMPATIBILIDADE / MIGRAÇÃO
    # ==================================================

    def _normalizar_dados(self, dados):

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
            "jogador",
            {}
        )

        if not isinstance(
            dados["jogador"],
            dict
        ):
            dados["jogador"] = {}

        dados[
            "jogador"
        ].setdefault(
            "nome",
            ""
        )

        dados.setdefault(
            "xp",
            0
        )

        dados.setdefault(
            "moedas",
            0
        )

        dados.setdefault(
            "estatisticas",
            {}
        )

        if not isinstance(
            dados["estatisticas"],
            dict
        ):
            dados[
                "estatisticas"
            ] = {}

        dados[
            "estatisticas"
        ].setdefault(
            "respostas_confirmadas",
            0
        )

        dados[
            "estatisticas"
        ].setdefault(
            "acertos",
            0
        )

        dados[
            "estatisticas"
        ].setdefault(
            "erros",
            0
        )

        dados.setdefault(
            "livros",
            {}
        )

        if not isinstance(
            dados["livros"],
            dict
        ):
            dados["livros"] = {}

        return dados


    # ==================================================
    # CARREGAMENTO
    # ==================================================

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

            dados = (
                self._normalizar_dados(
                    dados
                )
            )

            return dados

        except Exception:

            backup_corrompido = (
                self.arquivo.with_name(
                    self.arquivo.stem
                    + "_CORROMPIDO"
                    + self.arquivo.suffix
                )
            )

            try:

                self.arquivo.replace(
                    backup_corrompido
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


    # ==================================================
    # SALVAMENTO SEGURO
    # ==================================================

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
    # JOGADOR
    # ==================================================

    def definir_nome(
        self,
        nome
    ):

        if nome is None:

            raise ValueError(
                "Informe o nome do jogador."
            )

        nome = " ".join(
            str(nome).split()
        )

        if not nome:

            raise ValueError(
                "O nome do jogador "
                "não pode ficar vazio."
            )

        if len(nome) > 40:

            raise ValueError(
                "O nome deve ter "
                "no máximo 40 caracteres."
            )

        self.dados.setdefault(
            "jogador",
            {}
        )

        self.dados[
            "jogador"
        ]["nome"] = nome

        self.salvar()

        return nome


    def nome_jogador(self):

        return (
            self.dados
            .get(
                "jogador",
                {}
            )
            .get(
                "nome",
                ""
            )
            .strip()
        )


    def jogador_tem_nome(self):

        return bool(
            self.nome_jogador()
        )


    # ==================================================
    # ESTRUTURA DE CADA LIVRO
    # ==================================================

    def _livro(
        self,
        nome
    ):

        if not nome:

            raise ValueError(
                "Nome do livro inválido."
            )

        livros = self.dados[
            "livros"
        ]

        if nome not in livros:

            livros[nome] = {

                "respondidas_unicas": [],

                "acertos_unicos": [],

                "concluido": False,

                "tentativas": 0,

                "melhor_acertos": 0
            }

        dados_livro = livros[nome]

        dados_livro.setdefault(
            "respondidas_unicas",
            []
        )

        dados_livro.setdefault(
            "acertos_unicos",
            []
        )

        dados_livro.setdefault(
            "concluido",
            False
        )

        dados_livro.setdefault(
            "tentativas",
            0
        )

        dados_livro.setdefault(
            "melhor_acertos",
            0
        )

        return dados_livro


    # ==================================================
    # REGISTRAR RESPOSTA
    # ==================================================

    def registrar_resposta(
        self,
        livro,
        numero,
        acertou
    ):

        if not isinstance(
            numero,
            int
        ):

            raise ValueError(
                "Número da pergunta inválido."
            )

        if not 1 <= numero <= 30:

            raise ValueError(
                "Número da pergunta deve "
                "estar entre 1 e 30."
            )

        acertou = bool(
            acertou
        )

        dados_livro = (
            self._livro(
                livro
            )
        )

        estatisticas = (
            self.dados[
                "estatisticas"
            ]
        )

        estatisticas[
            "respostas_confirmadas"
        ] += 1

        if acertou:

            estatisticas[
                "acertos"
            ] += 1

        else:

            estatisticas[
                "erros"
            ] += 1


        # ----------------------------------------------
        # Pergunta respondida pelo menos uma vez
        # ----------------------------------------------

        if (
            numero
            not in
            dados_livro[
                "respondidas_unicas"
            ]
        ):

            dados_livro[
                "respondidas_unicas"
            ].append(
                numero
            )

            dados_livro[
                "respondidas_unicas"
            ].sort()


        ganhou_xp = 0
        ganhou_moedas = 0


        # ----------------------------------------------
        # Recompensa apenas no PRIMEIRO acerto
        # daquela pergunta.
        #
        # Isso impede farm infinito de XP.
        # ----------------------------------------------

        if (
            acertou
            and numero
            not in
            dados_livro[
                "acertos_unicos"
            ]
        ):

            dados_livro[
                "acertos_unicos"
            ].append(
                numero
            )

            dados_livro[
                "acertos_unicos"
            ].sort()

            ganhou_xp = (
                self.XP_POR_ACERTO
            )

            ganhou_moedas = (
                self.MOEDAS_POR_ACERTO
            )

            self.dados[
                "xp"
            ] += ganhou_xp

            self.dados[
                "moedas"
            ] += ganhou_moedas


        self.salvar()


        return {

            "livro":
                livro,

            "numero":
                numero,

            "acertou":
                acertou,

            "ganhou_xp":
                ganhou_xp,

            "ganhou_moedas":
                ganhou_moedas,

            "xp_total":
                self.dados[
                    "xp"
                ],

            "moedas_total":
                self.dados[
                    "moedas"
                ]
        }


    # ==================================================
    # CONCLUSÃO DO LIVRO
    # ==================================================

    def concluir_livro(
        self,
        livro,
        acertos
    ):

        if not isinstance(
            acertos,
            int
        ):

            raise ValueError(
                "Quantidade de acertos inválida."
            )

        if not 0 <= acertos <= 30:

            raise ValueError(
                "Acertos devem estar "
                "entre 0 e 30."
            )

        dados_livro = (
            self._livro(
                livro
            )
        )

        dados_livro[
            "tentativas"
        ] += 1

        dados_livro[
            "concluido"
        ] = True

        if (
            acertos
            >
            dados_livro[
                "melhor_acertos"
            ]
        ):

            dados_livro[
                "melhor_acertos"
            ] = acertos


        self.salvar()


        return self.status_livro(
            livro
        )


    # ==================================================
    # CONSULTAR UM LIVRO
    # ==================================================

    def status_livro(
        self,
        livro
    ):

        dados = (
            self._livro(
                livro
            )
        )

        return {

            "livro":
                livro,

            "respondidas_unicas":
                len(
                    dados[
                        "respondidas_unicas"
                    ]
                ),

            "acertos_unicos":
                len(
                    dados[
                        "acertos_unicos"
                    ]
                ),

            "concluido":
                dados[
                    "concluido"
                ],

            "tentativas":
                dados[
                    "tentativas"
                ],

            "melhor_acertos":
                dados[
                    "melhor_acertos"
                ]
        }


    # ==================================================
    # CONSULTAR RESUMO GERAL
    # ==================================================

    def resumo(self):

        livros = (
            self.dados[
                "livros"
            ]
        )

        concluidos = sum(
            1
            for dados
            in livros.values()
            if dados.get(
                "concluido",
                False
            )
        )

        estatisticas = (
            self.dados[
                "estatisticas"
            ]
        )

        respostas = (
            estatisticas[
                "respostas_confirmadas"
            ]
        )

        acertos = (
            estatisticas[
                "acertos"
            ]
        )

        erros = (
            estatisticas[
                "erros"
            ]
        )

        if respostas > 0:

            percentual = round(
                (
                    acertos
                    / respostas
                )
                * 100,
                1
            )

        else:

            percentual = 0.0


        return {

            "nome":
                self.nome_jogador(),

            "xp":
                self.dados[
                    "xp"
                ],

            "moedas":
                self.dados[
                    "moedas"
                ],

            "livros_concluidos":
                concluidos,

            "respostas_confirmadas":
                respostas,

            "acertos":
                acertos,

            "erros":
                erros,

            "percentual_acertos":
                percentual
        }
