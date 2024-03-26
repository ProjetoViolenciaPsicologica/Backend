import requests

# Script de teste para filtrar formulários no sistema

url = 'https://projpsi.pythonanywhere.com/api/psicoapp/formulario/filtro/'

data = {
    # 'data_inicio': '2024-03-07 00:00',
    # 'data_fim': '2024-03-08 00:00',
    #'local_aplicacao': 'escola',
    #'area' : 'Saúde',
    'idade': 24,
}

response = requests.get(url, params=data)

if response.status_code == 200:
    print("Formulários filtrados com sucesso!")
    print("Formulários filtrados:", response.json())
else:
    print("Erro ao filtrar os formulários. Código de status:", response.status_code)
    print("Resposta:", response.text)