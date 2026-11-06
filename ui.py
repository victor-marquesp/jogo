"""Camada de apresentação: tudo que imprime ou lê do terminal passa por aqui.

Defina POLIMEROS_FAST=1 para desativar pausas e limpeza de tela (útil em testes).
"""
import os
import textwrap
import time

WIDTH = 72
FAST = os.environ.get("POLIMEROS_FAST") == "1"

if os.name == "nt":  # habilita sequências ANSI no terminal do Windows
    os.system("")


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"


def paint(text, *styles):
    return "".join(styles) + text + Color.RESET


def clear():
    if not FAST:
        os.system("cls" if os.name == "nt" else "clear")


def rule(char="─"):
    print(paint(char * WIDTH, Color.DIM))


def banner(text):
    print(paint(text, Color.BOLD, Color.CYAN))


def title(text):
    print()
    rule("═")
    print(paint(text.center(WIDTH), Color.BOLD, Color.CYAN))
    rule("═")


def narrate(text, *styles, delay=0.03):
    """Imprime texto com quebra de linha automática, parágrafo a parágrafo."""
    for paragraph in text.strip().split("\n\n"):
        for line in textwrap.wrap(" ".join(paragraph.split()), WIDTH):
            print(paint(line, *styles) if styles else line)
            if not FAST:
                time.sleep(delay)
        print()


def info(text):
    narrate(text, Color.DIM)


def success(text):
    narrate(text, Color.GREEN)


def warning(text):
    narrate(text, Color.YELLOW)


def danger(text):
    narrate(text, Color.RED, Color.BOLD)


def item(name):
    print(paint(f"  + Obtido: {name}", Color.BOLD, Color.YELLOW))
    print()


def memory(text, count, total):
    rule()
    print(paint("◆ FLASH DE MEMÓRIA", Color.BOLD, Color.MAGENTA))
    narrate(text, Color.MAGENTA)
    print(paint(f"  Memórias recuperadas: {count}/{total}", Color.DIM))
    rule()
    print()


def scene_header(text):
    title(text)
    print()


def status(text):
    print(paint(text, Color.DIM))


def menu(options):
    """Mostra opções numeradas e devolve o índice (base 0) escolhido."""
    print()
    for number, label in enumerate(options, start=1):
        tag = paint(f"[{number}]", Color.BOLD, Color.YELLOW)
        print(f"  {tag} {label}")
    while True:
        raw = input(paint("\n> ", Color.BOLD)).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            print()
            return int(raw) - 1
        warning("Opção inválida.")


def prompt(message):
    return input(paint(f"{message}: ", Color.CYAN)).strip()


def pause(message="Pressione ENTER para continuar..."):
    if not FAST:
        input(paint(f"\n{message}", Color.DIM))
