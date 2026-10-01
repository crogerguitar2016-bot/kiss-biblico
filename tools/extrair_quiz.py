# -*- coding: utf-8 -*-

from pathlib import Path
import json
import re
import unicodedata


PASTA = Path(
    "/data/data/com.termux/files/home/Quiz_Biblico_66"
)

ARQUIVO_TXT = PASTA / "data" / "quiz_biblico.txt"
ARQUIVO_JSON = PASTA / "data" / "quiz_biblico.json"


LIVROS = [
    "Gênesis",
    "Êxodo",
    "Levítico",
    "Números",
    "Deuteronômio",
    "Josué",
    "Juízes",
    "Rute",
    "1 Samuel",
    "2 Samuel",
    "1 Reis",
    "2 Reis",
    "1 Crônicas",
    "2 Crônicas",
    "Esdras",
    "Neemias",
    "Ester",
    "Jó",
    "Salmos",
    "Provérbios",
    "Eclesiastes",
    "Cântico dos Cânticos",
    "Isaías",
    "Jeremias",
    "Lamentações",
    "Ezequiel",
    "Daniel",
    "Oséias",
    "Joel",
    "Amós",
    "Obadias",
    "Jonas",
    "Miqueias",
    "Naum",
    "Habacuque",
    "Sofonias",
    "Ageu",
    "Zacarias",
    "Malaquias",
    "Mateus",
    "Marcos",
    "Lucas",
    "João",
    "Atos",
    "Romanos",
    "1 Coríntios",
    "2 Coríntios",
    "Gálatas",
    "Efésios",
    "Filipenses",
    "Colossenses",
    "1 Tessalonicenses",
    "2 Tessalonicenses",
    "1 Timóteo",
    "2 Timóteo",
    "Tito",
    "Filemom",
    "Hebreus",
    "Tiago",
    "1 Pedro",
    "2 Pedro",
    "1 João",
    "2 João",
    "3 João",
    "Judas",
    "Apocalipse",
]


def normalizar_espacos(texto):
    return re.sub(
        r"\s+",
        " ",
        texto
    ).strip()


def normalizar_comparacao(texto):
    texto = unicodedata.normalize(
        "NFC",
        texto
    )

    texto = normalizar_espacos(texto)

    texto = texto.rstrip(
        "."
    )

    return texto.casefold()


def limpar_linhas(texto):
    resultado = []

    for linha in texto.splitlines():

        linha = linha.strip()

        if not linha:
            continue

        if linha.startswith(
            "Quiz Bíblico - 66 livros"
        ):
            continue

        if re.fullmatch(
            r"Página\s+\d+",
            linha,
            flags=re.I
        ):
            continue

        resultado.append(
            normalizar_espacos(linha)
        )

    return resultado


def separar_livros(texto):
    linhas = limpar_linhas(texto)

    posicoes = []

    inicio_busca = 0

    for numero, livro in enumerate(
        LIVROS,
        start=1
    ):

        alvo = f"{numero}. {livro}"

        encontrado = None

        for indice in range(
            inicio_busca,
            len(linhas)
        ):

            if linhas[indice] == alvo:
                encontrado = indice
                break

        if encontrado is None:
            raise RuntimeError(
                f"Livro não encontrado: "
                f"{numero}. {livro}"
            )

        posicoes.append(
            (
                numero,
                livro,
                encontrado
            )
        )

        inicio_busca = encontrado + 1

    blocos = {}

    for i, (
        numero,
        livro,
        inicio
    ) in enumerate(posicoes):

        if i + 1 < len(posicoes):
            fim = posicoes[i + 1][2]
        else:
            fim = len(linhas)

        blocos[livro] = linhas[
            inicio + 1:fim
        ]

    return blocos


