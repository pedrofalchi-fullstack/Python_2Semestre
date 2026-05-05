import oracledb as orcl
import requests
import pandas as pd

def main():
    conexao, str_autentic, inst_SQL = conectar_BD()
    if (conexao == True):
        resp = 1
        while (resp == 1):
            print("1-Insercao de um aluno")
            print("2-Alteracao de um aluno")
            print("3-Exclusao de um aluno")
            print("4-Exibicao de todos os alunos")
            print("5-Relatorio dos alunos que cursam TDS e que moram na cidade de São Paulo")
            print("6-Gerar um arquivo .txt do relatorio")

            opcao = int(input("Digite a opcao desejada (1 a 6): "))
            if (opcao >= 1 and opcao <= 6):
                if (opcao == 1): # insercao
                    inserir_aluno(str_autentic, inst_SQL)
                    print("\n")
                elif (opcao == 2):
                    alterar_aluno(str_autentic, inst_SQL)
                    print("\n")
                elif (opcao == 3):
                    excluir_aluno(str_autentic, inst_SQL)
                    print("\n")
                elif (opcao == 4):
                    exibir_alunos(inst_SQL)
                    print("\n")
                elif (opcao == 5):
                    gerar_relatorio(inst_SQL)
                    print("\n")
                elif (opcao == 6):
                    gerar_arquivo_txt(inst_SQL)
                else:
                    print("Opcao invalida!")
            resp = int(input("Deseja continuar (1-SIM/0-NAO)? "))


def conectar_BD():
    try:
        str_conectar = orcl.makedsn("oracle.fiap.com.br",1521,"ORCL")
        str_autentic = orcl.connect(user="PF1633",password="fiap23",dsn=str_conectar)

        inst_SQL = str_autentic.cursor()
    except Exception as erro:
        print(f"ERRO: {erro}")
        conexao = False
    else:
        conexao = True

    return conexao, str_autentic, inst_SQL

def inserir_aluno(str_autentic, inst_SQL):
    try:
        ra = int(input("Digite o RM do aluno: "))
        nome = input("Digite o nome do aluno: ")
        curso = input("Digite o curso do aluno: ")
        cep = input("Digite o cep da sua residencia (somente numeros): ")
        url = f"https://viacep.com.br/ws/{cep}/json/"
        requisicao = requests.get(url)
        if (requisicao.status_code == 200):
            dados_cep = requisicao.json()
            logradouro = dados_cep['logradouro']
            print(f"Logradouro: {logradouro}")
            numero = int(input("Digite o numero do logradouro: "))
            bairro = dados_cep['bairro']
            cidade = dados_cep['localidade']
        else:
            print("Falha na consulta do CEP")

        str_insert = f"""INSERT INTO alunos_1tdsps_2026 (ALUNO_RA,ALUNO_NOME,ALUNO_CURSO,ALUNO_CEP,ALUNO_LOGRADOURO,ALUNO_NUMERO,ALUNO_BAIRRO,ALUNO_CIDADE) VALUES ({ra},'{nome}','{curso}','{cep}','{logradouro}',{numero},'{bairro}','{cidade}')"""

        inst_SQL.execute(str_insert)
        str_autentic.commit()
    except ValueError:
        print("Os dados do rm e do numero do logradouro devem ser numericos")
    except Exception as erro:
        print(f"ERRO: {erro}")
    else:
        print("Dados inseridos com sucesso! ")

def exibir_alunos(inst_SQL):
    lista_dados = []

    inst_SQL.execute("SELECT ALUNO_ID,ALUNO_RA,ALUNO_NOME,ALUNO_CURSO,ALUNO_CIDADE FROM alunos_1tdsps_2026")

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    # Criar um dataframe baseado na lista com os dados do select
    df_alunos = pd.DataFrame.from_records(lista_dados,columns=['ID','RM','NOME','CURSO','CIDADE'],index='ID')

    if (df_alunos.empty):
        print("Nao existem alunos na tabela")
    else:
        print(df_alunos)

