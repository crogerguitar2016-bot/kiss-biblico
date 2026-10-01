# -*- coding: utf-8 -*-

from app.motor_quiz import MotorQuiz
from app.progresso import Progresso
from app.revisao import RevisaoErros
from app.recompensas import Recompensas
from app.desafio_diario import DesafioDiario
from app.sequencia import SequenciaEstudo
from app.estatisticas import Estatisticas


class ControladorJornada:

    def __init__(
        self,
        arquivo_progresso=None,
        arquivo_revisao=None,
        arquivo_desafio=None,
        arquivo_sequencia=None
    ):

        self.motor = MotorQuiz()

        self.progresso = Progresso(
            arquivo_progresso
        )

        self.revisao = RevisaoErros(
            arquivo_revisao
        )

        self.desafio = DesafioDiario(
            arquivo_desafio
        )

        self.sequencia = SequenciaEstudo(
            arquivo_sequencia
        )

        self.estatisticas = Estatisticas(
            self.progresso,
            self.revisao,
            self.desafio,
            self.sequencia
        )

        self.modo = None

        self.nome_livro_sessao = None

        self.data_sessao = None


    # ==================================================
    # JOGADOR
    # ==================================================

    def definir_nome(
        self,
        nome
    ):

        return (
            self.progresso
            .definir_nome(
                nome
            )
        )


    def nome_jogador(self):

        return (
            self.progresso
            .nome_jogador()
        )


    # ==================================================
    # CONFIGURAR SESSÃO PERSONALIZADA
    # ==================================================

    def _abrir_lista(
        self,
        titulo,
        perguntas
    ):

        self.motor.livro_atual = {
            "nome":
                titulo,

            "perguntas":
                perguntas
        }

        self.motor.indice_pergunta = 0

        self.motor.resposta_selecionada = None

        self.motor.resposta_confirmada = False

        self.motor.acertos = 0

        self.motor.erros = 0


    # ==================================================
    # ABRIR LIVRO NORMAL
    # ==================================================

    def abrir_livro(
        self,
        nome
    ):

        abriu = (
            self.motor
            .abrir_livro(
                nome
            )
        )

        if not abriu:

            return {
                "estado":
                    "livro_nao_encontrado",

                "livro":
                    nome
            }


        self.modo = "livro"

        self.nome_livro_sessao = nome

        self.data_sessao = None


        return {
            "estado":
                "livro_aberto",

            "livro":
                nome,

            "total_perguntas":
                len(
                    self.motor
                    .livro_atual[
                        "perguntas"
                    ]
                )
        }


    # ==================================================
    # ABRIR PERGUNTAS QUE ERREI
    # ==================================================

    def abrir_revisao(
        self,
        livro=None
    ):

        if livro:

            perguntas = (
                self.revisao
                .perguntas_do_livro(
                    livro
                )
            )

            titulo = (
                "Revisão - "
                + livro
            )

        else:

            perguntas = (
                self.revisao
                .todas_as_perguntas()
            )

            titulo = (
                "Perguntas que errei"
            )


        if not perguntas:

            return {
                "estado":
                    "revisao_vazia",

                "total_perguntas":
                    0
            }


        self._abrir_lista(
            titulo,
            perguntas
        )

        self.modo = "revisao"

        self.nome_livro_sessao = livro

        self.data_sessao = None


        return {
            "estado":
                "revisao_aberta",

            "livro":
                livro,

            "total_perguntas":
                len(
                    perguntas
                )
        }


    # ==================================================
    # ABRIR DESAFIO DIÁRIO
    # ==================================================

    def abrir_desafio(
        self,
        data_referencia=None
    ):

        perguntas = (
            self.desafio
            .perguntas_do_dia(
                data_referencia
            )
        )


        self._abrir_lista(
            "Desafio Diário",
            perguntas
        )

        self.modo = "desafio"

        self.nome_livro_sessao = None

        self.data_sessao = (
            data_referencia
        )


        return {
            "estado":
                "desafio_aberto",

            "total_perguntas":
                len(
                    perguntas
                ),

            "ja_concluido":
                self.desafio
                .concluido_em(
                    data_referencia
                )
        }


    # ==================================================
    # PERGUNTA PARA A INTERFACE
    #
    # Não enviamos a resposta correta antes
    # da confirmação.
    # ==================================================

    def pergunta_atual(self):

        pergunta = (
            self.motor
            .pergunta_atual()
        )

        if pergunta is None:
            return None


        publica = {
            chave: valor
            for chave, valor
            in pergunta.items()

            if chave not in {
                "correta",
                "resposta_correta",
                "texto_gabarito"
            }
        }


        if (
            "alternativas"
            in publica
        ):

            publica[
                "alternativas"
            ] = dict(
                publica[
                    "alternativas"
                ]
            )


        publica[
            "posicao"
        ] = (
            self.motor
            .indice_pergunta
            + 1
        )


        publica[
            "total_sessao"
        ] = len(
            self.motor
            .livro_atual[
                "perguntas"
            ]
        )


        return publica


    # ==================================================
    # SELECIONAR A/B/C/D
    # ==================================================

    def selecionar_resposta(
        self,
        letra
    ):

        return (
            self.motor
            .selecionar_resposta(
                letra
            )
        )


    # ==================================================
    # IDENTIFICAR LIVRO REAL DA PERGUNTA
    # ==================================================

    def _livro_da_pergunta(
        self,
        pergunta
    ):

        if self.modo == "livro":

            return (
                self.nome_livro_sessao
            )


        livro = pergunta.get(
            "livro"
        )


        if not livro:

            raise RuntimeError(
                "Não foi possível identificar "
                "o livro da pergunta."
            )


        return livro


    # ==================================================
    # SIM / NÃO
    # ==================================================

    def decidir_mudar(
        self,
        decisao,
        data_referencia=None
    ):

        pergunta = (
            self.motor
            .pergunta_atual()
        )


        if pergunta is None:

            raise RuntimeError(
                "Não existe pergunta atual."
            )


        resultado = (
            self.motor
            .decidir_mudar(
                decisao
            )
        )


        # Se escolheu SIM, nenhuma pontuação,
        # erro ou atividade é registrada.

        if (
            resultado[
                "estado"
            ]
            != "confirmada"
        ):

            return resultado


        livro = (
            self._livro_da_pergunta(
                pergunta
            )
        )


        numero = (
            pergunta[
                "numero"
            ]
        )


        acertou = (
            resultado[
                "acertou"
            ]
        )


        # ----------------------------------------------
        # PROGRESSO / XP / MOEDAS
        # ----------------------------------------------

        progresso_resultado = (
            self.progresso
            .registrar_resposta(
                livro,
                numero,
                acertou
            )
        )


        # ----------------------------------------------
        # PERGUNTAS QUE ERREI
        # ----------------------------------------------

        revisao_resultado = (
            self.revisao
            .registrar_resultado(
                livro,
                numero,
                acertou
            )
        )


        # ----------------------------------------------
        # SEQUÊNCIA DE ESTUDO
        # ----------------------------------------------

        data_atividade = (
            data_referencia
        )

        if (
            data_atividade is None
            and self.modo == "desafio"
        ):

            data_atividade = (
                self.data_sessao
            )


        sequencia_resultado = (
            self.sequencia
            .registrar_atividade(
                data_atividade
            )
        )


        resultado[
            "livro"
        ] = livro

        resultado[
            "numero"
        ] = numero

        resultado[
            "xp_ganho"
        ] = (
            progresso_resultado[
                "ganhou_xp"
            ]
        )

        resultado[
            "moedas_ganhas"
        ] = (
            progresso_resultado[
                "ganhou_moedas"
            ]
        )

        resultado[
            "xp_total"
        ] = (
            progresso_resultado[
                "xp_total"
            ]
        )

        resultado[
            "moedas_total"
        ] = (
            progresso_resultado[
                "moedas_total"
            ]
        )

        resultado[
            "entrou_na_revisao"
        ] = (
            revisao_resultado[
                "entrou_na_revisao"
            ]
        )

        resultado[
            "saiu_da_revisao"
        ] = (
            revisao_resultado[
                "saiu_da_revisao"
            ]
        )

        resultado[
            "perguntas_para_revisar"
        ] = (
            revisao_resultado[
                "total_pendente"
            ]
        )

        resultado[
            "sequencia_atual"
        ] = (
            sequencia_resultado[
                "sequencia_atual"
            ]
        )


        return resultado


    # ==================================================
    # PRÓXIMA PERGUNTA
    # ==================================================

    def proxima_pergunta(self):

        resultado = (
            self.motor
            .proxima_pergunta()
        )


        if (
            resultado[
                "estado"
            ]
            != "livro_concluido"
        ):

            resultado[
                "pergunta"
            ] = (
                self.pergunta_atual()
            )

            return resultado


        # ==============================================
        # FINAL DE LIVRO NORMAL
        # ==============================================

        if self.modo == "livro":

            livro = (
                self.nome_livro_sessao
            )

            acertos = (
                self.motor.acertos
            )

            erros = (
                self.motor.erros
            )


            status = (
                self.progresso
                .concluir_livro(
                    livro,
                    acertos
                )
            )


            recompensa = (
                Recompensas
                .montar_recompensa(
                    self.nome_jogador(),
                    livro,
                    acertos
                )
            )


            return {
                "estado":
                    "livro_concluido",

                "livro":
                    livro,

                "acertos":
                    acertos,

                "erros":
                    erros,

                "status":
                    status,

                "recompensa":
                    recompensa
            }


        # ==============================================
        # FINAL DE REVISÃO
        # ==============================================

        if self.modo == "revisao":

            return {
                "estado":
                    "revisao_concluida",

                "acertos":
                    self.motor.acertos,

                "erros":
                    self.motor.erros,

                "pendentes":
                    self.revisao
                    .total_pendentes()
            }


        # ==============================================
        # FINAL DO DESAFIO DIÁRIO
        # ==============================================

        if self.modo == "desafio":

            conclusao = (
                self.desafio
                .registrar_conclusao(
                    self.motor.acertos,
                    self.data_sessao
                )
            )


            return {
                "estado":
                    "desafio_concluido",

                "acertos":
                    self.motor.acertos,

                "erros":
                    self.motor.erros,

                "resultado":
                    conclusao
            }


        raise RuntimeError(
            "Modo de sessão desconhecido."
        )


    # ==================================================
    # RESUMO GERAL
    # ==================================================

    def meu_progresso(
        self,
        data_referencia=None
    ):

        return (
            self.estatisticas
            .resumo(
                data_referencia
            )
        )
