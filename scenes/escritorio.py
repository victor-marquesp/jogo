"""Cena: escritório (computador, anotações e curiosidades)."""
import answers
import ids
import story
import ui
from engine import Action, Scene, has, lacks, travel_action

WRONG_PASSWORD_PENALTY = 5

DESCRIPTION = """
Um escritório apertado, com papéis por toda parte. Uma mesa com gaveta, um computador ligado pedindo senha e uma estante cheia de livros técnicos.
"""

LOG_TEXT = f"""
LOG DO SISTEMA

13:56  Disco de ruptura do reator R-2 rompido. Vapores tóxicos detectados.
13:58  H. Vaz acionou LOCKDOWN e evacuou o prédio.
13:58  Exaustão desligada por falha de energia. Reinício manual no painel do reator.
Saída: crachá de acesso + código de liberação {answers.EXIT_CODE}.
Aviso: concentração de vapores em níveis críticos sem ventilação.
"""


def search_drawer(game):
    game.state.add(ids.DRAWER)
    ui.narrate("Na gaveta, um post-it colado na parte de dentro, com a letra de Helena:")
    ui.narrate('"Senha do PC: a sigla do polímero das minhas panelas antiaderentes favoritas (4 letras). Não esquece, hein?"', ui.Color.CYAN)
    game.remember("helena")


def use_computer(game):
    state = game.state
    ui.narrate('A tela pede uma senha. Dica do sistema: "veja a anotação da gaveta".')
    password = ui.prompt("Senha (ENTER para desistir)")
    if not password:
        game.free()
        return
    if password.lower() not in answers.PC_PASSWORDS:
        ui.danger("Senha incorreta.")
        game.lose_time(WRONG_PASSWORD_PENALTY)
        return
    state.add(ids.LOGGED_IN)
    state.add(ids.EXIT_CODE_KNOWN)
    ui.success("Acesso liberado. Você abre o log do sistema:")
    ui.narrate(LOG_TEXT, ui.Color.CYAN)
    game.remember("evacuacao")


def reread_log(game):
    ui.narrate(LOG_TEXT, ui.Color.CYAN)


def read_bookshelf(game):
    index = game.state.bump("facts") - 1
    ui.narrate("Você folheia um livro de ciência de polímeros e encontra um trecho:")
    ui.narrate(story.FACTS[index % len(story.FACTS)], ui.Color.CYAN)


def build() -> Scene:
    return Scene(
        id=ids.OFFICE,
        title="ESCRITÓRIO",
        description=DESCRIPTION,
        actions=[
            Action("Revistar a gaveta da mesa", search_drawer, 4, lacks(ids.DRAWER)),
            Action("Usar o computador", use_computer, 4, lacks(ids.LOGGED_IN)),
            Action("Reler o log do sistema", reread_log, 2, has(ids.LOGGED_IN)),
            Action("Folhear os livros da estante", read_bookshelf, 5),
            travel_action("Voltar ao laboratório", ids.LAB, "Você volta ao laboratório."),
        ],
    )
