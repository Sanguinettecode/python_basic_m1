from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Validators:
    @staticmethod
    def input_validator(message):
        valor = (float(input(message)))
        if valor <= 0:
            return False
        return True


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_trasacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento, endereco: str):
        super().__init__(endereco)
        self._cpf =  cpf
        self._nome =  nome
        self._data_nascimento =  data_nascimento
        


class Conta(Validators):
    n_contas = 0

    def __init__(self,numero, cliente):
        self._saldo =  0
        self._numero =  numero
        self._agencia = '0001'
        self._cliente =  cliente
        self._historico =  Historico()
        self.input_validator = super().input_validator

    @property
    def saldo(self) -> float:
        return round(self.saldo, 2) or 0.00
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        saldo =  self._saldo
        if valor > saldo:
            print("Saldo insuficiente.")
        if not self.input_validator(valor):
            print("valor inválido.")
        else:
            self._saldo -= valor
            print('saque realizado com sucesso.')
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if not self.input_validator(valor):
            print("valor inválido.")
            return False
        self._saldo += valor
        return True


class ContaCorrente(Conta):
    _limite: 500
    _limite_saques: 3

    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)

    def saque(self, valor):
        numero_saques = len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_transacoes = numero_saques > self._limite_saques

        if excedeu_limite:
            print("Valor de saque excede o limite.")
        elif excedeu_transacoes:
            print("Número máximo de transaçoes excedido.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            agência: {self._agencia}
            C/C: {self._numero}
            Titular: {self._cliente._nome}
        """
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_trasacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%y %H:%M:%s")
        })

class Saque(Transacao):
    def __init__(self, valor):
        self._valor =  valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao =  conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor =  valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao =  conta.depositar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
