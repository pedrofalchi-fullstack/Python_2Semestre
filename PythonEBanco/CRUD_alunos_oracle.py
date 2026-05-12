import oracledb as orcl
import requests
import pandas as pd

def main():
    conexao, str_autentic, inst_SQL = conectar_BD()
    opc_principal = 0
    if (conexao == True):
        while (opc_principal!=4):
            print("1-CRUD de alunos")
            print("2-CRUD de cursos")
            print("3-Relatorio dos alunos por curso")
            print("4-Sair")
            opc_principal = int(input("Digite a opcao desejada (1 a 4): "))
            if (opc_principal >= 1 and opc_principal <= 4):
                if (opc_principal == 1):
                    # CRUD dos alunos
                    opc_alunos = 0
                    while (opc_alunos!=7):
                        print("1-Insercao de um aluno")
                        print("2-Alteracao de um aluno")
                        print("3-Exclusao de um aluno")
                        print("4-Exibicao de todos os alunos")
                        print("5-Relatorio dos alunos que cursam TDS e que moram na cidade de São Paulo")
                        print("6-Gerar um arquivo .txt do relatorio")
                        print("7-Voltar para o menu principal")

                        opc_alunos = int(input("Digite a opcao desejada (1 a 7): "))
                        if (opc_alunos >= 1 and opc_alunos <= 7):
                            if (opc_alunos == 1): # insercao
                                inserir_aluno(str_autentic, inst_SQL)
                                print("\n")
                            elif (opc_alunos == 2):
                                alterar_aluno(str_autentic, inst_SQL)
                                print("\n")
                            elif (opc_alunos == 3):
                                excluir_aluno(str_autentic, inst_SQL)
                                print("\n")
                            elif (opc_alunos == 4):
                                exibir_alunos(inst_SQL)
                                print("\n")
                            elif (opc_alunos == 5):
                                gerar_relatorio_alunos(inst_SQL)
                                print("\n")
                                print("\n")
                            elif (opc_alunos == 6):
                                gerar_arquivo_txt_alunos(inst_SQL)
                                print("\n")
                elif (opc_principal == 2):
                    # CRUD dos cursos
                    opc_cursos = 0
                    while (opc_cursos != 7):
                        print("1-Insercao de um curso")
                        print("2-Alteracao de um curso")
                        print("3-Exclusao de um curso")
                        print("4-Exibicao de todos os curso")
                        print("5-Relatorio dos cursos cuja carga horaria seja maior do que 100 horas")
                        print("6-Gerar um arquivo .txt do relatorio")
                        print("7-Voltar para o menu principal")

                        opc_cursos = int(input("Digite a opcao desejada (1 a 7): "))
                        if (opc_cursos >= 1 and opc_cursos <= 7):
                            if (opc_cursos == 1):  # insercao
                                inserir_curso(str_autentic, inst_SQL)
                                print("\n")
                            elif (opc_cursos == 2):
                                alterar_curso(str_autentic, inst_SQL)
                                print("\n")
                            elif (opc_cursos == 3):
                                excluir_curso(str_autentic, inst_SQL)
                                print("\n")
                            elif (opc_cursos == 4):
                                exibir_cursos(inst_SQL)
                                print("\n")
                            elif (opc_cursos == 5):
                                gerar_relatorio_cursos(inst_SQL)
                                print("\n")
                            elif (opc_cursos == 6):
                                gerar_arquivo_txt_cursos(inst_SQL)
                                print("\n")
                elif (opc_principal == 3):
                    gerar_relatorio_alunos_curso(inst_SQL)
                    print("\n")

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

def inserir_curso(str_autentic, inst_SQL):
    try:
        nome = input("Digite o nome do curso: ")
        carga_horaria = int(input("Digite a carga horaria do curso: "))
        qtde_alunos = int(input("Digite a quantidade alunos do curso"))

        str_insert = f"""INSERT INTO cursos_1tdsps_2026 (CURSO_NOME,CURSO_CARGAHORARIA,CURSO_QTDEALUNOS) VALUES ('{nome}',{carga_horaria},{qtde_alunos})"""

        inst_SQL.execute(str_insert)
        str_autentic.commit()
    except ValueError:
        print("Os dados da carga horaria e quantidade de alunos devem ser numericos")
    except Exception as erro:
        print(f"ERRO: {erro}")
    else:
        print("Dados inseridos com sucesso! ")


