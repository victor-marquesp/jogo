"""Respostas dos enigmas, num só lugar.

Se mudar algo aqui, revise as pistas correspondentes nas cenas
(pôster, lousa, caderno, anotação da gaveta e log do computador).
"""

# Cofre: números de reciclagem de PET (1), PP (5) e PS (6), nessa ordem.
SAFE_CODE = "156"

# Painel do reator: massa molar do polietileno (-CH2-CH2-)n.
PE_REPEAT_UNITS = 500
PE_MONOMER_MASS = 28  # C2H4 = 2*12 + 4*1
PE_MOLAR_MASS = PE_REPEAT_UNITS * PE_MONOMER_MASS  # 14000 g/mol

# Computador do escritório: polímero das panelas antiaderentes.
PC_PASSWORDS = {"ptfe", "teflon"}

# Porta de saída (além do crachá).
EXIT_CODE = "7391"
