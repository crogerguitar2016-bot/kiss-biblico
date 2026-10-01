# -*- coding: utf-8 -*-


class EstadoJornada:

    def __init__(
        self,
        progresso,
        livros
    ):

        self.progresso = progresso
        self.livros = list(livros)

        self._garantir()


    def _garantir(self):

        dados = self.progresso.dados

        dados.setdefault(
            "jornada",
            {}
        )

        jornada = dados["jornada"]

        jornada.setdefault(
            "livro",
            None
        )

        jornada.setdefault(
            "pergunta",
            1
        )

        jornada.setdefault(
            "finalizada",
            False
        )

        jornada.setdefault(
            "acertos_sessao",
            0
        )

        jornada.setdefault(
            "erros_sessao",
            0
        )

        jornada.setdefault(
            "respondidas_sessao",
            []
        )

        if not isinstance(
            jornada[
                "respondidas_sessao"
            ],
            list
        ):

            jornada[
                "respondidas_sessao"
            ] = []

        self.progresso.salvar()


    def iniciar_livro(
        self,
        livro,
        pergunta=1
    ):

        if livro not in self.livros:

            raise ValueError(
                "Livro inválido."
            )

        pergunta = int(
            pergunta
        )

        if not 1 <= pergunta <= 30:

            raise ValueError(
                "Pergunta deve estar "
                "entre 1 e 30."
            )

        jornada = (
            self.progresso
            .dados[
                "jornada"
            ]
        )

        jornada[
            "livro"
        ] = livro

        jornada[
            "pergunta"
        ] = pergunta

        jornada[
            "finalizada"
        ] = False

        jornada[
            "acertos_sessao"
        ] = 0

        jornada[
            "erros_sessao"
        ] = 0

        jornada[
            "respondidas_sessao"
        ] = []

        self.progresso.salvar()


    def salvar_posicao(
        self,
        livro,
        pergunta
    ):

        if livro not in self.livros:

            raise ValueError(
                "Livro inválido."
            )

        pergunta = int(
            pergunta
        )

        if not 1 <= pergunta <= 30:

            raise ValueError(
                "Pergunta deve estar "
                "entre 1 e 30."
            )

        jornada = (
            self.progresso
            .dados[
                "jornada"
            ]
        )

        jornada[
            "livro"
        ] = livro

        jornada[
            "pergunta"
        ] = pergunta

        jornada[
            "finalizada"
        ] = False

        self.progresso.salvar()


    def registrar_resposta(
        self,
        livro,
        numero,
        acertou
    ):

        jornada = (
            self.progresso
            .dados[
                "jornada"
            ]
        )

        if (
            jornada.get(
                "livro"
            )
            != livro
        ):

            self.iniciar_livro(
                livro,
                numero
            )

            jornada = (
                self.progresso
                .dados[
                    "jornada"
                ]
            )

        respondidas = jornada[
            "respondidas_sessao"
        ]

        if numero in respondidas:

            return False

        respondidas.append(
            numero
        )

        respondidas.sort()

        if acertou:

            jornada[
                "acertos_sessao"
            ] += 1

        else:

            jornada[
                "erros_sessao"
            ] += 1

        self.progresso.salvar()

        return True


    def restaurar_no_motor(
        self,
        motor,
        livro
    ):

        jornada = (
            self.progresso
            .dados[
                "jornada"
            ]
        )

        if (
            jornada.get(
                "livro"
            )
            != livro
        ):

            return False

        motor.acertos = int(
            jornada.get(
                "acertos_sessao",
                0
            )
        )

        motor.erros = int(
            jornada.get(
                "erros_sessao",
                0
            )
        )

        return True


    def posicao(self):

        jornada = (
            self.progresso
            .dados[
                "jornada"
            ]
        )

        livro = jornada.get(
            "livro"
        )

        if livro not in self.livros:

            return None

        pergunta = int(
            jornada.get(
                "pergunta",
                1
            )
        )

        pergunta = max(
            1,
            min(
                30,
                pergunta
            )
        )

        return {
            "livro":
                livro,

            "pergunta":
                pergunta
        }


    def primeiro_nao_concluido(self):

        livros_salvos = (
            self.progresso
            .dados
            .get(
                "livros",
                {}
            )
        )

        for livro in self.livros:

            dados = (
                livros_salvos
                .get(
                    livro,
                    {}
                )
            )

            if not dados.get(
                "concluido",
                False
            ):

                return {
                    "livro":
                        livro,

                    "pergunta":
                        1
                }

        return None


    def proximo_livro(
        self,
        livro_atual
    ):

        try:

            indice = (
                self.livros
                .index(
                    livro_atual
                )
            )

        except ValueError:

            return None

        indice += 1

        if indice >= len(
            self.livros
        ):

            self.progresso.dados[
                "jornada"
            ][
                "finalizada"
            ] = True

            self.progresso.salvar()

            return None

        proximo = self.livros[
            indice
        ]

        self.iniciar_livro(
            proximo,
            1
        )

        return {
            "livro":
                proximo,

            "pergunta":
                1
        }


    def continuar(self):

        posicao = self.posicao()

        if posicao is not None:

            return posicao

        primeira = (
            self.primeiro_nao_concluido()
        )

        if primeira is not None:

            self.iniciar_livro(
                primeira[
                    "livro"
                ],
                1
            )

        return primeira
