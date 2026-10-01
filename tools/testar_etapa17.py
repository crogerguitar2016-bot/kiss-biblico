# -*- coding: utf-8 -*-

import sys
from pathlib import Path


BASE = Path(
    "/data/data/com.termux/files/home/Quiz_Biblico_66"
)

sys.path.insert(0, str(BASE))


from app.controlador import ControladorJornada


PASTA = BASE / "saves"

ARQUIVOS = {
    "progresso":
        PASTA / "TESTE17_progresso.json",

    "revisao":
        PASTA / "TESTE17_revisao.json",

    "desafio":
        PASTA / "TESTE17_desafio.json",

    "sequencia":
        PASTA / "TESTE17_sequencia.json",
}


# ======================================================
# LIMPAR TESTES ANTIGOS
# ======================================================

for arquivo in ARQUIVOS.values():

    candidatos = [
        arquivo,
        arquivo.with_name(
            arquivo.name + ".tmp"
        )
    ]

    for caminho in candidatos:

        if caminho.exists():
            caminho.unlink()


print()
print("=== TESTE DA ETAPA 17 ===")


# ======================================================
# CRIAR CONTROLADOR
# ======================================================

c = ControladorJornada(
    arquivo_progresso=
        ARQUIVOS["progresso"],

    arquivo_revisao=
        ARQUIVOS["revisao"],

    arquivo_desafio=
        ARQUIVOS["desafio"],

    arquivo_sequencia=
        ARQUIVOS["sequencia"]
)


# ======================================================
# 1. NOME DO JOGADOR
# ======================================================

c.definir_nome(
    "C Roger"
)

assert (
    c.nome_jogador()
    == "C Roger"
)

print(
    "OK - nome do jogador integrado"
)


# ======================================================
# 2. ABRIR GÊNESIS
# ======================================================

resultado = c.abrir_livro(
    "Gênesis"
)

assert (
    resultado["estado"]
    == "livro_aberto"
)

assert (
    resultado["total_perguntas"]
    == 30
)

print(
    "OK - Gênesis aberto com 30 perguntas"
)


# ======================================================
# 3. GABARITO NÃO DEVE IR PARA INTERFACE
# ======================================================

publica = c.pergunta_atual()

assert "correta" not in publica
assert "resposta_correta" not in publica
assert "texto_gabarito" not in publica

print(
    "OK - resposta correta fica oculta"
)


# ======================================================
# 4. ESCOLHER E DECIDIR MUDAR
# ======================================================

c.selecionar_resposta(
    "A"
)

resultado = c.decidir_mudar(
    "SIM",
    "2026-10-01"
)

assert (
    resultado["estado"]
    == "mudar_resposta"
)

assert (
    c.progresso.resumo()[
        "respostas_confirmadas"
    ]
    == 0
)

print(
    "OK - SIM volta para alternativas "
    "sem registrar resposta"
)


# ======================================================
# 5. CONFIRMAR Q1 CORRETA
# ======================================================

correta = (
    c.motor
    .pergunta_atual()[
        "correta"
    ]
)

c.selecionar_resposta(
    correta
)

resultado = c.decidir_mudar(
    "NÃO",
    "2026-10-01"
)

assert resultado["acertou"] is True
assert resultado["xp_ganho"] == 10
assert resultado["moedas_ganhas"] == 1
assert resultado["sequencia_atual"] == 1

print(
    "OK - NÃO confirma resposta"
)

print(
    "OK - acerto gera XP e moeda"
)

print(
    "OK - sequência de estudo integrada"
)


# ======================================================
# 6. PERGUNTA 2 ERRADA
# ======================================================

c.proxima_pergunta()

pergunta2 = (
    c.motor
    .pergunta_atual()
)

assert (
    pergunta2["numero"]
    == 2
)

correta2 = pergunta2[
    "correta"
]

errada2 = next(
    letra
    for letra in "ABCD"
    if letra != correta2
)

c.selecionar_resposta(
    errada2
)

resultado = c.decidir_mudar(
    "NÃO",
    "2026-10-01"
)

assert resultado["acertou"] is False
assert resultado["entrou_na_revisao"] is True

assert (
    c.revisao
    .numeros_pendentes(
        "Gênesis"
    )
    == [2]
)

print(
    "OK - erro entra em Perguntas que errei"
)


# ======================================================
# 7. PERGUNTAS 3 ATÉ 30 CORRETAS
# ======================================================

for numero in range(
    3,
    31
):

    c.proxima_pergunta()

    pergunta = (
        c.motor
        .pergunta_atual()
    )

    assert (
        pergunta["numero"]
        == numero
    )

    correta = pergunta[
        "correta"
    ]

    c.selecionar_resposta(
        correta
    )

    resultado = c.decidir_mudar(
        "NÃO",
        "2026-10-01"
    )

    assert (
        resultado["acertou"]
        is True
    )


print(
    "OK - todas as 30 perguntas processadas"
)


# ======================================================
# 8. CONCLUIR O LIVRO
# ======================================================

final = c.proxima_pergunta()

assert (
    final["estado"]
    == "livro_concluido"
)

assert final["acertos"] == 29
assert final["erros"] == 1

assert (
    final[
        "recompensa"
    ][
        "estrelas"
    ]
    == 3
)

assert (
    final[
        "recompensa"
    ][
        "selo"
    ]
    == "Selo das Origens"
)

assert (
    final[
        "status"
    ][
        "concluido"
    ]
    is True
)

print(
    "OK - livro concluído"
)

print(
    "OK - 3 estrelas calculadas"
)

print(
    "OK - Selo das Origens concedido"
)

print(
    "OK - pergaminho preparado"
)


# ======================================================
# 9. PONTUAÇÃO DO LIVRO
# ======================================================

