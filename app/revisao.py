# -*- coding: utf-8 -*-

from pathlib import Path
import json


from app.caminhos import pasta_saves, QUIZ_JSON

ARQUIVO_QUIZ = QUIZ_JSON

class RevisaoErros:

    def __init__(self, arquivo=None):

        self.arquivo = (
            Path(arquivo)
            if arquivo is not None
            else (
                pasta_saves()
                / "perguntas_erradas.json"
            )
        )

        self.arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.banco = self._carregar_banco()

        self.indice_livros = {
            livro["nome"]: livro
            for livro in self.banco["livros"]
        }

        self.dados = self._carregar()


    # ==================================================
    # BANCO DAS 1.980 PERGUNTAS
    # ==================================================

    def _carregar_banco(self):

        if not ARQUIVO_QUIZ.exists():

            raise RuntimeError(
                "quiz_biblico.json "
                "não foi encontrado."
            )

        with ARQUIVO_QUIZ.open(
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(
                arquivo
            )


    # ==================================================
    # MODELO DO ARQUIVO DE REVISÃO
    # ==================================================

    def _modelo_vazio(self):

        return {
            "versao": 1,
            "pendentes": {}
        }


    # ==================================================
    # CARREGAMENTO
    # ==================================================

    def _carregar(self):

        if not self.arquivo.exists():

            dados = self._modelo_vazio()

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
                "pendentes",
                {}
            )

            if not isinstance(
                dados["pendentes"],
                dict
            ):

                dados[
                    "pendentes"
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


            dados = self._modelo_vazio()

            self._salvar_dados(
                dados
            )

            return dados


    # ==================================================
    # SALVAMENTO ATÔMICO
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
    # VALIDAÇÕES
    # ==================================================

    def _validar(
        self,
        livro,
        numero
    ):

        if livro not in self.indice_livros:

            raise ValueError(
                f"Livro não reconhecido: {livro}"
            )


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


    # ==================================================
    # REGISTRAR RESULTADO
    # ==================================================

    def registrar_resultado(
        self,
        livro,
        numero,
        acertou
    ):

        self._validar(
            livro,
            numero
        )


        pendentes = self.dados[
            "pendentes"
        ]


        pendentes.setdefault(
            livro,
            []
        )


        lista = pendentes[
            livro
        ]


        entrou_na_revisao = False
        saiu_da_revisao = False


        if acertou:

            if numero in lista:

                lista.remove(
                    numero
                )

                saiu_da_revisao = True


        else:

            if numero not in lista:

                lista.append(
                    numero
                )

                lista.sort()

                entrou_na_revisao = True


        # Se o livro não possui mais erros,
        # removemos a chave para manter
        # o save organizado.

        if not lista:

            pendentes.pop(
                livro,
                None
            )


        self.salvar()


        return {
            "livro":
                livro,

            "numero":
                numero,

            "acertou":
                bool(acertou),

            "entrou_na_revisao":
                entrou_na_revisao,

            "saiu_da_revisao":
                saiu_da_revisao,

            "total_pendente":
                self.total_pendentes()
        }


    # ==================================================
    # QUANTIDADE TOTAL DE QUESTÕES ERRADAS
    # ==================================================

    def total_pendentes(self):

        return sum(
            len(numeros)
            for numeros
            in self.dados[
                "pendentes"
            ].values()
        )


    # ==================================================
    # LIVROS QUE POSSUEM ERROS PENDENTES
    # ==================================================

    def livros_com_erros(self):

        resultado = []

        for livro in self.banco[
            "livros"
        ]:

            nome = livro[
                "nome"
            ]

            numeros = (
                self.dados[
                    "pendentes"
                ].get(
                    nome,
                    []
                )
            )

            if numeros:

                resultado.append(
                    {
                        "livro":
                            nome,

                        "quantidade":
                            len(
                                numeros
                            )
                    }
                )

        return resultado


    # ==================================================
    # NÚMEROS DAS PERGUNTAS ERRADAS
    # ==================================================

    def numeros_pendentes(
        self,
        livro
    ):

        if livro not in self.indice_livros:

            raise ValueError(
                f"Livro não reconhecido: {livro}"
            )


        return list(
            self.dados[
                "pendentes"
            ].get(
                livro,
                []
            )
        )


    # ==================================================
    # RECUPERAR PERGUNTA REAL DO BANCO
    # ==================================================

    def obter_pergunta(
        self,
        livro,
        numero
    ):

        self._validar(
            livro,
            numero
        )


        perguntas = (
            self.indice_livros[
                livro
            ][
                "perguntas"
            ]
        )


        for pergunta in perguntas:

            if (
                pergunta[
                    "numero"
                ]
                == numero
            ):

                resultado = dict(
                    pergunta
                )

                resultado[
                    "livro"
                ] = livro

                return resultado


        raise RuntimeError(
            "Pergunta não encontrada."
        )


    # ==================================================
    # PERGUNTAS ERRADAS DE UM LIVRO
    # ==================================================

    def perguntas_do_livro(
        self,
        livro
    ):

        numeros = (
            self.numeros_pendentes(
                livro
            )
        )


        return [
            self.obter_pergunta(
                livro,
                numero
            )
            for numero in numeros
        ]


    # ==================================================
    # TODAS AS PERGUNTAS PARA REVISÃO
    # ==================================================

    def todas_as_perguntas(self):

        resultado = []


        for livro in self.banco[
            "livros"
        ]:

            nome = livro[
                "nome"
            ]

            resultado.extend(
                self.perguntas_do_livro(
                    nome
                )
            )


        return resultado


    # ==================================================
    # RESUMO
    # ==================================================

    def resumo(self):

        livros = (
            self.livros_com_erros()
        )

        return {
            "total_pendentes":
                self.total_pendentes(),

            "livros_com_erros":
                len(livros),

            "livros":
                livros
        }
