lista_aluno = ["João", 23455, "TDS"]

dicionario_aluno = { 
    'Nome': "João",
    'RM': 23455,
    'Curso': "TDS",
    'Mensalidade': 1620
    }
print(dicionario_aluno)

print(f'curso do aluno: {dicionario_aluno["Curso"]}')

dicionario_aluno['CPF_aluno'] = "12345678987-30"

print(dicionario_aluno)

#funçao para acessar os items do dicinario separadamente: items

print(dicionario_aluno.items())