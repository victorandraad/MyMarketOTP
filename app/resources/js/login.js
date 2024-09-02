let submitButton = document.getElementById('submit');

submitButton.addEventListener('click', function() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let requisitionError = document.getElementById('requisitionError');

    let formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch('http://localhost:8000/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    }).then(response => {
        return response.json();
    }).then(data => {
        if (data.access_token) {
            saveToken(data.access_token);
            window.location.href = 'http://localhost:5500/app/resources/views/index.html';
        } else {
            requisitionError.innerText = 'Usuário ou senha inválidos';
        }
    }).catch(error => {
        requisitionError.innerText = 'Erro na requisição: ' + error.message;
    });
});

function saveToken(token) {
    localStorage.setItem('token', token);
}