import socket
import csv

host = "127.0.0.1"
porta = 1060
arquivo_dados = 'dados_usuarios.csv'

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((host, porta))
print(f"Servidor UDP na escuta ... {host}:{porta}")

def salvar_dados(nome, cpf, loja, telefone,):
    with open(arquivo_dados, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nome, cpf, loja, telefone,])
    print(f"Dados salvos: {nome}, {cpf}, {loja}, {telefone}")

def listar_dados():
    with open(arquivo_dados, mode='r', newline='') as file:
        reader = csv.reader(file)
        dados = [linha for linha in reader]
    return dados
     
def pesquisar_dados(cpf):
    encontrado = False
    with open(arquivo_dados, mode='r', newline='') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[1] == cpf:
                encontrado = True
                return linha
    return None

def excluir_dados(cpf):
    linhas = []
    excluido = False
    with open(arquivo_dados, mode='r', newline='') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[1] == cpf:
                excluido = True
            else:
                linhas.append(linha)
    
    if excluido:
        with open(arquivo_dados, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(linhas)
        return True
    else:
        return False

while True:
    dados, endereco = servidor.recvfrom(1024)
    mensagem = dados.decode().split(',')
    
    if mensagem[0] == '1':
        nome, cpf, loja, telefone, = mensagem[1], mensagem[2], mensagem[3], mensagem[4]
        salvar_dados(nome, cpf, loja, telefone,)
        servidor.sendto("Dados salvos com sucesso.".encode(), endereco)
    
    elif mensagem[0] == '2':
        dados = listar_dados()
        resposta = "\n".join([f"Nome: {linha[0]}, CPF: {linha[1]}, Loja: {linha[2]}, Telefone: {linha[3]}" for linha in dados])
        servidor.sendto(resposta.encode(), endereco)
    
    elif mensagem[0] == '3':
        cpf = mensagem[1]
        resultado = pesquisar_dados(cpf)
        if resultado:
            resposta = f"Nome: {resultado[0]}, CPF: {resultado[1]}, Loja: {resultado[2]}, Telefone: {resultado[3]}"
        else:
            resposta = f"Dados com CPF {cpf} não encontrados."
        servidor.sendto(resposta.encode(), endereco)
    
    elif mensagem[0] == '4':
        cpf = mensagem[1]
        resultado = excluir_dados(cpf)
        if resultado:
            resposta = f"Dados com CPF {cpf} excluídos com sucesso."
        else:
            resposta = f"Dados com CPF {cpf} não encontrados."
        servidor.sendto(resposta.encode(), endereco)

    elif mensagem[0] == '5':
        servidor.sendto("Servidor UDP Finalizado".encode(), endereco)
        break

servidor.close()
