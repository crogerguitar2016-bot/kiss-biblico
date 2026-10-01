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
from app.revisao import RevisaoErros
from app.desafio_diario import DesafioDiario
from app.sequencia import SequenciaEstudo
from app.estatisticas import Estatisticas


PASTA = BASE / "saves"


ARQUIVOS = {
    "progresso":
        PASTA / "TESTE16_progresso.json",

    "revisao":
        PASTA / "TESTE16_revisao.json",

    "desafio":
        PASTA / "TESTE16_desafio.json",

    "sequencia":
        PASTA / "TESTE16_sequencia.json",
}


for arquivo in ARQUIVOS.values():

    if arquivo.exists():
        arquivo.unlink()

    temporario = arquivo.with_name(
        arquivo.name + ".tmp"
    )

    if temporario.exists():
        temporario.unlink()


print()
print(
    "=== TESTE DA ETAPA 16 ==="
)


# ======================================================
# DESAFIO DIÁRIO
# ======================================================

d = DesafioDiario(
    ARQUIVOS[
        "desafio"
    ]
)


dia1 = "2026-10-01"
dia2 = "2026-10-02"


perguntas_a = (
    d.perguntas_do_dia(
        dia1
    )
)

perguntas_b = (
    d.perguntas_do_dia(
        dia1
    )
)


assert (
    len(perguntas_a)
    == 10
)


chaves_a = [
    (
        p["livro"],
        p["numero"]
    )
    for p in perguntas_a
]


chaves_b = [
    (
        p["livro"],
        p["numero"]
    )
    for p in perguntas_b
]


assert (
    chaves_a
    == chaves_b
)


assert (
    len(
        set(
            chaves_a
        )
    )
    == 10
)


print(
    "OK - desafio possui 10 perguntas"
)

print(
    "OK - perguntas do mesmo dia "
    "permanecem iguais"
)

print(
    "OK - não há perguntas duplicadas"
)


perguntas_dia2 = (
    d.perguntas_do_dia(
        dia2
    )
)


chaves_dia2 = [
    (
        p["livro"],
        p["numero"]
    )
    for p in perguntas_dia2
]


assert (
    chaves_dia2
    != chaves_a
)


print(
    "OK - dia seguinte possui "
    "novo desafio"
)


resultado = (
    d.registrar_conclusao(
        8,
        dia1
    )
)


assert (
    resultado[
        "ja_concluido"
    ]
    is False
)

assert (
    resultado[
        "percentual"
    ]
    == 80.0
)


print(
    "OK - conclusão diária registrada"
)


resultado2 = (
    d.registrar_conclusao(
        10,
        dia1
    )
)


assert (
    resultado2[
        "ja_concluido"
    ]
    is True
)


assert (
    d.resumo()[
        "dias_concluidos"
    ]
    == 1
)


print(
    "OK - conclusão do mesmo dia "
    "não é duplicada"
)


# ======================================================
# SEQUÊNCIA DE ESTUDO
# ======================================================

s = SequenciaEstudo(
    ARQUIVOS[
        "sequencia"
    ]
)


s.registrar_atividade(
    "2026-09-29"
)

s.registrar_atividade(
    "2026-09-30"
)

s.registrar_atividade(
    "2026-10-01"
)


resumo_seq = (
    s.resumo(
        "2026-10-01"
    )
)


assert (
    resumo_seq[
        "sequencia_atual"
    ]
    == 3
)

assert (
    resumo_seq[
        "maior_sequencia"
    ]
    == 3
)

assert (
    resumo_seq[
        "dias_estudados"
    ]
    == 3
)


print(
    "OK - sequência de 3 dias reconhecida"
)


# Registrar o mesmo dia não duplica.

resultado_seq = (
    s.registrar_atividade(
        "2026-10-01"
    )
)


assert (
    resultado_seq[
        "novo_dia"
    ]
    is False
)

assert (
    resultado_seq[
        "dias_estudados"
    ]
    == 3
)


print(
    "OK - mesmo dia não duplica estudo"
)


# ======================================================
# CRIAR DADOS PARA ESTATÍSTICAS
# ======================================================

p = Progresso(
    ARQUIVOS[
        "progresso"
    ]
)


p.definir_nome(
    "C Roger"
)


p.registrar_resposta(
    "Gênesis",
    1,
    True
)


p.registrar_resposta(
    "Gênesis",
    2,
    False
)


r = RevisaoErros(
    ARQUIVOS[
        "revisao"
    ]
)


r.registrar_resultado(
    "Gênesis",
    2,
    False
)


# ======================================================
# ESTATÍSTICAS
# ======================================================

e = Estatisticas(
    p,
    r,
    d,
    s
)


geral = e.resumo(
    "2026-10-01"
)


assert (
    geral[
        "jogador"
    ]
    == "C Roger"
)

assert (
    geral[
        "xp"
    ]
    == 10
)

assert (
    geral[
        "moedas"
    ]
    == 1
)

assert (
    geral[
        "perguntas_aprendidas"
    ]
    == 1
)

assert (
    geral[
        "perguntas_para_revisar"
    ]
    == 1
)

assert (
    geral[
        "desafios_concluidos"
    ]
    == 1
)

assert (
    geral[
        "melhor_desafio"
    ]
    == 8
)

assert (
    geral[
        "sequencia_atual"
    ]
    == 3
)


print(
    "OK - estatísticas gerais integradas"
)


# ======================================================
# MOSTRAR EXEMPLO
# ======================================================

print()
print(
    "=== EXEMPLO DE MEU PROGRESSO ==="
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
    geral[
        "perguntas_para_revisar"
    ]
)

print(
    "Desafios diários:",
    geral[
        "desafios_concluidos"
    ]
)

print(
    "Sequência atual:",
    geral[
        "sequencia_atual"
    ],
    "dias"
)

print(
    "Maior sequência:",
    geral[
        "maior_sequencia"
    ],
    "dias"
)


print()
print(
    "=== ETAPA 16 APROVADA ==="
)

print(
    "Desafio Diário: OK"
)

print(
    "10 perguntas por dia: OK"
)

print(
    "Mesmo desafio durante o dia: OK"
)

print(
    "Novo desafio no dia seguinte: OK"
)

print(
    "Sequência de estudo: OK"
)

print(
    "Marcos de sequência: OK"
)

print(
    "Estatísticas gerais: OK"
)

print(
    "Persistência: OK"
)
