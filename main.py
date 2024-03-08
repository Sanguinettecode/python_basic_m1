from datetime import datetime
LIMITE_SAQUE = 500
LIMITE_DIARIO = 3
numero_saques= 0
saldo = 0
extrato = ""
usuarios = []
contas = []

def criar_conta(cpf, usuarios, contas):
    cliente_valido = False
    usuario = {}
    if not cpf:
        raise Exception("Você deve informar um cpf")
    for cliente in usuarios:
        if cliente['cpf'] == cpf:
            cliente_valido = True
            usuario = cliente
            break
    if not cliente_valido:
        raise Exception("Nenhum cliente encontrado.")
    nova_conta = {
        "agencia": "0001",
        "conta": len(contas) + 1
    }
    return nova_conta, usuario
def validar_usuario(novo_usuario, usuarios_cadastrados):
    usuario_cadastrado = False
    try:
        for cliente in usuarios_cadastrados:
            print(cliente)
            if novo_usuario["cpf"] == cliente['cpf']:
                usuario_cadastrado = True
                break
            
        if usuario_cadastrado:
            raise Exception("Usuário já cadastrado!")
    except ValueError as e:
        print(e)



def criar_usuario(usuarios):
    dados = ["nome", "data_nascimento", "cpf", "endereco"]
    dados_endereco = ["logradouro", "numero", "bairro", "cidade", "estado"]
    dados_cliente = {}
    for data in dados:
        if data == "endereco":
            endereco = input("insira o endereço no formato: 'logradouro, numero, bairro, cidade estado'")
            valor = endereco.replace(", ", " - ").replace(",", " - ")
        else:
            valor = input(f"Insira {data}: ")
            if not valor:
                raise Exception(f"Valor {data} é obrigatório")
        dados_cliente[data]=valor
        dados_cliente["contas"] = []
    validar_usuario(dados_cliente, usuarios)
    return dados_cliente

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

def saque(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite:
        raise Exception("Limite diário de saque alcançado. Entre em contato com o banco.")
    if valor > saldo:
        raise Exception("Saldo insuficiente.")
    elif valor > limite_saques:
        raise Exception("O valor é maior que o limite por saque.")
    else:
        saldo -= valor
        numero_saques += 1
        return saldo

def deposito(saldo, valor):
    saldo += valor
    return saldo

def get_extract(extrato, *,saldo):
    return f"extrato atualizado:\n{extrato}\nSaldo atual: {saldo:.2f}"

MENU = """
    Escolha uma operação:
    [d]: Deposito
    [s]: Saque
    [e]: extrato
    [q]: sair
    [c]: Criar Usuário
    [cc]: Criar Conta
"""

while True:
    option = input(MENU)
    if option == "s":
        try:
            valor = input_validator("Valor de saque: ")
            saldo = saque(saldo=saldo, valor=valor, extrato=extrato, limite=LIMITE_DIARIO, numero_saques=numero_saques, limite_saques=LIMITE_SAQUE)
            extrato = extract_formatted("Saque", valor, extrato)
            response = get_extract(extrato, saldo=saldo)
            print(response)
        except Exception as e:
            print(e)

    elif option == "d":
        valor = input_validator("valor do deposito: ")
        saldo = deposito(saldo, valor)
        extrato = extract_formatted("Desposito", valor, extrato)
        response = get_extract(extrato, saldo=saldo)
        print(response)

    elif option == "e":
        response = get_extract(extrato, saldo=saldo)
        print(response)
    elif option == "c":
        try:
            dados_cliente = criar_usuario(usuarios)
            usuarios.append(dados_cliente)
            print("usuário criado com sucesso")
        except Exception as e:
            print(e)
    elif option == "cc":
        try:
            cpf = input("Informe seu CPF: ")
            [nova_conta, usuario] = criar_conta(cpf, usuarios, contas)
            usuario['contas'].append(nova_conta)
            contas.append(nova_conta)
            print("conta criada com sucesso")
        except Exception as e:
            print(e)
    elif option == "l":
        print(usuarios)
    elif option == "q":
        print("Obrigado por usar nosso sistema. Até mais!")
        break
    else:
        print("Operação inválida. Por favor selecione uma opção válida.")
