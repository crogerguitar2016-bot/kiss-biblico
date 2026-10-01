# -*- coding: utf-8 -*-

import sys
from pathlib import Path

BASE = Path(
    "/data/data/com.termux/files/home/Quiz_Biblico_66"
)

sys.path.insert(0, str(BASE))

from app.motor_quiz import MotorQuiz


print("=== TESTE DO MOTOR DO QUIZ ===")

motor = MotorQuiz()


# 1. Banco
assert len(motor.listar_livros()) == 66
print("OK - 66 livros carregados")


# 2. Abrir Gênesis
assert motor.abrir_livro("Gênesis")
assert motor.pergunta_atual()["numero"] == 1
print("OK - Gênesis aberto")


# 3. Selecionar alternativa errada
resultado = motor.selecionar_resposta("A")

assert resultado["estado"] == "aguardando_confirmacao"
assert resultado["pergunta"] == "Deseja mudar sua resposta?"

print("OK - pergunta 'Deseja mudar sua resposta?' acionada")


# 4. Responder SIM
resultado = motor.decidir_mudar("SIM")

assert resultado["estado"] == "mudar_resposta"
assert motor.resposta_selecionada is None

print("OK - SIM permite mudar sem corrigir")


# 5. Escolher D
resultado = motor.selecionar_resposta("D")

assert resultado["estado"] == "aguardando_confirmacao"

print("OK - nova alternativa selecionada")


# 6. Responder NÃO
resultado = motor.decidir_mudar("NÃO")

assert resultado["estado"] == "confirmada"
assert resultado["acertou"] is True
assert resultado["correta"] == "D"

print("OK - NÃO confirma definitivamente")
print("OK - resposta correta reconhecida")


# 7. Conferir pontuação
assert motor.acertos == 1
assert motor.erros == 0

print("OK - acerto registrado")


# 8. Ir à próxima
resultado = motor.proxima_pergunta()

assert resultado["estado"] == "proxima_pergunta"
assert motor.pergunta_atual()["numero"] == 2

print("OK - avançou para pergunta 2")


# 9. Testar erro confirmado
correta = motor.pergunta_atual()["correta"]

errada = next(
    letra
    for letra in "ABCD"
    if letra != correta
)

motor.selecionar_resposta(errada)

resultado = motor.decidir_mudar("NÃO")

assert resultado["acertou"] is False
assert motor.acertos == 1
assert motor.erros == 1

print("OK - resposta errada registrada")


# 10. Não pode responder novamente
try:
    motor.selecionar_resposta("A")
    raise AssertionError(
        "Era esperado bloquear nova resposta."
    )
except RuntimeError:
    pass

print("OK - resposta confirmada fica bloqueada")


print()
print("=== ETAPA 12 APROVADA ===")
print("Motor do quiz funcionando.")
print()
print("Fluxo confirmado:")
print("Escolher A/B/C/D")
print("        ↓")
print("Deseja mudar sua resposta?")
print("        ↓")
print("SIM -> volta para escolher")
print("NÃO -> confirma")
print("        ↓")
print("mostra certo ou errado")
print("        ↓")
print("próxima pergunta")
