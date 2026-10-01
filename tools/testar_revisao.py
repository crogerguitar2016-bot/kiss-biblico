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


from app.revisao import RevisaoErros


ARQUIVO_TESTE = (
    BASE
    / "saves"
    / "perguntas_erradas_TESTE.json"
)


for caminho in [
    ARQUIVO_TESTE,

    ARQUIVO_TESTE.with_name(
        ARQUIVO_TESTE.name
        + ".tmp"
    )
]:

    if caminho.exists():
        caminho.unlink()


print()
print(
    "=== TESTE PERGUNTAS QUE ERREI ==="
)


# ------------------------------------------------------
# 1. Criar arquivo
# ------------------------------------------------------

r = RevisaoErros(
    ARQUIVO_TESTE
)

assert (
    r.total_pendentes()
    == 0
)

print(
    "OK - revisão inicialmente vazia"
)


# ------------------------------------------------------
# 2. Errar Gênesis 1
# ------------------------------------------------------

resultado = r.registrar_resultado(
    "Gênesis",
    1,
    False
)

assert (
    resultado[
        "entrou_na_revisao"
    ]
    is True
)

assert (
    r.total_pendentes()
    == 1
)

print(
    "OK - pergunta errada entra na revisão"
)


# ------------------------------------------------------
# 3. Errar a mesma novamente
# ------------------------------------------------------

r.registrar_resultado(
    "Gênesis",
    1,
    False
)

assert (
    r.total_pendentes()
    == 1
)

print(
    "OK - pergunta não é duplicada"
)


# ------------------------------------------------------
# 4. Errar outra pergunta
# ------------------------------------------------------

r.registrar_resultado(
    "Gênesis",
    2,
    False
)

assert (
    r.total_pendentes()
    == 2
)

print(
    "OK - segunda pergunta registrada"
)


# ------------------------------------------------------
# 5. Erro em outro livro
# ------------------------------------------------------

r.registrar_resultado(
    "Êxodo",
    9,
    False
)

assert (
    r.total_pendentes()
    == 3
)

assert (
    len(
        r.livros_com_erros()
    )
    == 2
)

print(
    "OK - erros separados por livro"
)


# ------------------------------------------------------
# 6. Conferir perguntas de Gênesis
# ------------------------------------------------------

numeros = (
    r.numeros_pendentes(
        "Gênesis"
    )
)

assert numeros == [
    1,
    2
]

perguntas = (
    r.perguntas_do_livro(
        "Gênesis"
    )
)

assert (
    len(perguntas)
    == 2
)

assert (
    perguntas[0][
        "numero"
    ]
    == 1
)

assert (
    perguntas[0][
        "correta"
    ]
    == "D"
)

print(
    "OK - perguntas reais recuperadas "
    "do banco de 1.980 questões"
)


# ------------------------------------------------------
# 7. Acertar uma questão anteriormente errada
# ------------------------------------------------------

resultado = r.registrar_resultado(
    "Gênesis",
    1,
    True
)

assert (
    resultado[
        "saiu_da_revisao"
    ]
    is True
)

assert (
    r.numeros_pendentes(
        "Gênesis"
    )
    == [2]
)

assert (
    r.total_pendentes()
    == 2
)

print(
    "OK - questão aprendida sai da revisão"
)


# ------------------------------------------------------
# 8. Acertar questão que nunca estava errada
# ------------------------------------------------------

resultado = r.registrar_resultado(
    "Gênesis",
    3,
    True
)

assert (
    resultado[
        "saiu_da_revisao"
    ]
    is False
)

assert (
    r.total_pendentes()
    == 2
)

print(
    "OK - acerto normal não altera "
    "a lista indevidamente"
)


# ------------------------------------------------------
# 9. Todas as perguntas
# ------------------------------------------------------

todas = (
    r.todas_as_perguntas()
)

assert (
    len(todas)
    == 2
)

print(
    "OK - revisão geral reúne "
    "todos os livros"
)


# ------------------------------------------------------
# 10. Persistência
# ------------------------------------------------------

del r


r2 = RevisaoErros(
    ARQUIVO_TESTE
)

assert (
    r2.total_pendentes()
    == 2
)

assert (
    r2.numeros_pendentes(
        "Gênesis"
    )
    == [2]
)

assert (
    r2.numeros_pendentes(
        "Êxodo"
    )
    == [9]
)

print(
    "OK - perguntas erradas "
    "continuam salvas após fechar"
)


# ------------------------------------------------------
# 11. Resolver tudo
# ------------------------------------------------------

r2.registrar_resultado(
    "Gênesis",
    2,
    True
)

r2.registrar_resultado(
    "Êxodo",
    9,
    True
)

assert (
    r2.total_pendentes()
    == 0
)

assert (
    r2.livros_com_erros()
    == []
)

print(
    "OK - lista fica vazia "
    "quando todas são aprendidas"
)


print()
print(
    "=== ETAPA 15 APROVADA ==="
)

print(
    "Sistema Perguntas que errei "
    "funcionando."
)

print()
print(
    "Registrar erro: OK"
)

print(
    "Não duplicar erro: OK"
)

print(
    "Separar por livro: OK"
)

print(
    "Buscar pergunta original: OK"
)

print(
    "Revisão geral: OK"
)

print(
    "Remover após acertar: OK"
)

print(
    "Persistência: OK"
)
