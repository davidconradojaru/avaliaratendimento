// Adicione um ouvinte de evento ao formulário de login
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Evita o envio do formulário padrão

    var email = document.getElementById("email").value;
    var senha = document.getElementById("senha").value;

    if (email === "" || senha === "") {
        alert("Por favor, preencha todos os campos.");
    } else {
        // Construa o corpo da solicitação
        var body = JSON.stringify({ email: email, senha: senha });

        // Faça a solicitação POST para o endpoint de login
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        })
        .then(function(response) {
            // Verifique se a resposta foi bem-sucedida
            if (response.ok) {
                // Se o login for bem-sucedido, redirecione o usuário para outra página
                window.location.href = "index.html";
            } else {
                // Se o login falhar, exiba uma mensagem de erro
                alert("Erro ao fazer login. Verifique suas credenciais.");
            }
        })
        .catch(function(error) {
            // Se ocorrer um erro durante a solicitação, exiba uma mensagem de erro
            console.error('Ocorreu um erro:', error);
            alert("Ocorreu um erro ao processar a solicitação. Por favor, tente novamente mais tarde.");
        });

        // Adicione um log para registrar a tentativa de login
        console.log('Tentativa de login para o usuário:', email);
    }
});

// Adicione um evento de clique ao ícone de olho para alternar a visibilidade da senha
document.getElementById("togglePassword").addEventListener("click", function() {
    var senhaField = document.getElementById("senha");
    var toggleBtn = document.getElementById("togglePassword");
    if (senhaField.type === "password") {
        senhaField.type = "text";
        toggleBtn.textContent = "🔒";
    } else {
        senhaField.type = "password";
        toggleBtn.textContent = "👁️";
    }
});
