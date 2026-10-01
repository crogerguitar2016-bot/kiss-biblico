# -*- coding: utf-8 -*-

from pathlib import Path
from collections import Counter
import json
import sys


BASE = Path(
    "/data/data/com.termux/files/home/Quiz_Biblico_66"
)

ARQUIVO = BASE / "data" / "quiz_biblico.json"


def falha(lista, mensagem):
    lista.append(mensagem)


if not ARQUIVO.exists():
    print("ERRO: quiz_biblico.json não encontrado.")
    sys.exit(1)


with ARQUIVO.open(
    "r",
    encoding="utf-8"
) as f:
    banco = json.load(f)


erros = []
livros = banco.get("livros", [])

total_perguntas = 0
respostas = Counter()
nomes = []


if banco.get("total_livros") != 66:
    falha(
        erros,
        "total_livros diferente de 66"
    )

if banco.get("total_perguntas") != 1980:
    falha(
        erros,
        "total_perguntas diferente de 1980"
    )

if len(livros) != 66:
    falha(
        erros,
        f"Há {len(livros)} livros no JSON"
    )


for posicao, livro in enumerate(
    livros,
    start=1
):
    nome = livro.get("nome", "")
    nomes.append(nome)

    if livro.get("id") != posicao:
        falha(
            erros,
            f"{nome}: ID incorreto"
        )

    testamento_esperado = (
        "Antigo Testamento"
        if posicao <= 39
        else "Novo Testamento"
    )

    if livro.get(
        "testamento"
    ) != testamento_esperado:
        falha(
            erros,
            f"{nome}: testamento incorreto"
        )

    if not livro.get(
        "tema",
        ""
    ).strip():
        falha(
            erros,
            f"{nome}: tema vazio"
        )

    perguntas = livro.get(
        "perguntas",
        []
    )

    if len(perguntas) != 30:
        falha(
            erros,
            f"{nome}: "
            f"{len(perguntas)} perguntas"
        )

    numeros = [
        p.get("numero")
        for p in perguntas
    ]

    if numeros != list(
        range(1, 31)
    ):
        falha(
            erros,
            f"{nome}: "
            "numeração das perguntas incorreta"
        )

    for pergunta in perguntas:
        numero = pergunta.get(
            "numero"
        )

        total_perguntas += 1

        texto = pergunta.get(
            "pergunta",
            ""
        ).strip()

        if not texto:
            falha(
                erros,
                f"{nome} #{numero}: "
                "pergunta vazia"
            )

        dica = pergunta.get(
            "dica",
            ""
        ).strip()

        if not dica:
            falha(
                erros,
                f"{nome} #{numero}: "
                "dica vazia"
            )

        alternativas = pergunta.get(
            "alternativas",
            {}
        )

        if set(
            alternativas.keys()
        ) != {"A", "B", "C", "D"}:
            falha(
                erros,
                f"{nome} #{numero}: "
                "alternativas inválidas"
            )

        for letra in "ABCD":
            if not alternativas.get(
                letra,
                ""
            ).strip():
                falha(
                    erros,
                    f"{nome} #{numero}: "
                    f"alternativa {letra} vazia"
                )

        correta = pergunta.get(
            "correta"
        )

        if correta not in "ABCD":
            falha(
                erros,
                f"{nome} #{numero}: "
                "gabarito inválido"
            )
            continue

        respostas[correta] += 1

        resposta_correta = pergunta.get(
            "resposta_correta",
            ""
        ).strip()

        if resposta_correta != alternativas[
            correta
        ].strip():
            falha(
                erros,
                f"{nome} #{numero}: "
                "resposta_correta não corresponde "
                "à alternativa do gabarito"
            )


if len(set(nomes)) != 66:
    falha(
        erros,
        "Existem nomes de livros duplicados"
    )


print()
print("=== AUDITORIA DO BANCO ===")
print("Livros:", len(livros))
print("Perguntas:", total_perguntas)

print(
    "Antigo Testamento:",
    sum(
        1
        for l in livros
        if l.get("testamento")
        == "Antigo Testamento"
    )
)

print(
    "Novo Testamento:",
    sum(
        1
        for l in livros
        if l.get("testamento")
        == "Novo Testamento"
    )
)

print()
print("=== DISTRIBUIÇÃO DAS RESPOSTAS ===")

for letra in "ABCD":
    print(
        f"{letra}:",
        respostas[letra]
    )

print()
print("=== RESULTADO ===")

if erros:
    print(
        "ERROS ENCONTRADOS:",
        len(erros)
    )

    for erro in erros[:50]:
        print("-", erro)

    sys.exit(1)

else:
    print("BANCO APROVADO")
    print("Erros encontrados: 0")
    print("Todas as 1.980 perguntas estão utilizáveis.")
