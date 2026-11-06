"""Ponto de entrada. Execute com:  python main.py"""
import ui
from engine import Game
from scenes import START_SCENE, build_world


def play_once() -> None:
    Game(build_world(), START_SCENE).run()


def main() -> None:
    try:
        while True:
            play_once()
            if ui.prompt("\nJogar novamente? (s/n)").lower() != "s":
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\nJogo encerrado.")


if __name__ == "__main__":
    main()
