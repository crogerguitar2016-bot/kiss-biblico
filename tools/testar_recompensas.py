# -*- coding: utf-8 -*-

import sys
from pathlib import Path


BASE = Path(
    "/data/data/com.termux/files/home/Quiz_Biblico_66"
)

sys.path.insert(
    0,
    str(BASE)
)


from app.recompensas import (
    Recompensas,
    validar_selose_livros
)


print()
print(
    "=== TESTE DAS RECOMPENSAS ==="
)


# ======================================================
# 1. CONFERIR 66 SELOS
# ======================================================

validacao = (
    validar_selose_livros()
)

assert (
    validacao[
        "livros_banco"
    ]
    == 66
)

assert (
    validacao[
        "selos"
    ]
    == 66
)

assert (
    validacao[
        "faltando"
    ]
    == []
)

assert (
    validacao[
        "sobrando"
    ]
    == []
)

assert (
    validacao[
        "valido"
    ]
    is True
)

print(
    "OK - os 66 livros possuem selo"
)


# ======================================================
# 2. TESTAR ESTRELAS
# ======================================================

assert (
    Recompensas.calcular_estrelas(0)
    == 0
)

assert (
    Recompensas.calcular_estrelas(17)
    == 0
)

assert (
    Recompensas.calcular_estrelas(18)
    == 1
)

assert (
    Recompensas.calcular_estrelas(23)
    == 1
)

assert (
    Recompensas.calcular_estrelas(24)
    == 2
)

assert (
    Recompensas.calcular_estrelas(28)
    == 2
)

assert (
    Recompensas.calcular_estrelas(29)
    == 3
)

assert (
    Recompensas.calcular_estrelas(30)
    == 3
)

print(
    "OK - sistema de estrelas"
)


# ======================================================
# 3. SELO DE GÊNESIS
# ======================================================

assert (
    Recompensas.selo_do_livro(
        "Gênesis"
    )
    == "Selo das Origens"
)

print(
    "OK - selo específico por livro"
)


# ======================================================
# 4. RECOMPENSA COM 1 ESTRELA
# ======================================================

r1 = (
    Recompensas
    .montar_recompensa(
        "C Roger",
        "Gênesis",
        20
    )
)

assert (
    r1[
        "jogador"
    ]
    == "C Roger"
)

assert (
    r1[
        "livro"
    ]
    == "Gênesis"
)

assert (
    r1[
        "estrelas"
    ]
    == 1
)

assert (
    r1[
        "selo"
    ]
    == "Selo das Origens"
)

assert (
    "C Roger"
    in r1[
        "mensagem"
    ]
)

assert (
    "Gênesis"
    in r1[
        "pergaminho"
    ][
        "texto"
    ]
)

print(
    "OK - nome do jogador "
    "entra na recompensa"
)

print(
    "OK - mensagem personalizada"
)

print(
    "OK - pergaminho personalizado"
)


# ======================================================
# 5. RECOMPENSA COM 2 ESTRELAS
# ======================================================

r2 = (
    Recompensas
    .montar_recompensa(
        "C Roger",
        "João",
        26
    )
)

assert (
    r2[
        "estrelas"
    ]
    == 2
)

assert (
    r2[
        "selo"
    ]
    == "Selo da Vida"
)

print(
    "OK - recompensa de duas estrelas"
)


# ======================================================
# 6. RECOMPENSA MÁXIMA
# ======================================================

r3 = (
    Recompensas
    .montar_recompensa(
        "C Roger",
        "Apocalipse",
        30
    )
)

assert (
    r3[
        "estrelas"
    ]
    == 3
)

assert (
    r3[
        "percentual"
    ]
    == 100.0
)

assert (
    r3[
        "selo"
    ]
    == "Selo da Vitória"
)

assert (
    r3[
        "proxima_meta"
    ][
        "faltam"
    ]
    == 0
)

print(
    "OK - recompensa máxima"
)


# ======================================================
# 7. TESTAR META SEGUINTE
# ======================================================

meta = (
    Recompensas
    .proxima_meta(
        20
    )
)

assert (
    meta[
        "acertos_necessarios"
    ]
    == 24
)

assert (
    meta[
        "faltam"
    ]
    == 4
)

print(
    "OK - próxima meta calculada"
)


# ======================================================
# MOSTRAR EXEMPLO REAL
# ======================================================

print()
print(
    "=== EXEMPLO DE RECOMPENSA ==="
)

exemplo = (
    Recompensas
    .montar_recompensa(
        "C Roger",
        "Gênesis",
        26
    )
)

print(
    "Jogador:",
    exemplo[
        "jogador"
    ]
)

print(
    "Livro:",
    exemplo[
        "livro"
    ]
)

print(
    "Resultado:",
    f'{exemplo["acertos"]}/30'
)

print(
    "Aproveitamento:",
    f'{exemplo["percentual"]}%'
)

print(
    "Estrelas:",
    exemplo[
        "estrelas_texto"
    ]
)

print(
    "Selo:",
    exemplo[
        "selo"
    ]
)

print(
    "Mensagem:",
    exemplo[
        "mensagem"
    ]
)


print()
print(
    "=== ETAPA 14 APROVADA ==="
)

print(
    "Sistema de recompensas funcionando."
)

print()
print(
    "66 selos: OK"
)

print(
    "Estrelas: OK"
)

print(
    "Mensagens personalizadas: OK"
)

print(
    "Nome do jogador: OK"
)

print(
    "Pergaminho de conquista: OK"
)

print(
    "Próxima meta: OK"
)
