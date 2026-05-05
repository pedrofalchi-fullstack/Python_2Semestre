import oracledb as orcl
import requests as req

def main():
    conexao, str_autenticacao, inst_SQL = conectar_BD()
    if (conexao == True):
        print("Conexão estabelecida com sucesso!")
        inserir_aluno()


def conectar_BD():

    try:
        str_conectar = orcl.makedsn("oracle.fiap.com.br", "1521", sid="ORCL")
        str_autenticacao = orcl.connect(user="rm566967", password="fiap26", dsn=str_conectar)

        inst_SQL = str.autentic.cursor()
    except Exception as e:
        print(f"Erro: {erro}")
        conexao = False
    else:
        print("Conexão bem sucedida!")
        conexao = True

    return conexao, str_autenticacao, inst_SQL


def inserir_aluno(str_autenticacao, inst_SQL):
    try:
        rm = int(input("Digite o RM do aluno: "))
        nome = input("Digite o nome do aluno: ")
        curso = input("Digite o curso do aluno: ")
        cep = input("Digite o CEP do aluno: (Somente números) ")
        url = f"https://viacep.com.br/ws/{cep}/json/"
        requisicao = req.get(url)
        if (req.status_code == 200):
            dados_cep = requisicao.json()
            logradouro = dados_cep["logradouro"]
            print(f"Logradouro: {logradouro}")
            numero = int(input("Digite o número do Logradouro: "))
            bairro = dados_cep['bairro']
            cidade = dados_cep['cidade']
            cep_api = dados_cep['cep']
        else:
            print("Falha na conexão do CEP")
    except:
        print("Teste")
    else:
        print("Teste")


if __name__ == "__main__":
    main()