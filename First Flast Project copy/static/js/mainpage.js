document.addEventListener('DOMContentLoaded', () => {
    const hostButton = document.getElementById('hostButton');
    const joinButton = document.getElementById('joinButton');
    const usernameInput = document.getElementById('username');

    hostButton.addEventListener('click', function() {
        const username = usernameInput.value.trim();
        if (username === "") {
            showInputError();
        } else {
            sessionStorage.setItem('username', username); // Store username in session storage
            sendUsernameAndNavigate(username, '/host');  // Send username to the server and navigate
        }
    });

    joinButton.addEventListener('click', function() {
        const username = usernameInput.value.trim();
        if (username === "") {
            showInputError();
        } else {
            sessionStorage.setItem('username', username); // Store username in session storage
            navigateTo('/join');  // Navigate to the join route
        }
    });

    usernameInput.addEventListener('input', () => {
        if (usernameInput.value.trim() !== "") {
            clearInputError();
        }
    });

    function sendUsernameAndNavigate(username, url) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username: username})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            navigateTo(url);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function showInputError() {
        usernameInput.classList.add('placeholder-error', 'input-error');
        usernameInput.focus();
    }

    function clearInputError() {
        usernameInput.classList.remove('placeholder-error', 'input-error');
    }

    function navigateTo(url) {
        document.body.classList.add('fade-out');
        setTimeout(() => window.location.href = url, 500);
    }
});
