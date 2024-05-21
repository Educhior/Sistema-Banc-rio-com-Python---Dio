
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def deposito (saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def saque (*, saldo, valor, extrato, limite, numero_de_saques, Limite_de_saques):
    if numero_de_saques < Limite_de_saques:
        if valor > 0:
            if valor <= saldo:
                saldo -= valor
                extrato += f"Saque:\t\tR$ {valor:.2f}\n"
                numero_de_saques += 1
                print("\n === Saque realizado com sucesso! ===")
            else:
                print("\nSaldo insuficiente!")
        else:
            print("\n @@@ Operação falhou! O valor informado não é válido. @@@")
    else:
        print("\n @@@ Limite de saques atingido!@@@")

    return saldo, extrato

def criar_usuario(usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe um usuário com esse CPF! @@@")
        return

    nome = input("Digite seu nome completo: ")
    data_de_nascimento = input("Digite sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite seu endereço (logradouro, num - bairro - cidade/estado): ")

    usuario = PessoaFisica(nome, data_de_nascimento, cpf, endereco)
    usuarios.append(usuario)

    print("\n=== Usuário cadastrado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = ContaCorrente(numero_conta, usuario)
        usuario.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return conta
    
    print("\n@@@ Usuário não existe! Conta não criada. @@@")
    return None

def lista_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f}\tData: {transacao['data']}")
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def menu():
    opcao = int(input('''
                Banco Digital

    ============ Bem-Vindo(a) ============
           
           [1] - Criar Conta
           [2] - Criar Usuario
           [3] - Fazer Login
           [0] - Sair do Sistema
    ======================================

    Escolha sua opcao:
    => '''))
    print('''\n
    =======================================''')
    return opcao

def menu_conta():
    opcao = int(input('''
                Banco Digital

    ============ Bem-Vindo(a) ============
                                       
           [1] - Depositar
           [2] - Sacar
           [3] - Extrato
           [4] - Lista Contas
           [0] - Sair
                                        
    ======================================

    Escolha sua opcao:
    => '''))
    return opcao

def main():
    usuarios = []
    contas = []
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == 1:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == 2:
            criar_usuario(usuarios)

        elif opcao == 3:
            cpf = input("Digite seu CPF: ")
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                print("\n=== Usuário logado com sucesso! ===")
                while True:
                    opcao = menu_conta()

                    if opcao == 1:
                        valor = float(input("Digite o valor do depósito: "))
                        transacao = Deposito(valor)
                        usuario.realizar_transacao(usuario.contas[0], transacao)  # Considerando uma conta para simplificar

                    elif opcao == 2:
                        valor = float(input("Digite o valor do saque: "))
                        transacao = Saque(valor)
                        usuario.realizar_transacao(usuario.contas[0], transacao)  # Considerando uma conta para simplificar

                    elif opcao == 3:
                        exibir_extrato(usuario.contas[0])  # Considerando uma conta para simplificar

                    elif opcao == 4:
                        lista_contas(contas)

                    elif opcao == 0:
                        break

            else:
                print("\n@@@ Usuário não existe! @@@")

        elif opcao == 0:
            print("\n=== Sistema encerrado! ===")
            break

if __name__ == "__main__":
    main()