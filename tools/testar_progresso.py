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


from app.progresso import Progresso


ARQUIVO_TESTE = (
    BASE
    / "saves"
    / "progresso_TESTE.json"
)


# ======================================================
# LIMPEZA DE TESTE ANTERIOR
# ======================================================

for caminho in [
    ARQUIVO_TESTE,
    ARQUIVO_TESTE.with_name(
        ARQUIVO_TESTE.name
        + ".tmp"
    ),
    ARQUIVO_TESTE.with_name(
        ARQUIVO_TESTE.stem
        + "_CORROMPIDO"
        + ARQUIVO_TESTE.suffix
    )
]:

    if caminho.exists():
        caminho.unlink()


print()
print(
    "=== TESTE DO PROGRESSO ==="
)


# ======================================================
# TESTE 1
# CRIAÇÃO DO SAVE
# ======================================================

p = Progresso(
    ARQUIVO_TESTE
)

assert ARQUIVO_TESTE.exists()

resumo = p.resumo()

assert resumo["nome"] == ""
assert resumo["xp"] == 0
assert resumo["moedas"] == 0
assert resumo["livros_concluidos"] == 0
assert resumo["respostas_confirmadas"] == 0
assert resumo["acertos"] == 0
assert resumo["erros"] == 0

print(
    "OK - arquivo de progresso criado"
)


# ======================================================
# TESTE 2
# NOME DO JOGADOR
# ======================================================

assert (
    p.jogador_tem_nome()
    is False
)

nome = p.definir_nome(
    "Carlos Rogério"
)

assert nome == "Carlos Rogério"

assert (
    p.nome_jogador()
    == "Carlos Rogério"
)

assert (
    p.jogador_tem_nome()
    is True
)

print(
    "OK - nome do jogador salvo"
)


# ======================================================
# TESTE 3
# ALTERAR NOME
# ======================================================

nome = p.definir_nome(
    "C Roger"
)

assert nome == "C Roger"

assert (
    p.nome_jogador()
    == "C Roger"
)

print(
    "OK - nome do jogador pode ser alterado"
)


# ======================================================
# TESTE 4
# PRIMEIRO ACERTO
# ======================================================

resultado = p.registrar_resposta(
    "Gênesis",
    1,
    True
)

assert (
    resultado[
        "ganhou_xp"
    ]
    == 10
)

assert (
    resultado[
        "ganhou_moedas"
    ]
    == 1
)

assert (
    p.resumo()[
        "xp"
    ]
    == 10
)

assert (
    p.resumo()[
        "moedas"
    ]
    == 1
)

print(
    "OK - primeiro acerto gera 10 XP"
)

print(
    "OK - primeiro acerto gera 1 moeda"
)


# ======================================================
# TESTE 5
# REPETIR A MESMA QUESTÃO
# ======================================================

resultado = p.registrar_resposta(
    "Gênesis",
    1,
    True
)

assert (
    resultado[
        "ganhou_xp"
    ]
    == 0
)

assert (
    resultado[
        "ganhou_moedas"
    ]
    == 0
)

assert (
    p.resumo()[
        "xp"
    ]
    == 10
)

assert (
    p.resumo()[
        "moedas"
    ]
    == 1
)

print(
    "OK - mesma pergunta "
    "não duplica recompensa"
)


# ======================================================
# TESTE 6
# REGISTRAR ERRO
# ======================================================

p.registrar_resposta(
    "Gênesis",
    2,
    False
)

assert (
    p.resumo()[
        "erros"
    ]
    == 1
)

print(
    "OK - resposta errada registrada"
)


# ======================================================
# TESTE 7
# APRENDER DEPOIS
# ======================================================

resultado = p.registrar_resposta(
    "Gênesis",
    2,
    True
)

assert (
    resultado[
        "ganhou_xp"
    ]
    == 10
)

assert (
    resultado[
        "ganhou_moedas"
    ]
    == 1
)

