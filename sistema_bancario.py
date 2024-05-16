menu = '''

            Banco Digital

    ============ MENU ============
    [1] - Deposito
    [2] - Saque
    [3] - Extrato
    [0] - Sair
    ==============================

    Escolha sua opcao:
    =>'''

saldo = 0
limite = 500
extrato = []
numero_de_saques = 0
Limite_de_saques = 3

while True:
    opcao = int(input(menu))

    if opcao == 1:
        valor = float(input("Digite o valor do depósito: "))
        
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito de R$ {valor}")
        else:
            print("Operação falhou! O valor informado não é válido")

    elif opcao == 2:
        if numero_de_saques < Limite_de_saques:
            valor = float(input("Digite o valor do saque: "))
            if valor > 0:
                if valor <= saldo:
                    saldo -= valor
                    extrato.append(f"Saque de R$ {valor}")
                    numero_de_saques += 1
                else:
                    print("Saldo insuficiente!")
            else:
                print("Operação falhou! O valor informado não é válido")
        else:
            print("Limite de saques atingido!")

    elif opcao == 3:
        print('''

            Banco Digital

    ========== Extrato ==========
    ''')
        print("Não foram realizados saques" if not extrato else extrato )
        print(f"\nSaldo: R$ {saldo:.2f}")
        print('''
    =============================
    ''')

    elif opcao == 0:
        print('''

            Banco Digitals

    ============ SAIR ============
    3
    Obrigado por utilizar nosso sistema!
              
    Saindo ...
    ==============================
''')
        break

    else:
        print("Operação Invalida, por falor selecione novamente a operação desejada.")