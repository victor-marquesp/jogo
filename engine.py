"""Motor do jogo: estado, ações, cenas e laço principal.

Não conhece nenhuma cena específica. O conteúdo vive em `scenes/` e `story.py`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Union

import ids
import story
import ui

DEFAULT_COST = 3  # minutos gastos por ação, se não especificado

Condition = Callable[["GameState"], bool]
Handler = Callable[["Game"], Optional[str]]


# ----------------------------------------------------------------- estado
@dataclass
class GameState:
    time_total: int
    scene_id: str = ""
    time_left: int = 0
    flags: set = field(default_factory=set)
    counters: dict = field(default_factory=dict)
    memories: set = field(default_factory=set)

    def __post_init__(self):
        self.time_left = self.time_left or self.time_total

    def has(self, flag: str) -> bool:
        return flag in self.flags

    def add(self, flag: str) -> None:
        self.flags.add(flag)

    def bump(self, key: str) -> int:
        """Incrementa e devolve um contador (ex.: tentativas erradas num enigma)."""
        self.counters[key] = self.counters.get(key, 0) + 1
        return self.counters[key]

    def spend(self, minutes: int) -> None:
        self.time_left = max(0, self.time_left - minutes)

    @property
    def alive(self) -> bool:
        return self.time_left > 0

    @property
    def fraction_left(self) -> float:
        return self.time_left / self.time_total

    def clock(self) -> str:
        elapsed = self.time_total - self.time_left
        total = story.START_HOUR * 60 + elapsed
        return f"{total // 60:02d}:{total % 60:02d}"


# ------------------------------------------------------ condições (helpers)
def always(state: GameState) -> bool:
    return True


def has(flag: str) -> Condition:
    return lambda state: state.has(flag)


def lacks(flag: str) -> Condition:
    return lambda state: not state.has(flag)


def all_of(*conditions: Condition) -> Condition:
    return lambda state: all(condition(state) for condition in conditions)


# ------------------------------------------------------------ ações e cenas
@dataclass(frozen=True)
class Action:
    """Uma opção do menu. O handler devolve o id de uma cena para mudar de lugar."""
    label: str
    handler: Handler
    cost: int = DEFAULT_COST
    visible: Condition = always


@dataclass(frozen=True)
class Scene:
    id: str
    title: str
    description: Union[str, Callable[[GameState], str]]
    actions: list

    def describe(self, state: GameState) -> str:
        return self.description(state) if callable(self.description) else self.description


def simple_action(label, text, cost=DEFAULT_COST, visible=always) -> Action:
    """Ação que só mostra um texto (pistas passivas e armadilhas de tempo)."""
    def handler(game: Game):
        ui.narrate(text)
    return Action(label, handler, cost, visible)


def travel_action(label, destination, text="", cost=2, visible=always) -> Action:
    """Ação que leva a outra cena."""
    def handler(game: Game):
        if text:
            ui.narrate(text)
        return destination
    return Action(label, handler, cost, visible)


# ------------------------------------------------------------------- jogo
class Game:
    def __init__(self, scenes: dict, start_scene: str):
        self.scenes = scenes
        self.state = GameState(time_total=story.TOTAL_MINUTES, scene_id=start_scene)
        self._free = False
        self._symptom_stage = self._current_stage()

    # --- API usada pelos handlers das cenas ---
    def free(self) -> None:
        """A ação em andamento não gasta tempo (ex.: desistir de um enigma)."""
        self._free = True

    def lose_time(self, minutes: int, reason: str = "") -> None:
        self.state.spend(minutes)
        ui.info(f"{reason} (+{minutes} min perdidos)".strip())

    def remember(self, key: str) -> None:
        if key in self.state.memories:
            return
        self.state.memories.add(key)
        ui.memory(story.MEMORIES[key], len(self.state.memories), len(story.MEMORIES))

    # --- laço principal ---
    def run(self) -> None:
        self._intro()
        entering = True
        while True:
            scene = self.scenes[self.state.scene_id]
            if entering:
                self._show_scene(scene)
                entering = False
            self._show_status()

            actions = [a for a in scene.actions if a.visible(self.state)]
            action = actions[ui.menu([a.label for a in actions])]

            self._free = False
            destination = action.handler(self)

            if self.state.has(ids.ESCAPED):
                return self._ending(win=True)
            if not self._free:
                self._pass_time(action.cost)
            if not self.state.alive:
                return self._ending(win=False)

            if destination and destination != self.state.scene_id:
                self.state.scene_id = destination
                entering = True
                ui.pause()

    # --- internos ---
    def _intro(self) -> None:
        ui.clear()
        ui.banner(story.BANNER)
        ui.narrate(story.INTRO)
        ui.pause()

    def _show_scene(self, scene: Scene) -> None:
        ui.clear()
        ui.scene_header(scene.title)
        ui.narrate(scene.describe(self.state))

    def _show_status(self) -> None:
        _, short, _ = story.SYMPTOMS[self._current_stage()]
        ui.rule()
        ui.status(f"Você sente: {short}  |  Memórias: {len(self.state.memories)}/{len(story.MEMORIES)}")

    def _pass_time(self, minutes: int) -> None:
        self.state.spend(minutes)
        ui.info(f"O tempo passa... ({minutes} min)")
        stage = self._current_stage()
        if stage > self._symptom_stage and self.state.alive:
            ui.danger(story.SYMPTOMS[stage][2])
        self._symptom_stage = stage

    def _current_stage(self) -> int:
        fraction = self.state.fraction_left
        for index, (threshold, _, _) in enumerate(story.SYMPTOMS):
            if fraction >= threshold:
                return index
        return len(story.SYMPTOMS) - 1

    def _ending(self, win: bool) -> None:
        ui.clear()
        if win:
            ui.title("FIM - VOCÊ ESCAPOU")
            ui.narrate(story.ENDING_WIN, ui.Color.GREEN)
        else:
            ui.title("FIM - O TEMPO ACABOU")
            ui.narrate(story.ENDING_DEATH, ui.Color.RED)
        ui.status(f"Memórias recuperadas: {len(self.state.memories)}/{len(story.MEMORIES)}")