resumo = (
    c.progresso
    .resumo()
)

assert resumo["xp"] == 290
assert resumo["moedas"] == 29

assert (
    c.revisao
    .total_pendentes()
    == 1
)

print(
    "OK - XP do livro correto"
)

print(
    "OK - moedas do livro corretas"
)


# ======================================================
# 10. ABRIR REVISÃO
# ======================================================

resultado = c.abrir_revisao(
    "Gênesis"
)

assert (
    resultado["estado"]
    == "revisao_aberta"
)

assert (
    resultado["total_perguntas"]
    == 1
)

assert (
    c.pergunta_atual()[
        "numero"
    ]
    == 2
)

print(
    "OK - Perguntas que errei aberta"
)


# ======================================================
# 11. ACERTAR Q2 NA REVISÃO
# ======================================================

correta = (
    c.motor
    .pergunta_atual()[
        "correta"
    ]
)

c.selecionar_resposta(
    correta
)

resultado = c.decidir_mudar(
    "NÃO",
    "2026-10-01"
)

assert resultado["acertou"] is True
assert resultado["saiu_da_revisao"] is True
assert resultado["xp_ganho"] == 10

assert (
    c.revisao
    .total_pendentes()
    == 0
)

assert (
    c.progresso
    .resumo()[
        "xp"
    ]
    == 300
)

print(
    "OK - pergunta aprendida sai da revisão"
)

print(
    "OK - primeiro acerto posterior gera recompensa"
)


final_revisao = (
    c.proxima_pergunta()
)

assert (
    final_revisao["estado"]
    == "revisao_concluida"
)

print(
    "OK - revisão concluída"
)


# ======================================================
# 12. DESAFIO DIÁRIO
# ======================================================

resultado = c.abrir_desafio(
    "2026-10-01"
)

assert (
    resultado["estado"]
    == "desafio_aberto"
)

assert (
    resultado["total_perguntas"]
    == 10
)

print(
    "OK - Desafio Diário aberto"
)


for posicao in range(
    1,
    11
):

    pergunta = (
        c.motor
        .pergunta_atual()
    )

    correta = pergunta[
        "correta"
    ]

    c.selecionar_resposta(
        correta
    )

    resposta = c.decidir_mudar(
        "NÃO",
        "2026-10-01"
    )

    assert (
        resposta["acertou"]
        is True
    )

    final_desafio = (
        c.proxima_pergunta()
    )

    if posicao < 10:

        assert (
            final_desafio["estado"]
            == "proxima_pergunta"
        )


assert (
    final_desafio["estado"]
    == "desafio_concluido"
)

assert (
    final_desafio["acertos"]
    == 10
)

assert (
    final_desafio[
        "resultado"
    ][
        "percentual"
    ]
    == 100.0
)

print(
    "OK - Desafio Diário concluído com 10/10"
)


# ======================================================
# 13. MEU PROGRESSO
# ======================================================

geral = c.meu_progresso(
    "2026-10-01"
)

assert (
    geral["jogador"]
    == "C Roger"
)

assert (
    geral["livros_concluidos"]
    == 1
)

assert (
    geral["perguntas_para_revisar"]
    == 0
)

assert (
    geral["desafios_concluidos"]
    == 1
)

assert (
    geral["sequencia_atual"]
    == 1
)

print(
    "OK - Meu Progresso integrado"
)


# ======================================================
# 14. PERSISTÊNCIA
# ======================================================

del c


c2 = ControladorJornada(
    arquivo_progresso=
        ARQUIVOS["progresso"],

    arquivo_revisao=
        ARQUIVOS["revisao"],

    arquivo_desafio=
        ARQUIVOS["desafio"],

    arquivo_sequencia=
        ARQUIVOS["sequencia"]
)


assert (
    c2.nome_jogador()
    == "C Roger"
)

assert (
    c2.progresso
    .status_livro(
        "Gênesis"
    )[
        "concluido"
    ]
    is True
)

assert (
    c2.revisao
    .total_pendentes()
    == 0
)

assert (
    c2.desafio
    .concluido_em(
        "2026-10-01"
    )
    is True
)

print(
    "OK - integração permanece salva "
    "após fechar"
)


# ======================================================
# RESULTADO
# ======================================================

geral = c2.meu_progresso(
    "2026-10-01"
)


print()
print(
    "=== RESUMO FINAL ==="
)

print(
    "Jogador:",
    geral["jogador"]
)

print(
    "XP:",
    geral["xp"]
)

print(
    "Moedas:",
    geral["moedas"]
)

print(
    "Livros:",
    f'{geral["livros_concluidos"]}/66'
)

print(
    "Perguntas aprendidas:",
    f'{geral["perguntas_aprendidas"]}/1980'
)

print(
    "Para revisar:",
    geral["perguntas_para_revisar"]
)

print(
    "Desafios:",
    geral["desafios_concluidos"]
)

print(
    "Sequência:",
    geral["sequencia_atual"],
    "dia"
)


print()
print(
    "=== ETAPA 17 APROVADA ==="
)

print(
    "Motor central: OK"
)

print(
    "Nome do jogador: OK"
)

print(
    "Confirmação SIM/NÃO: OK"
)

print(
    "Gabarito oculto: OK"
)

print(
    "Progresso: OK"
)

print(
    "XP e moedas: OK"
)

print(
    "Perguntas que errei: OK"
)

print(
    "Revisão: OK"
)

print(
    "Sequência: OK"
)

print(
    "Conclusão de livro: OK"
)

print(
    "Estrelas e selos: OK"
)

print(
    "Pergaminho: OK"
)

print(
    "Desafio Diário: OK"
)

print(
    "Meu Progresso: OK"
)

print(
    "Persistência: OK"
)

print(
    "Integração geral: OK"
)
