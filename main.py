from datetime import datetime
def input_validator(message):
    while True:
        try:
            value = (float(input(message)))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Por favor insira um valor numérico e positivo.")

def extract_formatted(operacao, valor, extrato):
    data_atual = datetime.now().strftime('%d/%m')
    extrato += f"{operacao}: {valor:.2f} ({data_atual})\n"
    return extrato


MENU = """
    Escolha uma operação:
    [d]: Deposito
    [s]: Saque
    [e]: extrato
    [q]: sair
"""
LIMITE_SAQUE = 500
LIMITE_DIARIO = 3
saldo = 0
extrato = ""
numero_saques = 0

while True:
    option = input(MENU)
    if option == "s":
        valor = input_validator("Valor de saque: ")
        if numero_saques >= LIMITE_DIARIO:
            print("Limite diário de saque alcançado. Entre em contato com o banco.")
            continue
        if valor > saldo:
            print("Saldo insuficiente.")
        elif valor > LIMITE_SAQUE:
            print("O valor é maior que o limite por saque.")
        else:
            saldo -= valor
            extrato = extract_formatted("Saque", valor, extrato)
            numero_saques += 1
            print("Aguarde a contagem do dinheiro")

    elif option == "d":
        valor = input_validator("valor do deposito: ")
        saldo += valor
        extrato = extract_formatted("Depósito", valor, extrato)
        print("Deposito realizado com sucesso.")

    elif option == "e":
        print(f"extrato atualizado:\n{extrato}\nSaldo atual: {saldo:.2f}")

    elif option == "q":
        print("Obrigado por usar nosso sistema. Até mais!")
        break
    else:
        print("Operação inválida. Por favor selecione uma opção válida.")
