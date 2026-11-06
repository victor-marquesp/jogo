"""Cena inicial: o laboratório (hub do jogo)."""
import answers
import ids
import ui
from engine import Action, Scene, all_of, always, has, lacks, simple_action, travel_action

WRONG_CODE_PENALTY = 5

DESCRIPTION = """
Bancadas de aço inox, vidrarias espalhadas, o cheiro químico impregnado no ar. Na parede, um relógio analógico marca a passagem do tempo. Ao lado dele, um pôster de reciclagem. Numa lousa, rabiscos de fórmulas. Um pequeno cofre está embutido na parede.

Há três portas: uma aberta para o escritório, uma trancada para a sala do reator e, ao fundo, a pesada porta de saída, com uma luz vermelha piscando.
"""

NOTEBOOK_TEXT = """
Caderno de laboratório - Projeto RECICLA-PET

- Catalisador RP-9 funcionou no PET! Frasco guardado no cofre da parede.
- Código do cofre (3 dígitos): números de reciclagem do PET, do PP e do PS, nessa ordem.
- A chave da sala do reator também fica no cofre. Helena insiste: "nada de chave solta por aí".
- Lote 7 (polietileno) será testado no reator R-2. Dados na lousa.
"""

POSTER_TEXT = """
Pôster "Reciclagem de plásticos". Cada símbolo traz um número dentro de um triângulo:

1 = PET (garrafas)    2 = PEAD (frascos)    3 = PVC (tubos)
4 = PEBD (sacolas)    5 = PP (potes)        6 = PS (isopor)
7 = Outros
"""

WHITEBOARD_TEXT = f"""
Na lousa, com letra apressada:

LOTE 7 - Polietileno (PE)    unidade repetitiva: (-CH2-CH2-)n    n = {answers.PE_REPEAT_UNITS}
Massas atômicas: C = 12    H = 1
"""


def look_at_clock(game):
    state = game.state
    ui.narrate(f"Você ergue os olhos para o relógio analógico. Os ponteiros marcam {state.clock()}.")
    if not state.has(ids.CLOCK_SEEN):
        ui.narrate("Você percebe que demorou para focar a vista. Olhar, pensar, andar: tudo leva tempo, e o ponteiro dos minutos não para.")
        state.add(ids.CLOCK_SEEN)


def examine_bench(game):
    ui.narrate("Entre vidrarias quebradas, você encontra um caderno de laboratório aberto. Você o lê:")
    ui.narrate(NOTEBOOK_TEXT, ui.Color.CYAN)
    game.state.add(ids.NOTEBOOK)
    game.remember("projeto")


def reread_notebook(game):
    ui.narrate(NOTEBOOK_TEXT, ui.Color.CYAN)


def examine_poster(game):
    game.state.add(ids.POSTER)
    ui.narrate(POSTER_TEXT, ui.Color.CYAN)


def examine_whiteboard(game):
    game.state.add(ids.WHITEBOARD)
    ui.narrate(WHITEBOARD_TEXT, ui.Color.CYAN)
    game.remember("equipe")


def open_safe(game):
    state = game.state
    ui.narrate("O cofre tem um teclado numérico de três dígitos.")
    code = ui.prompt("Código (ENTER para desistir)")
    if not code:
        game.free()
        return
    if code != answers.SAFE_CODE:
        attempts = state.bump("safe_wrong")
        ui.danger("Bip de erro. O teclado trava por alguns segundos.")
        game.lose_time(WRONG_CODE_PENALTY)
        if attempts >= 2:
            ui.info("Dica: o caderno de laboratório fala sobre esse código.")
        return
    state.add(ids.SAFE_OPEN)
    state.add(ids.REACTOR_KEY)
    state.add(ids.VIAL)
    ui.success("Clique! A porta do cofre se abre.")
    ui.item("Chave da sala do reator")
    ui.item("Frasco do catalisador RP-9")
    game.remember("catalisador")


def go_to_reactor(game):
    if game.state.has(ids.REACTOR_KEY):
        ui.narrate("A chave gira com um estalo. Você empurra a porta e entra.")
        return ids.REACTOR
    ui.narrate("A porta da sala do reator está trancada. Você sacode a maçaneta em vão.")


def build() -> Scene:
    def after_clock(condition=always):
        return all_of(has(ids.CLOCK_SEEN), condition)

    return Scene(
        id=ids.LAB,
        title="LABORATÓRIO",
        description=DESCRIPTION,
        actions=[
            Action("Olhar o relógio", look_at_clock, cost=2),
            Action("Examinar a bancada", examine_bench, 4, after_clock(lacks(ids.NOTEBOOK))),
            Action("Reler o caderno de laboratório", reread_notebook, 2, after_clock(has(ids.NOTEBOOK))),
            Action("Examinar o pôster de reciclagem", examine_poster, 3, after_clock()),
            Action("Examinar a lousa", examine_whiteboard, 3, after_clock()),
            Action("Tentar abrir o cofre", open_safe, 4, after_clock(lacks(ids.SAFE_OPEN))),
            simple_action(
                "Vasculhar a geladeira de reagentes",
                "Frascos etiquetados, nenhum é o que você procura. Um deles tem a tampa derretida e uma etiqueta amarelada: NÃO ABRIR. Você recua. Tempo perdido.",
                cost=7, visible=after_clock()),
            simple_action(
                "Beber água na pia",
                "A água sai turva, com cheiro estranho. Você joga um pouco no rosto, sem melhorar em nada. Tempo perdido.",
                cost=7, visible=after_clock()),
            travel_action("Ir ao escritório", ids.OFFICE, "Você atravessa a porta aberta.", visible=after_clock()),
            Action("Ir à sala do reator", go_to_reactor, 3, after_clock()),
            travel_action("Ir até a porta de saída", ids.EXIT, "Você caminha até a porta pesada.", visible=after_clock()),
        ],
    )