def extrair_perguntas(linhas):
    tema = ""

    perguntas = []

    atual = None
    estado = None

    for linha in linhas:

        if linha.startswith(
            "Tema do livro:"
        ):

            tema = linha.split(
                ":",
                1
            )[1].strip()

            continue

        inicio_pergunta = re.match(
            r"^(\d{1,2})\.\s+(.+)$",
            linha
        )

        if inicio_pergunta:

            numero = int(
                inicio_pergunta.group(1)
            )

            if 1 <= numero <= 30:

                if atual:
                    perguntas.append(
                        atual
                    )

                atual = {
                    "numero": numero,
                    "pergunta":
                        inicio_pergunta.group(2),
                    "alternativas": {},
                    "dica": ""
                }

                estado = "pergunta"

                continue

        if atual is None:
            continue

        alternativa = re.match(
            r"^([ABCD])\.\s+(.+)$",
            linha
        )

        if alternativa:

            letra = alternativa.group(1)

            atual[
                "alternativas"
            ][letra] = alternativa.group(2)

            estado = letra

            continue

        if linha.startswith("Dica:"):

            atual["dica"] = linha.split(
                ":",
                1
            )[1].strip()

            estado = "dica"

            continue

        if estado == "pergunta":

            atual["pergunta"] += (
                " " + linha
            )

        elif estado in {
            "A", "B", "C", "D"
        }:

            atual[
                "alternativas"
            ][estado] += (
                " " + linha
            )

        elif estado == "dica":

            atual["dica"] += (
                " " + linha
            )

    if atual:
        perguntas.append(
            atual
        )

    return tema, perguntas


def extrair_gabarito(linhas):

    respostas = {}

    numero_atual = None

    for linha in linhas:

        resposta = re.match(
            r"^(\d{1,2})\.\s+"
            r"([ABCD])\s*-\s*(.+)$",
            linha
        )

        if resposta:

            numero = int(
                resposta.group(1)
            )

            if 1 <= numero <= 30:

                respostas[numero] = {
                    "letra":
                        resposta.group(2),
                    "texto":
                        resposta.group(3)
                }

                numero_atual = numero

                continue

        if numero_atual is not None:

            respostas[
                numero_atual
            ]["texto"] += (
                " " + linha
            )

    return respostas


if not ARQUIVO_TXT.exists():
    raise SystemExit(
        "ERRO: quiz_biblico.txt "
        "não foi encontrado."
    )


texto = ARQUIVO_TXT.read_text(
    encoding="utf-8",
    errors="replace"
)

texto = texto.replace(
    "\r",
    ""
).replace(
    "\f",
    "\n"
)


marcador = re.search(
    r"(?m)^\s*GABARITO\s*$",
    texto
)

if not marcador:
    raise SystemExit(
        "ERRO: seção GABARITO "
        "não encontrada."
    )


parte_perguntas = texto[
    :marcador.start()
]

parte_gabarito = texto[
    marcador.end():
]


blocos_perguntas = separar_livros(
    parte_perguntas
)

blocos_gabarito = separar_livros(
    parte_gabarito
)


banco = {
    "titulo":
        "Jornada Bíblica - 66 Livros",
    "total_livros": 66,
    "total_perguntas": 1980,
    "livros": []
}


total_perguntas = 0
total_gabaritos = 0
sem_resposta = []
problemas = []
diferencas_texto = []


