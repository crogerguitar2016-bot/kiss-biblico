# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import date, datetime, timedelta
import json


from app.caminhos import pasta_saves

class SequenciaEstudo:

    MARCOS = [
        1,
        2,
        7,
        30
    ]


    def __init__(
        self,
        arquivo=None
    ):

        self.arquivo = (
            Path(arquivo)
            if arquivo is not None
            else (
                pasta_saves()
                / "sequencia_estudo.json"
            )
        )

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.dados = (
            self._carregar()
        )


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
            "dias_estudados": []
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


            dados.setdefault(
                "versao",
                1
            )

            dados.setdefault(
                "dias_estudados",
                []
            )


            if not isinstance(
                dados[
                    "dias_estudados"
                ],
                list
            ):

                dados[
                    "dias_estudados"
                ] = []


            dados[
                "dias_estudados"
            ] = sorted(
                set(
                    dados[
                        "dias_estudados"
                    ]
                )
            )


            return dados


        except Exception:

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
    # REGISTRAR DIA DE ESTUDO
    # ==================================================

    def registrar_atividade(
        self,
        data_referencia=None
    ):

        dia = (
            self._normalizar_data(
                data_referencia
            )
        )

        texto = (
            dia.isoformat()
        )


        dias = self.dados[
            "dias_estudados"
        ]


        novo_dia = False


        if texto not in dias:

            dias.append(
                texto
            )

            dias.sort()

            novo_dia = True

            self.salvar()


        resultado = (
            self.resumo(
                data_referencia=dia
            )
        )


        resultado[
            "novo_dia"
        ] = novo_dia


        return resultado


    # ==================================================
    # SEQUÊNCIA TERMINANDO NUM DIA
    # ==================================================

    def _sequencia_terminando_em(
        self,
        dia
    ):

        conjunto = {
            date.fromisoformat(
                item
            )
            for item in self.dados[
                "dias_estudados"
            ]
        }


        if dia not in conjunto:

            return 0


        contador = 0

        atual = dia


        while atual in conjunto:

            contador += 1

            atual -= timedelta(
                days=1
            )


        return contador


    # ==================================================
    # MAIOR SEQUÊNCIA JÁ ALCANÇADA
    # ==================================================

    def maior_sequencia(self):

        datas = sorted(
            date.fromisoformat(
                item
            )
            for item in self.dados[
                "dias_estudados"
            ]
        )


        if not datas:
            return 0


        maior = 1
        atual = 1


        for anterior, seguinte in zip(
            datas,
            datas[1:]
        ):

            diferenca = (
                seguinte
                - anterior
            ).days


            if diferenca == 1:

                atual += 1

            else:

                atual = 1


            maior = max(
                maior,
                atual
            )


        return maior


    # ==================================================
    # RESUMO
    # ==================================================

    def resumo(
        self,
        data_referencia=None
    ):

        referencia = (
            self._normalizar_data(
                data_referencia
            )
        )


        datas = sorted(
            date.fromisoformat(
                item
            )
            for item in self.dados[
                "dias_estudados"
            ]
        )


        if not datas:

            return {
                "dias_estudados": 0,
                "sequencia_atual": 0,
                "maior_sequencia": 0,
                "ultimo_estudo": None,
                "marcos_alcancados": []
            }


        ultimo = datas[-1]


        diferenca = (
            referencia
            - ultimo
        ).days


        # Se estudou hoje:
        # sequência termina hoje.
        #
        # Se estudou ontem:
        # a sequência ainda está ativa.
        #
        # Se passou mais tempo:
        # sequência atual = zero.

        if diferenca == 0:

            sequencia_atual = (
                self._sequencia_terminando_em(
                    ultimo
                )
            )

        elif diferenca == 1:

            sequencia_atual = (
                self._sequencia_terminando_em(
                    ultimo
                )
            )

        else:

            sequencia_atual = 0


        maior = (
            self.maior_sequencia()
        )


        marcos = [
            marco
            for marco in self.MARCOS
            if maior >= marco
        ]


        return {
            "dias_estudados":
                len(datas),

            "sequencia_atual":
                sequencia_atual,

            "maior_sequencia":
                maior,

            "ultimo_estudo":
                ultimo.isoformat(),

            "marcos_alcancados":
                marcos
        }