def inserir_aluno(str_autentic, inst_SQL):
    try:
        ra = int(input("Digite o RM do aluno: "))
        nome = input("Digite o nome do aluno: ")
        exibir_cursos(inst_SQL)
        id_curso = int(input("Digite o id co curso que deseja relacionar ao aluno: "))
        lista_dados = []

        str_consulta_alteracao = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_ID={id_curso} """
        inst_SQL.execute(str_consulta_alteracao)

        # recuperar as linhas resultantes da consulta SQL (Select)
        dados = inst_SQL.fetchall()

        for dado in dados:
            lista_dados.append(dado)

        if (len(lista_dados) > 0):
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

            str_insert = f"""INSERT INTO alunos_1tdsps_2026 (ALUNO_RA,ALUNO_NOME,ALUNO_CEP,ALUNO_LOGRADOURO,ALUNO_NUMERO,ALUNO_BAIRRO,ALUNO_CIDADE,ALUNO_CURSOID) VALUES ({ra},'{nome}','{cep}','{logradouro}',{numero},'{bairro}','{cidade}',{id_curso})"""

            inst_SQL.execute(str_insert)
            str_autentic.commit()
        else:
            print("Esse id do curso nao existe")
    except ValueError:
        print("Os dados do rm e do numero do logradouro devem ser numericos")
    except Exception as erro:
        print(f"ERRO: {erro}")
    else:
        print("Dados inseridos com sucesso! ")

def exibir_cursos(inst_SQL):
    lista_dados = []

    inst_SQL.execute("SELECT * FROM cursos_1tdsps_2026")

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    # Criar um dataframe baseado na lista com os dados do select
    df_cursos = pd.DataFrame.from_records(lista_dados,columns=['ID','NOME','CARGA HORARIA','QTDE ALUNOS'],index='ID')

    if (df_cursos.empty):
        print("Nao existem alunos na tabela")
    else:
        print(df_cursos)

def exibir_alunos(inst_SQL):
    lista_dados = []

    inst_SQL.execute("SELECT A.ALUNO_ID,A.ALUNO_RA,A.ALUNO_NOME,A.ALUNO_CIDADE,C.CURSO_NOME FROM alunos_1tdsps_2026 A, cursos_1tdsps_2026 C WHERE A.ALUNO_CURSOID=C.CURSO_ID")

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    # Criar um dataframe baseado na lista com os dados do select
    df_alunos = pd.DataFrame.from_records(lista_dados,columns=['ID','RM','NOME','CIDADE','CURSO'],index='ID')

    if (df_alunos.empty):
        print("Nao existem alunos na tabela")
    else:
        print(df_alunos)

def alterar_curso(str_autentic, inst_SQL):
    exibir_cursos(inst_SQL)
    lista_dados = []

    id_alterar = int(input("Digite o ID do curso que deseja alterar os dados: "))

    str_consulta_alteracao = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_ID={id_alterar} """
    inst_SQL.execute(str_consulta_alteracao)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if (len(lista_dados) > 0):
        try:
            novo_nome = input("Digite o novo nome do curso: ")
            nova_carga_horaria = int(input("Digite a nova carga horaria do curso: "))
            nova_qtde_alunos = int(input("Digite a nova quantidade alunos do curso"))

            str_update = f"""UPDATE cursos_1tdsps_2026 SET CURSO_NOME='{novo_nome}', CURSO_CARGAHORARIA={nova_carga_horaria},CURSO_QTDEALUNOS={nova_qtde_alunos} WHERE CURSO_ID={id_alterar}"""

            inst_SQL.execute(str_update)
            str_autentic.commit()
        except ValueError:
            print("Os dados da carga horaria e da quantidade devem ser numericos")
        except Exception as erro:
            print(f"ERRO: {erro}")
        else:
            print("Dados alterados com sucesso! ")
    else:
        print("O ID desse curso nao existe")

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
            exibir_cursos(inst_SQL)
            id_curso = int(input("Digite o id co curso que deseja relacionar ao aluno: "))
            lista_dados = []

            str_consulta_alteracao = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_ID={id_curso} """
            inst_SQL.execute(str_consulta_alteracao)

            # recuperar as linhas resultantes da consulta SQL (Select)
            dados = inst_SQL.fetchall()

            for dado in dados:
                lista_dados.append(dado)

            if (len(lista_dados) > 0):
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

                str_update = f"""UPDATE alunos_1tdsps_2026 SET ALUNO_RA={novo_ra}, ALUNO_NOME='{novo_nome}',ALUNO_CEP='{cep}',ALUNO_LOGRADOURO='{logradouro}',ALUNO_NUMERO={numero},ALUNO_BAIRRO='{bairro}',ALUNO_CIDADE='{cidade}',ALUNO_CURSOID={id_curso} WHERE ALUNO_ID={id_alterar}"""

                inst_SQL.execute(str_update)
                str_autentic.commit()
            else:
                print("Esse id de curso nao existe")
        except ValueError:
            print("Os dados do rm e do numero do logradouro devem ser numericos")
        except Exception as erro:
            print(f"ERRO: {erro}")
        else:
            print("Dados alterados com sucesso! ")
    else:
        print("O ID desse aluno nao existe")

def excluir_curso(str_autentic, inst_SQL):
    exibir_cursos(inst_SQL)
    lista_dados = []

    id_excluir = int(input("Digite o ID do curso que deseja excluir os dados: "))

    str_consulta_exclusao = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_ID={id_excluir} """
    inst_SQL.execute(str_consulta_exclusao)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if (len(lista_dados) > 0):
        try:
            str_delete = f"""DELETE FROM cursos_1tdsps_2026 WHERE CURSO_ID={id_excluir}"""
            inst_SQL.execute(str_delete)
            str_autentic.commit()
        except Exception as erro:
            print(f"ERRO: {erro}")
        else:
            print("Dados excluidos com sucesso! ")
    else:
        print("O ID desse curso nao existe")

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

