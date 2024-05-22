import socket
import time
import select

def main():
    broadcast_port = 12345
    ack_port = 12346
    message = "Hello, anyone out there?"
    active_players = {}

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket, \
         socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ack_socket:
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ack_socket.bind(('', ack_port))
        ack_socket.setblocking(0)

        while True:
            # Send a broadcast message
            broadcast_socket.sendto(message.encode(), ('<broadcast>', broadcast_port))
            print(f"Broadcast sent. Currently {len(active_players)} active player(s).")

            # Listen for acknowledgments for 3 seconds
            start_time = time.time()
            while time.time() - start_time < 3:
                ready = select.select([ack_socket], [], [], 1)
                if ready[0]:
                    data, addr = ack_socket.recvfrom(1024)
                    player_ip = addr[0]
                    if player_ip not in active_players:
                        active_players[player_ip] = time.time()
                        print(f"New player joined: {player_ip}")
                    else:
                        active_players[player_ip] = time.time()  # Update last seen time

            # Remove players who haven't acknowledged in the last 6 seconds
            current_time = time.time()
            to_remove = [ip for ip, last_seen in active_players.items() if current_time - last_seen > 6]
            for ip in to_remove:
                del active_players[ip]
                print(f"Player {ip} removed due to timeout.")

            time.sleep(3)  # Wait before the next broadcast

if __name__ == '__main__':
    main()
