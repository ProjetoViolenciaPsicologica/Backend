async function getData(token, params) {
    // Constrói a string de consulta a partir dos parâmetros
    const queryString = new URLSearchParams(params).toString();
    const url = `https://projpsi.pythonanywhere.com/api/psicoapp/graficosPDF?${queryString}`;

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }

    const data = await response.json();
    return data;
}

async function loadImages() {
    const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2ODYxODA4LCJpYXQiOjE3MTY0Mjk4MDgsImp0aSI6IjJlMmM5NmRiMDZjYTQ5MjliZjZjN2I0ZjBlYjZhMDg4IiwidXNlcl9pZCI6MSwibmFtZSI6IkFETUlOIEFETUlOIiwidGlwbyI6Imhvc3BpdGFsIiwiYXJlYSI6IkFnZW50ZSBkZSBFZHVjYVx1MDBlN1x1MDBlM28iLCJpc19zdXBlcnVzZXIiOnRydWV9.X6S9jrmIX_5MPdC9Ib9MD8raje5rknhlIGLxlU4cImA";
    const params = {
        // Adicione aqui os seus parâmetros de consulta
        //idade_min: 0,
        //idade_max: 25,
    };
    try {
        const dados_base64 = await getData(token, params);

        // Verifica se a resposta contém todas as chaves esperadas
        const requiredKeys = ['Dispersao', 'Desvio', 'Barra', 'Pizza'];
        //const requiredKeys = ['Dispersao', 'Barra', 'Pizza'];
        for (const key of requiredKeys) {
            if (!dados_base64[key]) {
                throw new Error(`Resposta da API não contém a chave "${key}"`);
            }
        }

        // Obtém as imagens da resposta
        const imagem1 = dados_base64.Dispersao;
        const imagem2 = dados_base64.Desvio;
        const imagem3 = dados_base64.Barra;
        const imagem4 = dados_base64.Pizza;

        // Cria novas imagens
        const img1 = new Image();
        const img2 = new Image();
        const img3 = new Image();
        const img4 = new Image();

        // Define a fonte das imagens como o resultado da decodificação do código base64
        img1.src = "data:image/png;base64," + imagem1;
        img2.src = "data:image/png;base64," + imagem2;
        img3.src = "data:image/png;base64," + imagem3;
        img4.src = "data:image/png;base64," + imagem4;

        // Adiciona as imagens aos elementos div correspondentes
        document.getElementById("imagem-container").appendChild(img1);
        document.getElementById("imagem-container2").appendChild(img2);
        document.getElementById("imagem-container3").appendChild(img3);
        document.getElementById("imagem-container4").appendChild(img4);
    } catch (error) {
        console.error('Erro ao carregar as imagens:', error);
    }
}

// Chama a função para carregar as imagens
loadImages();