def gerar_relatorio_cursos(inst_SQL):
    lista_dados = []

    str_relatorio = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_CARGAHORARIA > 100"""

    inst_SQL.execute(str_relatorio)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    # Criar um dataframe baseado na lista com os dados do select
    df_cursos = pd.DataFrame.from_records(lista_dados, columns=['ID', 'NOME', 'CARGA HORARIA', 'QTDE ALUNOS'], index='ID')

    if (df_cursos.empty):
        print("Nao existem cursos nessa condicao")
    else:
        print(df_cursos)

def gerar_relatorio_alunos(inst_SQL):
    lista_dados = []

    str_relatorio = f"""SELECT A.ALUNO_ID,A.ALUNO_RA,A.ALUNO_NOME,A.ALUNO_CIDADE,C.CURSO_NOME FROM alunos_1tdsps_2026 A, cursos_1tdsps_2026 C WHERE A.ALUNO_CURSOID=C.CURSO_ID AND C.CURSO_NOME='TDS' AND A.ALUNO_CIDADE='São Paulo'"""

    inst_SQL.execute(str_relatorio)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    # Criar um dataframe baseado na lista com os dados do select
    df_alunos = pd.DataFrame.from_records(lista_dados, columns=['ID', 'RM', 'NOME', 'CIDADE','CURSO'], index='ID')

    if (df_alunos.empty):
        print("Nao existem alunos nessa condicao")
    else:
        print(df_alunos)

def gerar_arquivo_txt_cursos(inst_SQL):
    lista_dados = []

    str_relatorio = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_CARGAHORARIA > 100"""

    inst_SQL.execute(str_relatorio)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    if (len(lista_dados) > 0):
        nome_arq = input("Digite o nome do arquivo texto (com extensao .txt): ")
        for curso in lista_dados:
            str_txt = str(curso[0]) + "\t" + curso[1] + "\t" + str(curso[2]) + "\t" + str(curso[3]) + "\n"
            with open(nome_arq,"a",encoding="utf-8") as arqCurso:
                arqCurso.write(str_txt)
                arqCurso.close()
        print("Arquivo txt gerado com sucesso!")
    else:
        print("Nao existem cursos nessa condicao")

def gerar_arquivo_txt_alunos(inst_SQL):
    lista_dados = []

    str_relatorio = f"""SELECT A.ALUNO_ID,A.ALUNO_RA,A.ALUNO_NOME,A.ALUNO_CIDADE,C.CURSO_NOME FROM alunos_1tdsps_2026 A, cursos_1tdsps_2026 C WHERE A.ALUNO_CURSOID=C.CURSO_ID AND C.CURSO_NOME='TDS' AND A.ALUNO_CIDADE='São Paulo'"""

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

def gerar_relatorio_alunos_curso(inst_SQL):
    exibir_cursos(inst_SQL)
    lista_dados = []

    id_curso = int(input("Digite o ID do curso que deseja exibir os alunos: "))

    str_consulta = f"""SELECT * FROM cursos_1tdsps_2026 WHERE CURSO_ID={id_curso} """
    inst_SQL.execute(str_consulta)

    # recuperar as linhas resultantes da consulta SQL (Select)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    if (len(lista_dados) > 0):
        lista_dados_alunos = []

        str_consulta = f"""SELECT A.ALUNO_ID,A.ALUNO_RA,A.ALUNO_NOME,A.ALUNO_CIDADE,C.CURSO_NOME FROM alunos_1tdsps_2026 A, cursos_1tdsps_2026 C WHERE A.ALUNO_CURSOID=C.CURSO_ID AND C.CURSO_ID={id_curso}"""

        inst_SQL.execute(str_consulta)

        # recuperar as linhas resultantes da consulta SQL (Select)
        dados = inst_SQL.fetchall()

        for dado in dados:
            lista_dados_alunos.append(dado)

        lista_dados_alunos = sorted(lista_dados_alunos)

        # Criar um dataframe baseado na lista com os dados do select
        df_alunos = pd.DataFrame.from_records(lista_dados_alunos, columns=['ID', 'RM', 'NOME', 'CIDADE', 'CURSO'], index='ID')

        if (df_alunos.empty):
            print("Nao existem alunos para esse curso")
        else:
            print(df_alunos)

if (__name__ == "__main__" ):
    main()

