// Função para gerar o QR code com dados pré-preenchidos
function gerarQRCodeComDados(nome, id) {
    const qr = qrcode(0, 'L'); // Criar um novo objeto QRCode
    const dados = "Nome: " + nome + ", ID: " + id; // Concatenar os dados do vendedor
    qr.addData(dados); // Adicionar os dados ao QRCode
    qr.make(); // Gerar o QRCode
    const qrCodeImage = qr.createSvgTag({ // Criar a tag <svg> para o QRCode
        margin: 2, // Margem em torno do QRCode
        scale: 4 // Escala do QRCode
    });
    document.getElementById('qrcode').innerHTML = qrCodeImage; // Inserir o QRCode na página HTML
}

// Chamar a função para gerar o QR code com os dados do vendedor
gerarQRCodeComDados("Nome do Vendedor", "ID do Vendedor");












// Função assíncrona para capturar o evento de escaneamento do QR code

async function capturarQRCode() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    const video = document.createElement('video');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        video.srcObject = stream;
        await video.play();

        // Aguardar 2 segundos para que a câmera ajuste a exposição e foco
        await new Promise(resolve => setTimeout(resolve, 2000));

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);

        decodeQRCode(imageData);
    } catch (error) {
        console.error('Erro ao acessar a câmera:', error);
    } finally {
        // Parar o vídeo e liberar o stream
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }
    }
}

// Chamar a função para capturar o QR code quando a página carregar
window.onload = function() {
    capturarQRCode();
};



