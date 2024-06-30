import socket

host = "127.0.0.1"
porta = 1060

# Configuração do cliente UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Loop principal do cliente
while True:
    print("\n=== MENU ===")
    print("1. Incluir Dados")
    print("2. Listar Dados")
    print("3. Pesquisar Dados")
    print("4. Excluir Dados")
    print("5. Finalizar")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == '1':
        nome = input("Nome: ")
        cpf = input("CPF: ")
        telefone = input("Telefone: ")
        loja = input("loja afiliada: ")
        dados = f"1,{nome},{cpf},{loja},{telefone}"
        cliente.sendto(dados.encode(), (host, porta))
        resposta, _ = cliente.recvfrom(1024)
        print(resposta.decode())
    
    elif opcao == '2':
        cliente.sendto("2".encode(), (host, porta))
        resposta, _ = cliente.recvfrom(4096)
        print(resposta.decode())
    
    elif opcao == '3':
        cpf = input("Digite o CPF para pesquisar: ")
        cliente.sendto(f"3,{cpf}".encode(), (host, porta))
        resposta, _ = cliente.recvfrom(1024)
        print(resposta.decode())
    
    elif opcao == '4':
        cpf = input("Digite o CPF de exclusão: ")
        cliente.sendto(f"4,{cpf}".encode(), (host, porta))
        resposta, _ = cliente.recvfrom(1024)
        print(resposta.decode())
    
    elif opcao == '5':
        cliente.sendto("5".encode(), (host, porta))
        resposta, _ = cliente.recvfrom(1024)
        print(resposta.decode())
        break
    
    else:
        print("Opção inválida. Escolha novamente.")

# Fechar o cliente UDP
cliente.close()
