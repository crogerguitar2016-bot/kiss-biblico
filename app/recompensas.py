# -*- coding: utf-8 -*-

from pathlib import Path
import json


from app.caminhos import QUIZ_JSON

BANCO_QUIZ = QUIZ_JSON


SELOS = {

    "Gênesis":
        "Selo das Origens",

    "Êxodo":
        "Selo da Libertação",

    "Levítico":
        "Selo da Santidade",

    "Números":
        "Selo da Perseverança",

    "Deuteronômio":
        "Selo da Aliança",

    "Josué":
        "Selo da Coragem",

    "Juízes":
        "Selo da Fidelidade",

    "Rute":
        "Selo da Lealdade",

    "1 Samuel":
        "Selo da Obediência",

    "2 Samuel":
        "Selo da Promessa",

    "1 Reis":
        "Selo da Sabedoria",

    "2 Reis":
        "Selo da Palavra Cumprida",

    "1 Crônicas":
        "Selo da Memória",

    "2 Crônicas":
        "Selo da Restauração",

    "Esdras":
        "Selo do Retorno",

    "Neemias":
        "Selo da Reconstrução",

    "Ester":
        "Selo da Providência",

    "Jó":
        "Selo da Perseverança na Provação",

    "Salmos":
        "Selo da Adoração",

    "Provérbios":
        "Selo da Sabedoria",

    "Eclesiastes":
        "Selo da Reflexão",

    "Cântico dos Cânticos":
        "Selo do Amor",

    "Isaías":
        "Selo da Esperança",

    "Jeremias":
        "Selo da Nova Aliança",

    "Lamentações":
        "Selo da Esperança na Dor",

    "Ezequiel":
        "Selo da Restauração",

    "Daniel":
        "Selo da Fidelidade",

    "Oséias":
        "Selo do Amor Fiel",

    "Joel":
        "Selo do Espírito",

    "Amós":
        "Selo da Justiça",

    "Obadias":
        "Selo da Humildade",

    "Jonas":
        "Selo da Misericórdia",

    "Miqueias":
        "Selo da Justiça e Misericórdia",

    "Naum":
        "Selo da Justiça Divina",

    "Habacuque":
        "Selo da Fé",

    "Sofonias":
        "Selo do Remanescente",

    "Ageu":
        "Selo da Prioridade",

    "Zacarias":
        "Selo da Esperança Messiânica",

    "Malaquias":
        "Selo da Fidelidade",

    "Mateus":
        "Selo do Reino",

    "Marcos":
        "Selo do Servo",

    "Lucas":
        "Selo da Compaixão",

    "João":
        "Selo da Vida",

    "Atos":
        "Selo da Missão",

    "Romanos":
        "Selo do Evangelho",

    "1 Coríntios":
        "Selo da Unidade",

    "2 Coríntios":
        "Selo da Graça na Fraqueza",

    "Gálatas":
        "Selo da Liberdade",

    "Efésios":
        "Selo da Unidade em Cristo",

    "Filipenses":
        "Selo da Alegria",

    "Colossenses":
        "Selo da Supremacia de Cristo",

    "1 Tessalonicenses":
        "Selo da Esperança",

    "2 Tessalonicenses":
        "Selo da Perseverança",

    "1 Timóteo":
        "Selo da Sã Doutrina",

    "2 Timóteo":
        "Selo da Fidelidade",

    "Tito":
        "Selo das Boas Obras",

    "Filemom":
        "Selo da Reconciliação",

    "Hebreus":
        "Selo da Excelência de Cristo",

    "Tiago":
        "Selo da Fé Prática",

    "1 Pedro":
        "Selo da Esperança no Sofrimento",

    "2 Pedro":
        "Selo do Crescimento",

    "1 João":
        "Selo do Amor",

    "2 João":
        "Selo da Verdade",

    "3 João":
        "Selo da Hospitalidade",

    "Judas":
        "Selo da Perseverança na Fé",

    "Apocalipse":
        "Selo da Vitória",
}


