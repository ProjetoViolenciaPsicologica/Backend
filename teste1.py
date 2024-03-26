import requests

# SCRIPT DE TESTE PARA REGISTRAR USUÁRIOS NO SISTEMA

# URL do seu endpoint de registro de usuários
url = 'https://projpsi.pythonanywhere.com/api/psicoapp/user/register'

# Dados do usuário a serem enviados no formato JSON
areas = ['Saúde', 'Educação', 'Segurança']
user_data_list = []

for i in range(2, 16):
    if i <= 5:
        area = areas[0]
    elif i <= 10:
        area = areas[1]
    else:
        area = areas[2]
    data = {
        'email': f'exemplo{i}@email.com',
        'name': f'Usuário{i}',
        'password': f'senha123{i}',
        'tipo': {
            'definicaoTipo': f'Agente de {area}',  # Este é o campo relacionado ao TipoUsuario
        },
        'area': {
            'definicaoArea': f'{area}',  # Este é o campo relacionado ao AreaAtuacao
        }
    }
    user_data_list.append(data)

# Fazendo a requisição POST fora do loop
for user_data in user_data_list:
    response = requests.post(url, json=user_data)

    # Verificando a resposta
    if response.status_code == 201:
        print("Usuário registrado com sucesso!")
        print("Dados do usuário registrado:", response.json())
    else:
        print("Erro ao registrar o usuário:", response.text)