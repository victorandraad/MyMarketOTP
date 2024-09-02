let submitButton = document.getElementById('submit');

submitButton.addEventListener('click', function() { 
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let email = document.getElementById('email').value;

    let usernameError = document.getElementById('usernameError');
    let passwordError = document.getElementById('passwordError');
    let emailError = document.getElementById('emailError');
    let requisitionError = document.getElementById('requisitionError');

    username = username.trim();
    password = password.trim();
    email = email.trim();

    usernameError.innerText = validateUsername(username)? validateUsername(username): '';
    passwordError.innerText = validatePassword(password)? validatePassword(password): '';
    emailError.innerText = validateEmail(email)? validateEmail(email): '';

    if (usernameError.innerText.length > 0 || passwordError.innerText.length > 0 || emailError.innerText.length > 0) {
        return;
    }

    let data = {
        username: username,
        password: password,
        email: email,
    };

    fetch('http://127.0.0.1:8000/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        return response.json(); // Convertendo a resposta em JSON
    }).then(data => {
        if (data.status === 200) {
            window.location.href = 'http://127.0.0.1:5500/app/resources/views/login.html';
        } else {
            requisitionError.innerText = data.detail;
        }
    }).catch(error => {
        console.error('Erro na requisição:', error);
    });    
});

function validateEmail(email) {
    if (email.length === 0) {
        return "Campo obrigatório";
    }

    let re = /\S+@\S+\.\S+/;
    if (!re.test(email)) {
        return "Email inválido";
    }
}

function validatePassword(password) {
    if (password.length === 0) {
        return "Campo obrigatório";
    }

    if (password.length < 8 || password.length > 32) {
        return "Senha deve ter entre 8 e 32 caracteres";
    }
}

function validateUsername(username) {
    if (username.length === 0) {
        return "Campo obrigatório";
    }
   
    if (username.length < 3 || username.length > 25) {
        return "Nome de usuário deve ter entre 3 e 25 caracteres";
    }

    // Verifica se o nome de usuário contém apenas letras e números
    let re = /^[a-zA-Z0-9]+$/;
    if (!re.test(username)) {
        return "Nome de usuário deve conter apenas letras e números";
    }
    
}