class Recompensas:

    TOTAL_PERGUNTAS_LIVRO = 30

    @staticmethod
    def calcular_estrelas(acertos):

        if not isinstance(
            acertos,
            int
        ):

            raise ValueError(
                "Quantidade de acertos inválida."
            )

        if not 0 <= acertos <= 30:

            raise ValueError(
                "Acertos devem estar entre 0 e 30."
            )


        if acertos >= 29:
            return 3

        if acertos >= 24:
            return 2

        if acertos >= 18:
            return 1

        return 0


    @staticmethod
    def percentual(acertos):

        return round(
            (
                acertos
                / 30
            )
            * 100,
            1
        )


    @staticmethod
    def estrelas_texto(
        estrelas
    ):

        if estrelas == 3:
            return "⭐⭐⭐"

        if estrelas == 2:
            return "⭐⭐"

        if estrelas == 1:
            return "⭐"

        return "Ainda sem estrelas"


    @staticmethod
    def selo_do_livro(
        livro
    ):

        if livro not in SELOS:

            raise ValueError(
                f"Livro não reconhecido: {livro}"
            )

        return SELOS[livro]


    @staticmethod
    def proxima_meta(
        acertos
    ):

        estrelas = (
            Recompensas
            .calcular_estrelas(
                acertos
            )
        )

        if estrelas == 0:

            return {
                "acertos_necessarios": 18,
                "faltam":
                    max(
                        0,
                        18 - acertos
                    ),
                "meta":
                    "Conquistar 1 estrela"
            }

        if estrelas == 1:

            return {
                "acertos_necessarios": 24,
                "faltam":
                    max(
                        0,
                        24 - acertos
                    ),
                "meta":
                    "Conquistar 2 estrelas"
            }

        if estrelas == 2:

            return {
                "acertos_necessarios": 29,
                "faltam":
                    max(
                        0,
                        29 - acertos
                    ),
                "meta":
                    "Conquistar 3 estrelas"
            }

        return {
            "acertos_necessarios": None,
            "faltam": 0,
            "meta":
                "Pontuação máxima alcançada"
        }


    @staticmethod
    def mensagem(
        nome,
        livro,
        acertos
    ):

        nome = (
            str(nome).strip()
            if nome
            else "Jogador"
        )

        estrelas = (
            Recompensas
            .calcular_estrelas(
                acertos
            )
        )

        if estrelas == 3:

            return (
                f"Excelente, {nome}! "
                f"Você concluiu {livro} "
                "com um resultado extraordinário. "
                "Seu conhecimento deste livro "
                "alcançou o nível máximo desta jornada."
            )

        if estrelas == 2:

            return (
                f"Muito bem, {nome}! "
                f"Você concluiu {livro} "
                "com ótimo aproveitamento. "
                "Continue avançando e tente conquistar "
                "as três estrelas."
            )

        if estrelas == 1:

            return (
                f"Parabéns, {nome}! "
                f"Você concluiu {livro} "
                "e conquistou sua primeira estrela. "
                "Você pode refazer este livro depois "
                "para melhorar ainda mais seu resultado."
            )

        return (
            f"{nome}, você concluiu {livro}. "
            "A jornada continua. "
            "Revisar as perguntas que você errou "
            "pode ajudar você a conquistar "
            "sua primeira estrela."
        )


    @staticmethod
    def montar_recompensa(
        nome,
        livro,
        acertos
    ):

        estrelas = (
            Recompensas
            .calcular_estrelas(
                acertos
            )
        )

        percentual = (
            Recompensas
            .percentual(
                acertos
            )
        )

        selo = (
            Recompensas
            .selo_do_livro(
                livro
            )
        )

        mensagem = (
            Recompensas
            .mensagem(
                nome,
                livro,
                acertos
            )
        )

        meta = (
            Recompensas
            .proxima_meta(
                acertos
            )
        )

        nome_exibicao = (
            str(nome).strip()
            if nome
            else "Jogador"
        )


        texto_pergaminho = (
            "PERGAMINHO DE CONQUISTA\n\n"
            f"{nome_exibicao}\n\n"
            f"concluiu a jornada pelo livro de\n"
            f"{livro}\n\n"
            f"{selo}\n\n"
            f"Resultado: {acertos}/30\n"
            f"Aproveitamento: {percentual}%\n"
            f"{Recompensas.estrelas_texto(estrelas)}"
        )


        return {

            "jogador":
                nome_exibicao,

            "livro":
                livro,

            "acertos":
                acertos,

            "erros":
                30 - acertos,

            "percentual":
                percentual,

            "estrelas":
                estrelas,

            "estrelas_texto":
                Recompensas
                .estrelas_texto(
                    estrelas
                ),

            "selo":
                selo,

            "mensagem":
                mensagem,

            "proxima_meta":
                meta,

            "pergaminho": {
                "titulo":
                    "PERGAMINHO DE CONQUISTA",

                "texto":
                    texto_pergaminho
            }
        }


def validar_selose_livros():

    if not BANCO_QUIZ.exists():

        raise RuntimeError(
            "quiz_biblico.json não encontrado."
        )

    with BANCO_QUIZ.open(
        "r",
        encoding="utf-8"
    ) as arquivo:

        banco = json.load(
            arquivo
        )


    livros_banco = [
        livro["nome"]
        for livro in banco["livros"]
    ]


    livros_selos = list(
        SELOS.keys()
    )


    faltando = [
        livro
        for livro in livros_banco
        if livro not in SELOS
    ]


    sobrando = [
        livro
        for livro in livros_selos
        if livro not in livros_banco
    ]


    return {
        "livros_banco":
            len(livros_banco),

        "selos":
            len(SELOS),

        "faltando":
            faltando,

        "sobrando":
            sobrando,

        "valido":
            (
                len(livros_banco) == 66
                and len(SELOS) == 66
                and not faltando
                and not sobrando
            )
    }
