"""Registro das cenas. Para adicionar uma cena: crie o módulo e inclua-o na lista."""
from engine import Scene

from . import escritorio, laboratorio, reator, saida

START_SCENE = "laboratorio"


def build_world() -> dict:
    modules = [laboratorio, escritorio, reator, saida]
    scenes = [module.build() for module in modules]
    return {scene.id: scene for scene in scenes}
