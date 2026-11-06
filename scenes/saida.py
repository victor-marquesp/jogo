"""Cena: porta de saída (cena final)."""
import answers
import ids
import ui
from engine import Action, Scene, simple_action, travel_action

WRONG_CODE_PENALTY = 5

DESCRIPTION = """
A porta de saída é blindada. Ao lado, um leitor de crachá e um teclado numérico. Uma luz vermelha pisca: LOCKDOWN ATIVO.
"""


def try_exit(game):
    state = game.state
    if not state.has(ids.BADGE):
        ui.narrate("O leitor de crachá continua apagado. Você não tem nenhum crachá de acesso.")
        return
    if not state.has(ids.EXIT_CODE_KNOWN):
        ui.narrate("O crachá é aceito, mas o teclado pede um código de 4 dígitos que você não sabe.")
        return
    if not state.has(ids.VENTILATION):
        ui.narrate("O crachá é aceito, mas o painel informa: LOCKDOWN MANTIDO. EXAUSTÃO DESLIGADA. A porta não abre enquanto o ar não for purgado.")
        return
    ui.narrate("O crachá é aceito. O teclado aguarda o código de liberação.")
    code = ui.prompt("Código (ENTER para desistir)")
    if not code:
        game.free()
        return
    if code == answers.EXIT_CODE:
        state.add(ids.ESCAPED)
        return
    ui.danger("Código incorreto.")
    game.lose_time(WRONG_CODE_PENALTY)


def build() -> Scene:
    return Scene(
        id=ids.EXIT,
        title="PORTA DE SAÍDA",
        description=DESCRIPTION,
        actions=[
            Action("Passar o crachá e digitar o código", try_exit, 3),
            simple_action(
                "Tentar forçar a porta",
                "Você empurra com todo o peso, mas a porta blindada nem estremece. Só gastou o pouco fôlego que tinha.",
                cost=10),
            travel_action("Voltar ao laboratório", ids.LAB, "Você volta pelo corredor."),
        ],
    )
