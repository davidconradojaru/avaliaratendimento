function setRating(rating) {
    // Exibe o emoji correspondente ao rating
    switch (rating) {
        case 1:
            document.getElementById('result').textContent = '😡';
            break;
        case 2:
            document.getElementById('result').textContent = '😠';
            break;
        case 3:
            document.getElementById('result').textContent = '😐';
            break;
        case 4:
            document.getElementById('result').textContent = '🙂';
            break;
        case 5:
            document.getElementById('result').textContent = '😄';
            break;
        default:
            document.getElementById('result').textContent = '-';
    }
}



function fadeIn(element) {
    var opacity = 0;
    var interval = setInterval(function() {
        if (opacity < 1) {
            opacity += 0.1;
            element.style.opacity = opacity;
        } else {
            clearInterval(interval);
            element.textContent = 'OBRIGADO POR COMPRAR NA NOVALAR!!!';
        }
    }, 100);
}

// ANIMAÇÃO DO TEXTO
const animatedText = document.getElementById('animatedText');
let yPos = 0; // Posição vertical inicial
let direction = 1; // Direção inicial

// Função para animar o texto
function animateText() {
    // Muda a posição vertical do texto
    yPos += direction;
    animatedText.style.transform = `translateY(${yPos}px)`;

    // Inverte a direção quando o texto atinge um limite
    if (yPos >= 10 || yPos <= -10) {
        direction *= -1;
    }

    // Chama esta função novamente após um curto intervalo de tempo para criar a animação contínua
    requestAnimationFrame(animateText);
}


function setRating(rating) {
    document.getElementById('result').textContent = rating;
    document.getElementById('rating').style.display = 'none';
    var resultContainer = document.getElementById('resultContainer');
    resultContainer.style.display = 'block';
    var thankYouMessage = document.getElementById('thankYouMessage');
    thankYouMessage.style.opacity = '1';
}
// Inicia a animação
animateText();


//REQUISIÇÕES A API PYTHON

// Função para obter o idVendedor e o nome do vendedor da API Python
function getVendedorInfo() {
    // Fazer uma requisição à API Python
    fetch('sua_api_python/endpoint_para_obter_vendedor_info')
        .then(response => response.json())
        .then(data => {
            // Atualizar o campo no HTML com os dados obtidos da API
            document.getElementById('idVendedor').textContent = data.idVendedor;
            document.getElementById('nomeVendedor').textContent = data.nomeVendedor;
        })
        .catch(error => console.error('Erro ao obter informações do vendedor:', error));
}

// Chamada à função para obter o idVendedor e o nome do vendedor
getVendedorInfo();
