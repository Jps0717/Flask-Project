function fetchBroadcasters() {
    fetch('/broadcasters')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('broadcastersList');
            list.innerHTML = ''; // Clear the list before updating
            if (data.length === 0) {
                list.textContent = 'No broadcasters available at the moment.';
            } else {
                data.forEach(broadcaster => {
                    const joinButton = document.createElement('button');
                    joinButton.textContent = `Join ${broadcaster.username}`;
                    joinButton.value = broadcaster.ip; // Set the IP address as the value of the button
                    joinButton.addEventListener('click', () => {
                        joinBroadcaster(broadcaster.ip, broadcaster.username);
                    });
                    list.appendChild(joinButton);
                });
            }
        })
        .catch(error => {
            console.error('Failed to fetch broadcasters:', error);
            document.getElementById('broadcastersList').textContent = 'Failed to load broadcaster IPs. Please try again later.';
        });
}

function joinBroadcaster(ip, username) {
    console.log(`Joining broadcaster at IP: ${ip}`);
    fetch('/acknowledge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: ip, username: username })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Failed to send acknowledgment:', error);
    });
}

// Fetch broadcasters every 5 seconds
setInterval(fetchBroadcasters, 5000);
fetchBroadcasters(); // Also fetch immediately on page load
