from flask import Flask, request, jsonify, render_template
import threading
import socket
import time
import logging

app = Flask(__name__)
active_broadcasters = []  # Global list to store broadcaster IPs
lock = threading.Lock()  # Lock for thread-safe operations on the active_broadcasters list

logging.basicConfig(level=logging.INFO)

def listen_for_broadcasts():
    broadcast_port = 12345
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as recv_socket:
        recv_socket.bind(('', broadcast_port))
        logging.info(f"Listening for broadcasts on port {broadcast_port}")

        while True:
            data, addr = recv_socket.recvfrom(buffer_size)
            broadcaster_info = {'ip': addr[0], 'username': data.decode()}
            logging.info(f"Received broadcast from {broadcaster_info['username']} ({broadcaster_info['ip']})")

            with lock:
                if broadcaster_info not in active_broadcasters:
                    active_broadcasters.append(broadcaster_info)
                    logging.info(f"Added new broadcaster: {broadcaster_info['username']} ({broadcaster_info['ip']})")

@app.route('/broadcasters')
def broadcasters():
    with lock:
        return jsonify(active_broadcasters)

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/host', methods=['GET', 'POST'])
def host_game():
    if request.method == 'POST':
        try:
            username = request.json['username']
            thread = threading.Thread(target=broadcast_server, args=(username,))
            thread.daemon = True
            thread.start()
            return jsonify({'status': 'Broadcasting', 'username': username})
        except KeyError:
            return jsonify({'error': 'Username is required'}), 400
    return render_template('hostgame.html')

@app.route('/join')
def join_game():
    if not any(thread.name == 'ListenThread' for thread in threading.enumerate()):
        thread = threading.Thread(target=listen_for_broadcasts, name='ListenThread')
        thread.daemon = True
        thread.start()
    return render_template('joingame.html')

@app.route('/acknowledge', methods=['POST'])
def acknowledge():
    data = request.json
    ip = data.get('ip')
    username = data.get('username')
    message = f"Acknowledgment received from {request.remote_addr}"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ack_socket:
            ack_socket.sendto(message.encode(), (ip, 12345))
            logging.info(f"Sent acknowledgment to {username} at IP: {ip}")
        return jsonify({'message': 'Acknowledgment sent successfully'}), 200
    except Exception as e:
        logging.error(f"Failed to send acknowledgment: {e}")
        return jsonify({'error': 'Failed to send acknowledgment'}), 500

def broadcast_server(username):
    broadcast_port = 12345
    message = username

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket:
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while True:
            try:
                broadcast_socket.sendto(message.encode(), ('<broadcast>', broadcast_port))
                logging.info(f"Broadcast sent by {username}.")
                time.sleep(2)
            except Exception as e:
                logging.error(f"Error sending broadcast: {e}")

@app.route('/sharedpage')
def shared_page():
    broadcaster = request.args.get('broadcaster')
    return render_template('sharedpage.html', broadcaster=broadcaster)

if __name__ == '__main__':
    listen_thread = threading.Thread(target=listen_for_broadcasts, name='ListenThread')
    listen_thread.daemon = True
    listen_thread.start()
    app.run(debug=True)
