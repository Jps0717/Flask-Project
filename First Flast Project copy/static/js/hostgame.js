document.addEventListener('DOMContentLoaded', function() {
    const maxPlayers = 2;
    let playerCount = 1;
    const playerStatus = document.getElementById('playerStatus');
    const waitingScreen = document.getElementById('waitingScreen');
    const gameScreen = document.getElementById('gameScreen');
    const reconnectingOverlay = document.createElement('div');

    reconnectingOverlay.id = 'reconnectingOverlay';
    reconnectingOverlay.textContent = 'Reconnecting...';
    document.body.appendChild(reconnectingOverlay);
    reconnectingOverlay.style.display = 'none';

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
        reconnectingOverlay.style.display = 'none';
        socket.emit('request_count', {}, (ack) => {
            if (ack.success) {
                playerCount = 2; // Set player count to 2 upon receiving acknowledgment
                playerStatus.textContent = `Currently joined: ${playerCount} players`;

                if (playerCount >= maxPlayers) {
                    transitionToGame();
                }
            }
        });
    });

    socket.on('connect_error', () => {
        console.error('Connection failed! Trying to reconnect...');
        reconnectingOverlay.style.display = 'block';
    });

    socket.on('update_count', (data) => {
        playerCount = data.count;
        playerStatus.textContent = `Currently joined: ${playerCount} players`;

        if (playerCount >= maxPlayers) {
            transitionToGame();
        }
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        reconnectingOverlay.style.display = 'block';
    });

    function transitionToGame() {
        waitingScreen.style.transition = 'opacity 0.5s ease-out';
        waitingScreen.style.opacity = 0;

        setTimeout(() => {
            waitingScreen.style.display = 'none';
            gameScreen.style.display = 'block';
        }, 500);
    }
});
