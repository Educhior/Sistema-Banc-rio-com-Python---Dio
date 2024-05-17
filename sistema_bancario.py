
import textwrap


def deposito (saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito de R$ {valor}")
        print("\n === Deposito realizado com sucesso! ===")

    else:
        print("\n @@@ Operação falhou! O valor informado não é válido. @@@")
        
    return saldo, extrato

def saque (*, saldo, valor, extrato, limite, numero_de_saques, Limite_de_saques):
    if numero_de_saques < Limite_de_saques:
        valor = float(input("Digite o valor do saque: "))
        if valor > 0:
            if valor <= saldo:
                saldo -= valor
                extrato.append(f"Saque de R$ {valor}")
                numero_de_saques += 1
                print("\n === Saque realizado com sucesso! ===")
            else:
                print("Saldo insuficiente!")
        else:
            print("\n @@@ Operação falhou! O valor informado não é válido. @@@")
    else:
        print("\n @@@ Limite de saques atingido!@@@")

    return saldo, extrato

def criar_usuario(usuarios):
     cpf = input("Digite seu CPF: ")
     usuario = filtrar_usuario(cpf, usuarios)

     if usuario:
          print("\n @@@ Já existe um usuário com esse CPF! @@@")
          return
     
     nome = input("Digite seu nome completo: ")
     data_de_nascimento = input("Digite sua data de nascimento (dd-mm-aaaa): ")
     endereço = input("Digite seu endereço (logradouro, num - bairro - cidade/estado): ")

     usuarios.append({"nome":nome, "data_de_nascimento":data_de_nascimento, "cpf":cpf, "endereco":endereço })

     print("=== Usuário cadastrado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
     usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf] 
     return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia":agencia, "numero_conta":numero_conta, "usuario":usuario}
    
    print("\n@@@ Usuario não existe! Conta não criada. @@@")

def lista_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
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
     

def main():
    
     usuarios = []
     contas = []
     AGENCIA = "0001"
     saldo = 0
     limite = 500
     extrato = ""
     numero_de_saques = 0
     Limite_de_saques = 3

     while True:
          opcao = menu()

          if opcao == 1:
              numero_conta = len(contas) + 1
              conta = criar_conta(AGENCIA, numero_conta, usuarios)

              if conta:
                  contas.append(conta)
                  print("\n === Conta criada com sucesso! ===")
          if opcao == 2:
              criar_usuario(usuarios)
          if opcao == 3:
              cpf = input("Digite seu CPF: ")
              usuario = filtrar_usuario(cpf, usuarios)
              if usuario:
                  print("\n === Usuario logado com sucesso! ===")
                  while True:
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

                      if opcao == 1:
                          valor = float(input("Digite o valor do deposito: "))
                          saldo, extrato = deposito(saldo, valor, extrato)
                      if opcao == 2:
                          valor = float(input("Digite o valor do saque: "))
                          saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_de_saques=numero_de_saques, Limite_de_saques=Limite_de_saques)
                      if opcao == 3:
                          exibir_extrato(saldo, extrato=extrato)
                      if opcao == 4:
                          lista_contas(contas)
                      if opcao == 0:
                          print("\n === Sistema encerrado! ===")
                          print('''\n
                          =======================================''')
                          break
                      else:
                          print("\n@@@ Operação invalida! Por favor selecione novamente a operação desejada. @@@")
                          print('''\n
                          =======================================''')
              else:
                print("\n @@@ Usuario não existe! @@@")
          if opcao == 0:
                print("\n === Sistema encerrado! ===")
                print('''\n
                =======================================''')
                break
          else:
              print("\n@@@ Operação invalida! Por favor selecione novamente a operação desejada. @@@")
              print('''\n
              =======================================''')
              
              
                          
               
main()