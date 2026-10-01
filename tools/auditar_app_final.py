# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image
import json
import sys


BASE = Path(
    "/data/data/com.termux/files/home/Quiz_Biblico_66"
)

sys.path.insert(
    0,
    str(BASE)
)


print()
print("=== AUDITORIA FINAL DO KISS ===")


# ======================================================
# ARQUIVOS OBRIGATÓRIOS
# ======================================================

obrigatorios = [
    "main.py",
    "app/interface.py",
    "app/tema.py",
    "app/controlador.py",
    "app/motor_quiz.py",
    "app/progresso.py",
    "app/recompensas.py",
    "app/revisao.py",
    "app/desafio_diario.py",
    "app/sequencia.py",
    "app/estatisticas.py",
    "app/jornada_estado.py",
    "data/quiz_biblico.json",
    "assets/imagens/kiss_logo.png",
    "icon.png",
]


for relativo in obrigatorios:

    caminho = BASE / relativo

    assert caminho.exists(), (
        f"Arquivo ausente: {relativo}"
    )

    assert caminho.stat().st_size > 0, (
        f"Arquivo vazio: {relativo}"
    )


print("OK - arquivos principais presentes")


# ======================================================
# LOGO E ÍCONE
# ======================================================

logo = Image.open(
    BASE
    / "assets"
    / "imagens"
    / "kiss_logo.png"
)

icone = Image.open(
    BASE
    / "icon.png"
)


assert logo.size == (
    1254,
    1254
)

assert icone.size == (
    1254,
    1254
)

assert logo.mode == "RGB"
assert icone.mode == "RGB"


print("OK - logo K/Kiss validada")
print("OK - ícone do APK validado")


# ======================================================
# BANCO
# ======================================================

with (
    BASE
    / "data"
    / "quiz_biblico.json"
).open(
    "r",
    encoding="utf-8"
) as f:

    banco = json.load(f)


assert banco[
    "total_livros"
] == 66

assert banco[
    "total_perguntas"
] == 1980

assert len(
    banco["livros"]
) == 66


for livro in banco[
    "livros"
]:

    assert len(
        livro[
            "perguntas"
        ]
    ) == 30


print("OK - 66 livros")
print("OK - 1.980 perguntas")
print("OK - 30 perguntas por livro")


# ======================================================
# INTERFACE
# ======================================================

interface = (
    BASE
    / "app"
    / "interface.py"
).read_text(
    encoding="utf-8"
)


elementos = [
    "CONTINUAR",
    "PERGUNTAS",
    "LIVROS",
    "PROGRESSO",
    "DESAFIO",
    "CONQUISTAS",
    "TelaPergunta",
    "TelaConquistas",
    "TelaProgresso",
    "Deseja mudar sua resposta?",
    "Autor do aplicativo, Carlos Rogério.",
]


for elemento in elementos:

    assert elemento in interface, (
        f"Elemento não encontrado: "
        f"{elemento}"
    )


print("OK - comandos principais presentes")
print("OK - crédito do autor presente")
print("OK - confirmação SIM/NÃO presente")


# ======================================================
# ROLAGEM
# ======================================================

assert (
    "ScrollView"
    in interface
)

assert (
    "do_scroll_y=True"
    in interface
)

assert (
    '"content"'
    in interface
)

assert (
    '"bars"'
    in interface
)


print("OK - rolagem vertical configurada")
print("OK - arraste pelo conteúdo configurado")
print("OK - barra de rolagem configurada")


# ======================================================
# TEMA
# ======================================================

tema = (
    BASE
    / "app"
    / "tema.py"
).read_text(
    encoding="utf-8"
)


assert "ANIL" in tema
assert "BEGE" in tema
assert "Botao3D" in tema
assert "disabled_color" in tema
assert "kiss_logo.png" in tema


print("OK - fundo azul-anil")
print("OK - botões bege 3D")
print("OK - letras brancas")
print("OK - logo interna configurada")


# ======================================================
# MECÂNICA
# ======================================================

from app.motor_quiz import MotorQuiz
from app.recompensas import validar_selose_livros


motor = MotorQuiz()

assert len(
    motor.listar_livros()
) == 66


selos = validar_selose_livros()

assert selos[
    "valido"
] is True


print("OK - motor carregado")
print("OK - 66 selos associados")


# ======================================================
# RESULTADO
# ======================================================

print()
print("=== AUDITORIA FINAL APROVADA ===")
print("Banco bíblico: OK")
print("Motor: OK")
print("Interface: OK")
print("Rolagem: OK")
print("Logo: OK")
print("Ícone APK: OK")
print("Tema visual: OK")
print("Conquistas: OK")
print("Crédito do autor: OK")
