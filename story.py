"""Textos e parâmetros narrativos. Altere aqui sem mexer no motor."""

# --- Tempo ---
TOTAL_MINUTES = 90      # tempo de vida do personagem (o jogador não é avisado)
START_HOUR = 14         # o relógio da parede começa às 14:00

# --- Sintomas: (fração mínima de tempo restante, estado curto, mensagem ao piorar) ---
SYMPTOMS = [
    (0.66, "tontura e náusea", ""),
    (0.33, "tosse seca e visão embaçada",
     "A tosse piora e a garganta queima. As letras ao redor parecem se borrar."),
    (0.12, "falta de ar e mãos trêmulas",
     "Cada respiração dói. Suas mãos tremem tanto que mal seguram as coisas."),
    (0.00, "à beira do desmaio",
     "Seus joelhos cedem. As bordas da visão escurecem... Você precisa sair DAQUI."),
]

BANNER = r"""
  ____   ___  _     _ __  __ _____ ____   ___  ____
 |  _ \ / _ \| |   | |  \/  | ____|  _ \ / _ \/ ___|
 | |_) | | | | |   | | |\/| |  _| | |_) | | | \___ \
 |  __/| |_| | |___| | |  | | |___|  _ <| |_| |___) |
 |_|    \___/|_____|_|_|  |_|_____|_| \_\\___/|____/
"""

INTRO = """
Escuridão. Depois, um zumbido distante e uma luz fria de lâmpadas fluorescentes.

Você está deitado no chão de um laboratório, com a bochecha colada no piso gelado. A cabeça lateja, a garganta arde e o estômago revira. Há um gosto estranho no ar.

Você se levanta, apoiando-se numa bancada. No jaleco, um crachá: "Pesquisador(a) Sênior - Laboratório de Polímeros".

Quem é você? O que aconteceu aqui? Você não lembra de nada.
"""

# --- Flashbacks (cada um é revelado uma única vez) ---
MEMORIES = {
    "projeto": "Você se lembra: o Projeto RECICLA-PET. Um catalisador capaz de quebrar o PET de volta em seus monômeros, ácido tereftálico e etilenoglicol, para que o plástico fosse reciclado infinitas vezes, sem perder qualidade. Funcionou. Vocês realmente conseguiram.",
    "equipe": "Uma voz: Helena Vaz, sua parceira de bancada, riscando números na lousa. \"Se o catalisador funcionar no polietileno do lote 7, a gente muda o jogo.\" Vocês riram. Era o dia mais feliz da pesquisa.",
    "catalisador": "O frasco do catalisador RP-9 é a única amostra que existe. Você mesmo o trancou no cofre, com um código que só você e Helena conheciam.",
    "acidente": "O teste de escalonamento no reator R-2. A temperatura disparou, o alarme gritou, o disco de ruptura estourou e uma nuvem de vapores tóxicos tomou o laboratório. Você correu... e tudo apagou.",
    "helena": "Helena colando post-its por toda parte. \"Você esquece senhas até do próprio nome!\" Ela sempre escolhia algo de que você gostava para brincar com você.",
    "evacuacao": "Você empurrou Helena porta afora e voltou para buscar o frasco. Foi a última coisa que fez antes de cair.",
}

# --- Curiosidades da estante (ciclam a cada leitura) ---
FACTS = [
    "\"Polímero\" vem do grego: poli (muitos) + meros (partes). Uma única cadeia pode ter milhares de unidades repetidas.",
    "O náilon, criado por Wallace Carothers na DuPont em 1935, foi a primeira fibra totalmente sintética.",
    "Termoplásticos amolecem com calor e podem ser remoldados. Termofixos, como a baquelite, curam de forma irreversível.",
    "Na vulcanização de Charles Goodyear, pontes de enxofre ligam as cadeias da borracha, tornando-a elástica e resistente.",
    "O PTFE (Teflon) foi descoberto por acaso, em 1938, por Roy Plunkett, que investigava gases refrigerantes.",
]

# --- Finais ---
ENDING_DEATH = """
Você tenta dar mais um passo, mas as pernas não respondem. O ar parece feito de vidro.

No chão, o último que vê é o relógio da parede. Os ponteiros continuam girando, indiferentes.

Seu último pensamento: "Eu deveria ter prestado mais atenção no tempo."
"""

ENDING_WIN = """
A porta pesada se abre com um suspiro e o ar fresco da tarde atinge seu rosto como um tapa. Você cai de joelhos no estacionamento, tossindo, mas vivo.

Passos apressados. Helena corre até você, o rosto molhado de lágrimas. "Você demorou!" Ela vê o frasco nas suas mãos e ri e chora ao mesmo tempo.

As lembranças voltam aos poucos. O catalisador sobreviveu. O PET nunca mais precisará virar lixo.
"""
