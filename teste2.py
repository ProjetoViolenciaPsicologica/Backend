import requests

# SCRIPT DE TESTE PARA CRIAR FORMULÁRIOS NO SISTEMA

url = 'https://projpsi.pythonanywhere.com/api/psicoapp/formulario/novo'

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NjYxNjI2LCJpYXQiOjE3MDg2NjEzMjYsImp0aSI6IjY4MWZlZjdjNzM1YTQ4YzBhZjY3YjUxN2MwMGEwMmU2IiwidXNlcl9pZCI6MjYsIm5hbWUiOiIiLCJ0aXBvIjoiRWR1Y2FcdTAwZTdcdTAwZTNvIiwiYXJlYSI6IkFnZW50ZSBkZSBTYVx1MDBmYWRlIiwiaXNfc3VwZXJ1c2VyIjp0cnVlfQ.693rRDjV-Mb7_zoLVC8UdbRWrOkdOxG3KryKauTT8cM'

# Corpo da requisição
data = {
    "campo_questoes": "1,2,3,4",
    "idade": 12,
    "escolha_sexo": "Feminino",
    "grau_de_instrucao": "Ensino Superior",
    "localAplicacao": {
        "definicicaoLocal": "Hospital"
    },
    "area": {
        "definicaoArea": "Saúde"
    },
}

# Cabeçalhos da requisição incluindo o token JWT
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 201:
    print("Formulário criado com sucesso!")
else:
    print("Erro ao criar o formulário. Código de status:", response.status_code)
    print("Resposta:", response.text)