assert (
    p.resumo()[
        "xp"
    ]
    == 20
)

assert (
    p.resumo()[
        "moedas"
    ]
    == 2
)

print(
    "OK - pergunta errada "
    "pode ser aprendida depois"
)


# ======================================================
# TESTE 8
# STATUS DE GÊNESIS
# ======================================================

status = p.status_livro(
    "Gênesis"
)

assert (
    status[
        "respondidas_unicas"
    ]
    == 2
)

assert (
    status[
        "acertos_unicos"
    ]
    == 2
)

assert (
    status[
        "concluido"
    ]
    is False
)

print(
    "OK - progresso por livro funciona"
)


# ======================================================
# TESTE 9
# CONCLUIR LIVRO
# ======================================================

status = p.concluir_livro(
    "Gênesis",
    25
)

assert (
    status[
        "concluido"
    ]
    is True
)

assert (
    status[
        "tentativas"
    ]
    == 1
)

assert (
    status[
        "melhor_acertos"
    ]
    == 25
)

print(
    "OK - livro concluído"
)


# ======================================================
# TESTE 10
# REFAZER COM RESULTADO MENOR
# ======================================================

status = p.concluir_livro(
    "Gênesis",
    20
)

assert (
    status[
        "tentativas"
    ]
    == 2
)

assert (
    status[
        "melhor_acertos"
    ]
    == 25
)

print(
    "OK - melhor resultado foi preservado"
)


# ======================================================
# TESTE 11
# RESUMO GERAL
# ======================================================

resumo = p.resumo()

assert (
    resumo[
        "livros_concluidos"
    ]
    == 1
)

assert (
    resumo[
        "respostas_confirmadas"
    ]
    == 4
)

assert (
    resumo[
        "acertos"
    ]
    == 3
)

assert (
    resumo[
        "erros"
    ]
    == 1
)

assert (
    resumo[
        "percentual_acertos"
    ]
    == 75.0
)

print(
    "OK - estatísticas gerais corretas"
)


# ======================================================
# TESTE 12
# PERSISTÊNCIA APÓS FECHAR
# ======================================================

del p


p2 = Progresso(
    ARQUIVO_TESTE
)


assert (
    p2.nome_jogador()
    == "C Roger"
)

assert (
    p2.resumo()[
        "xp"
    ]
    == 20
)

assert (
    p2.resumo()[
        "moedas"
    ]
    == 2
)

assert (
    p2.resumo()[
        "livros_concluidos"
    ]
    == 1
)

assert (
    p2.status_livro(
        "Gênesis"
    )[
        "melhor_acertos"
    ]
    == 25
)

assert (
    p2.status_livro(
        "Gênesis"
    )[
        "tentativas"
    ]
    == 2
)

print(
    "OK - nome permanece salvo "
    "após fechar"
)

print(
    "OK - XP permanece salvo "
    "após fechar"
)

print(
    "OK - moedas permanecem salvas "
    "após fechar"
)

print(
    "OK - progresso dos livros "
    "permanece salvo"
)


# ======================================================
# RESULTADO
# ======================================================

print()
print(
    "=== ETAPA 13 APROVADA ==="
)

print(
    "Sistema de progresso permanente "
    "funcionando."
)

print()
print(
    "Nome do jogador: OK"
)

print(
    "Alteração do nome: OK"
)

print(
    "Persistência do nome: OK"
)

print(
    "XP: OK"
)

print(
    "Moedas: OK"
)

print(
    "Acertos e erros: OK"
)

print(
    "Perguntas aprendidas: OK"
)

print(
    "Livros concluídos: OK"
)

print(
    "Número de tentativas: OK"
)

print(
    "Melhor resultado: OK"
)

print(
    "Estatísticas: OK"
)

print(
    "Persistência em arquivo: OK"
)

print()
print(
    "Arquivo usado somente no teste:"
)

print(
    ARQUIVO_TESTE
)
