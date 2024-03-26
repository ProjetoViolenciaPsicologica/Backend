import requests

# Script de teste para filtrar formulários no sistema

url = 'https://projpsi.pythonanywhere.com/api/psicoapp/desvio'

data = {

    'data_inicio': '2024-03-11 00:00',
    'data_fim': '2024-03-15 00:00',
    # 'idade': 15,
    
    # 'usuario': 'Clara Lierica'
}

response = requests.get(url, params=data)

if response.status_code == 200:
    print("Formulários filtrados com sucesso!")
    print("Formulários filtrados:", response.json())
else:
    print("Erro ao filtrar os formulários. Código de status:", response.status_code)
    print("Resposta:", response.text)