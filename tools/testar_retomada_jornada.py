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


from app.controlador import ControladorJornada
from app.jornada_estado import EstadoJornada


SAVES = BASE / "saves"


ARQUIVOS = {
    "progresso":
        SAVES / "TESTE_RETOMADA_progresso.json",

    "revisao":
        SAVES / "TESTE_RETOMADA_revisao.json",

    "desafio":
        SAVES / "TESTE_RETOMADA_desafio.json",

    "sequencia":
        SAVES / "TESTE_RETOMADA_sequencia.json",
}


for arquivo in ARQUIVOS.values():

    for caminho in [
        arquivo,
        arquivo.with_name(
            arquivo.name + ".tmp"
        )
    ]:

        if caminho.exists():
            caminho.unlink()


def criar():

    return ControladorJornada(
        arquivo_progresso=
            ARQUIVOS["progresso"],

        arquivo_revisao=
            ARQUIVOS["revisao"],

        arquivo_desafio=
            ARQUIVOS["desafio"],

        arquivo_sequencia=
            ARQUIVOS["sequencia"]
    )


print(
    "=== TESTE DE RETOMADA ==="
)


c = criar()

estado = EstadoJornada(
    c.progresso,
    c.motor.listar_livros()
)


estado.iniciar_livro(
    "Gênesis",
    1
)

c.abrir_livro(
    "Gênesis"
)


# Pergunta 1 correta

q1 = c.motor.pergunta_atual()

c.selecionar_resposta(
    q1["correta"]
)

r1 = c.decidir_mudar(
    "NÃO",
    "2026-10-01"
)

estado.registrar_resposta(
    "Gênesis",
    1,
    r1["acertou"]
)

assert r1["acertou"] is True


c.proxima_pergunta()

estado.salvar_posicao(
    "Gênesis",
    2
)


# Pergunta 2 errada

q2 = c.motor.pergunta_atual()

errada = next(
    letra
    for letra in "ABCD"
    if letra != q2["correta"]
)

c.selecionar_resposta(
    errada
)

r2 = c.decidir_mudar(
    "NÃO",
    "2026-10-01"
)

estado.registrar_resposta(
    "Gênesis",
    2,
    r2["acertou"]
)

assert r2["acertou"] is False


c.proxima_pergunta()

estado.salvar_posicao(
    "Gênesis",
    3
)


assert c.motor.acertos == 1
assert c.motor.erros == 1


print(
    "OK - sessão parcial criada: "
    "1 acerto e 1 erro"
)


# Simular fechamento

del estado
del c


# Abrir novamente

c2 = criar()

estado2 = EstadoJornada(
    c2.progresso,
    c2.motor.listar_livros()
)


posicao = estado2.continuar()

assert (
    posicao["livro"]
    == "Gênesis"
)

assert (
    posicao["pergunta"]
    == 3
)


c2.abrir_livro(
    "Gênesis"
)

c2.motor.indice_pergunta = 2

restaurou = (
    estado2.restaurar_no_motor(
        c2.motor,
        "Gênesis"
    )
)


assert restaurou is True
assert c2.motor.acertos == 1
assert c2.motor.erros == 1


print(
    "OK - voltou exatamente "
    "para Gênesis 3"
)

print(
    "OK - 1 acerto foi preservado"
)

print(
    "OK - 1 erro foi preservado"
)


print()
print(
    "=== RETOMADA DA JORNADA APROVADA ==="
)