def alterar_aluno(str_autentic, inst_SQL):
    exibir_alunos(inst_SQL)
    lista_dados = []

    id_alterar = int(input("Digite o ID do aluno que deseja alterar os dados: "))

    str_consulta_alteracao = f"""SELECT * FROM alunos_1tdsps_2026 WHERE ALUNO_ID={id_alterar} """
    inst_SQL.execute(str_consulta_alteracao)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if (len(lista_dados) > 0):
        try:
            novo_ra = int(input("Digite o novo RM do aluno: "))
            novo_nome = input("Digite o novo nome do aluno: ")
            novo_curso = input("Digite o novo curso do aluno: ")
            cep = input("Digite o novo cep da sua residencia (somente numeros): ")
            url = f"https://viacep.com.br/ws/{cep}/json/"
            requisicao = requests.get(url)
            if (requisicao.status_code == 200):
                dados_cep = requisicao.json()
                logradouro = dados_cep['logradouro']
                print(f"Logradouro: {logradouro}")
                numero = int(input("Digite o numero do logradouro: "))
                bairro = dados_cep['bairro']
                cidade = dados_cep['localidade']
            else:
                print("Falha na consulta do CEP")

            str_update = f"""UPDATE alunos_1tdsps_2026 SET ALUNO_RA={novo_ra}, ALUNO_NOME='{novo_nome}',ALUNO_CURSO='{novo_curso}',ALUNO_CEP='{cep}',ALUNO_LOGRADOURO='{logradouro}',ALUNO_NUMERO={numero},ALUNO_BAIRRO='{bairro}',ALUNO_CIDADE='{cidade}' WHERE ALUNO_ID={id_alterar}"""

            inst_SQL.execute(str_update)
            str_autentic.commit()
        except ValueError:
            print("Os dados do rm e do numero do logradouro devem ser numericos")
        except Exception as erro:
            print(f"ERRO: {erro}")
        else:
            print("Dados alterados com sucesso! ")
    else:
        print("O ID desse aluno nao existe")

def excluir_aluno(str_autentic, inst_SQL):
    exibir_alunos(inst_SQL)
    lista_dados = []

    id_excluir = int(input("Digite o ID do aluno que deseja excluir os dados: "))

    str_consulta_exclusao = f"""SELECT * FROM alunos_1tdsps_2026 WHERE ALUNO_ID={id_excluir} """
    inst_SQL.execute(str_consulta_exclusao)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if (len(lista_dados) > 0):
        try:
            str_delete = f"""DELETE FROM alunos_1tdsps_2026 WHERE ALUNO_ID={id_excluir}"""
            inst_SQL.execute(str_delete)
            str_autentic.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")
        else:
            print("Dados excluidos com sucesso! ")
    else:
        print("O ID desse aluno nao existe")

def gerar_relatorio(inst_SQL):
    lista_dados = []

    str_relatorio = f"""SELECT ALUNO_ID,ALUNO_RA,ALUNO_NOME,ALUNO_CURSO,ALUNO_CIDADE FROM alunos_1tdsps_2026 WHERE ALUNO_CURSO='TDS' AND ALUNO_CIDADE='São Paulo'"""

    inst_SQL.execute(str_relatorio)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    # Criar um dataframe baseado na lista com os dados do select
    df_alunos = pd.DataFrame.from_records(lista_dados, columns=['ID', 'RM', 'NOME', 'CURSO', 'CIDADE'], index='ID')

    if (df_alunos.empty):
        print("Nao existem alunos nessa condicao")
    else:
        print(df_alunos)

def gerar_arquivo_txt(inst_SQL):
    lista_dados = []

    str_relatorio = f"""SELECT ALUNO_ID,ALUNO_RA,ALUNO_NOME,ALUNO_CURSO,ALUNO_CIDADE FROM alunos_1tdsps_2026 WHERE ALUNO_CURSO='TDS' AND ALUNO_CIDADE='São Paulo'"""

    inst_SQL.execute(str_relatorio)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    if (len(lista_dados) > 0):
        nome_arq = input("Digite o nome do arquivo texto (com extensao .txt): ")
        for aluno in lista_dados:
            str_txt = str(aluno[0]) + "\t" + str(aluno[1]) + "\t" + aluno[2] + "\t" + aluno[3] + "\t" + aluno[4] + "\n"
            with open(nome_arq,"a",encoding="utf-8") as arqAluno:
                arqAluno.write(str_txt)
                arqAluno.close()
        print("Arquivo txt gerado com sucesso!")
    else:
        print("Nao existem alunos nessa condicao")

if (__name__ == "__main__" ):
    main()

