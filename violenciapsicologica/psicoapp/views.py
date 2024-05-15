# views de uma aplicação Django

import matplotlib.pyplot as plt
import numpy as np

import io
import base64

def get_dispersao(queryset):
    # Criando um buffer de memória para salvar o gráfico
    buffer = io.BytesIO()

    #  Dispersao
    valores_idade = []
    valores_pontuacao = []

    for query in queryset:
        valores_idade.append(query.idade)
        valores_pontuacao.append(query.sinalizacao_quantidade())

    # Calculando os coeficientes da regressão linear
    coefficients = np.polyfit(valores_idade, valores_pontuacao, 1)
    m = coefficients[0]  # Coeficiente angular
    b = coefficients[1]  # Coeficiente linear

    # Criando uma nova figura
    plt.figure()

    # Criando o gráfico de dispersão
    plt.scatter(valores_idade, valores_pontuacao)

    # Adicionando a linha de regressão
    plt.plot(valores_idade, m*np.array(valores_idade) + b, color='red')

    # Adicionando rótulos aos eixos
    plt.xlabel('Idade')
    plt.ylabel('Pontuação')

    # Adicionando um título
    plt.title('Gráfico de Dispersão entre Idade e Pontuação')

    # Salvando o gráfico no buffer
    plt.savefig(buffer, format='png')

    # Convertendo o buffer para base64
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return image_base64

def get_desvio(queryset):
    # Criando um buffer de memória para salvar o gráfico
    buffer = io.BytesIO()

    valores_pontuados_verdes = []
    valores_pontuados_amarelo = []
    valores_pontuados_vermelho = []

    for query in queryset:
        if query.sinalizacao() == "Vermelho":
            valores_pontuados_vermelho.append(query.sinalizacao_quantidade())
        elif query.sinalizacao() == "Amarelo":
            valores_pontuados_amarelo.append(query.sinalizacao_quantidade())
        else:
            valores_pontuados_verdes.append(query.sinalizacao_quantidade())

    desvio_padrao_verde = np.std(valores_pontuados_verdes)
    desvio_padrao_amarelo = np.std(valores_pontuados_amarelo)
    desvio_padrao_vermelho = np.std(valores_pontuados_vermelho)

    medias = [(sum(valores_pontuados_verdes) / len(valores_pontuados_verdes)), (sum(valores_pontuados_amarelo) / len(valores_pontuados_amarelo)), (sum(valores_pontuados_vermelho) / len(valores_pontuados_vermelho))]
    desvios = [desvio_padrao_verde, desvio_padrao_amarelo, desvio_padrao_vermelho]
    labels = ['Verde', 'Amarelo', 'Vermelho']

    # Criando uma nova figura
    plt.figure()

    plt.bar(labels, medias, yerr=desvios, capsize=3)

    # Adicionando rótulos e título
    plt.xlabel('Avaliação')
    plt.ylabel('Pontuação')
    plt.title('Gráfico de Barras com Desvio Padrão')

    # Salvando o gráfico no buffer
    plt.savefig(buffer, format='png')

    # Convertendo o buffer para base64
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return image_base64



