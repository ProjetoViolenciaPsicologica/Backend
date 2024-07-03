# views de uma aplicação Django

import matplotlib.pyplot as plt
import numpy as np

import io
import base64

def get_dispersao(queryset):
    try:
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
        plt.figure(figsize=(10, 10))

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

        # Limpando o buffer de memória
        buffer.close()  # ou buffer.truncate(0)
        return image_base64
    except Exception as e:
        return f"Erro ao gerar gráfico: {e}"

def get_desvio(queryset):
    try:
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

        medias = []
        desvios = []
        labels = ['Verde', 'Amarelo', 'Vermelho']

        # Calculando média e desvio padrão apenas se houver valores na lista correspondente
        for valores_pontuados in [valores_pontuados_verdes, valores_pontuados_amarelo, valores_pontuados_vermelho]:
            if valores_pontuados:
                media = sum(valores_pontuados) / len(valores_pontuados)
                desvio_padrao = np.std(valores_pontuados)
            else:
                media = 0
                desvio_padrao = 0
            medias.append(media)
            desvios.append(desvio_padrao)

        # Criando uma nova figura
        plt.figure(figsize=(10, 10))

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

        # Limpando o buffer de memória
        buffer.close()  # ou buffer.truncate(0)
        return image_base64
    except Exception as e:
        return f"Erro ao gerar imagem: {e}"

def get_pizza(queryset):
    try:
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

        sinal = ['Verde', 'Amarelo', 'Vermelho']
        valores = [sum(valores_pontuados_verdes), sum(valores_pontuados_amarelo), sum(valores_pontuados_vermelho)]
        # Criando uma nova figura
        plt.figure(figsize=(10, 10))
        plt.pie(valores, labels=sinal, autopct='%1.1f%%', startangle=90, colors=['green', 'yellow', 'red'])
        plt.title('Sinalização de Questionários')

        # Salvando o gráfico no buffer
        plt.savefig(buffer, format='png')

        # Convertendo o buffer para base64
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # Limpando o buffer de memória
        buffer.close()  # ou buffer.truncate(0)
        return image_base64
    except Exception as e:
        return f"Erro ao gerar gráfico: {e}"

def get_bar(queryset):
    try:
        # Criando um buffer de memória para salvar o gráfico
        buffer = io.BytesIO()

        nunca = 0
        as_vezes = 0
        frequentemente = 0
        sempre = 0

        for formulario in queryset:
            questoes = formulario.obter_array()
            for questao in questoes:
                if questao == "1":
                    nunca+=1
                else:
                    if questao == "2":
                        as_vezes +=1
                    else:
                        if questao == "3":
                            frequentemente+=1
                        else:
                            sempre +=1

        categorias = ['Nunca', 'Sempre', 'Às vezes', 'Frequentemente']
        valores = [nunca, sempre, as_vezes, frequentemente]
        # Criando uma nova figura
        plt.figure(figsize=(10, 10))
        plt.barh(categorias, valores, color='skyblue')
        plt.xlabel('Respostas')
        plt.ylabel('Opções')
        plt.title('Opções escolhidas do questionário')

        # Salvando o gráfico no buffer
        plt.savefig(buffer, format='png')

        # Convertendo o buffer para base64
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # Limpando o buffer de memória
        buffer.close()  # ou buffer.truncate(0)
        return image_base64
    except Exception as e:
        return f"Erro ao gerar gráfico: {e}"