for indice, livro in enumerate(
    LIVROS,
    start=1
):

    tema, perguntas = extrair_perguntas(
        blocos_perguntas[livro]
    )

    gabarito = extrair_gabarito(
        blocos_gabarito[livro]
    )

    if len(perguntas) != 30:
        problemas.append(
            f"{livro}: "
            f"{len(perguntas)} perguntas"
        )

    if len(gabarito) != 30:
        problemas.append(
            f"{livro}: "
            f"{len(gabarito)} gabaritos"
        )

    perguntas_finais = []

    for pergunta in perguntas:

        numero = pergunta["numero"]

        resposta = gabarito.get(
            numero
        )

        if resposta is None:

            sem_resposta.append(
                f"{livro} - "
                f"pergunta {numero}"
            )

            correta = None
            texto_gabarito = ""

        else:

            correta = resposta["letra"]

            texto_gabarito = normalizar_espacos(
                resposta["texto"]
            )

            total_gabaritos += 1

        alternativas = {}

        for letra in [
            "A", "B", "C", "D"
        ]:

            if letra not in pergunta[
                "alternativas"
            ]:

                problemas.append(
                    f"{livro} "
                    f"pergunta {numero}: "
                    f"alternativa {letra} "
                    f"ausente"
                )

                alternativas[letra] = ""

            else:

                alternativas[letra] = (
                    normalizar_espacos(
                        pergunta[
                            "alternativas"
                        ][letra]
                    )
                )

        resposta_correta = ""

        if correta in alternativas:

            resposta_correta = (
                alternativas[correta]
            )

            if texto_gabarito:

                if (
                    normalizar_comparacao(
                        resposta_correta
                    )
                    !=
                    normalizar_comparacao(
                        texto_gabarito
                    )
                ):

                    diferencas_texto.append(
                        {
                            "livro": livro,
                            "numero": numero,
                            "alternativa":
                                resposta_correta,
                            "gabarito":
                                texto_gabarito
                        }
                    )

        perguntas_finais.append(
            {
                "numero": numero,
                "pergunta":
                    normalizar_espacos(
                        pergunta["pergunta"]
                    ),
                "alternativas":
                    alternativas,
                "dica":
                    normalizar_espacos(
                        pergunta["dica"]
                    ),
                "correta":
                    correta,
                "resposta_correta":
                    resposta_correta,
                "texto_gabarito":
                    texto_gabarito
            }
        )

        total_perguntas += 1

    banco["livros"].append(
        {
            "id": indice,
            "nome": livro,
            "testamento":
                (
                    "Antigo Testamento"
                    if indice <= 39
                    else
                    "Novo Testamento"
                ),
            "tema": tema,
            "perguntas":
                perguntas_finais
        }
    )


ARQUIVO_JSON.write_text(
    json.dumps(
        banco,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print()
print(
    "=== EXTRAÇÃO CONCLUÍDA ==="
)

print(
    "Livros encontrados:",
    len(banco["livros"])
)

print(
    "Perguntas encontradas:",
    total_perguntas
)

print(
    "Gabaritos encontrados:",
    total_gabaritos
)

print(
    "Perguntas sem resposta:",
    len(sem_resposta)
)

print(
    "Problemas estruturais:",
    len(problemas)
)

print(
    "Diferenças texto/gabarito:",
    len(diferencas_texto)
)

print()
print(
    "JSON:",
    ARQUIVO_JSON
)

print(
    "Tamanho:",
    ARQUIVO_JSON.stat().st_size,
    "bytes"
)


if problemas:

    print()
    print(
        "=== PROBLEMAS ==="
    )

    for item in problemas[:20]:
        print(
            "-",
            item
        )


if sem_resposta:

    print()
    print(
        "=== SEM RESPOSTA ==="
    )

    for item in sem_resposta[:20]:
        print(
            "-",
            item
        )


if diferencas_texto:

    print()
    print(
        "=== PRIMEIRAS DIFERENÇAS ==="
    )

    for item in diferencas_texto[:5]:

        print(
            f'{item["livro"]} '
            f'#{item["numero"]}'
        )

        print(
            "ALT:",
            item["alternativa"]
        )

        print(
            "GAB:",
            item["gabarito"]
        )

        print()


print()
print(
    "=== PRIMEIRA PERGUNTA ==="
)

primeira = banco[
    "livros"
][0]["perguntas"][0]

print(
    primeira["pergunta"]
)

for letra, alternativa in (
    primeira["alternativas"].items()
):
    print(
        f"{letra}. {alternativa}"
    )

print(
    "Dica:",
    primeira["dica"]
)

print(
    "Correta:",
    primeira["correta"]
)

print(
    "Resposta:",
    primeira["resposta_correta"]
)
