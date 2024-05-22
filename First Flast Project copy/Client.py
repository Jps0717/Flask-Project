import socket

def main():
    broadcast_port = 12345
    ack_port = 12346
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as recv_socket, \
         socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as send_socket:
        recv_socket.bind(('', broadcast_port))
        print(f"Listening for broadcasts on port {broadcast_port}")

        while True:
            data, addr = recv_socket.recvfrom(buffer_size)
            print(f"Received message from {addr[0]}: {data.decode()}")

            ack_message = "Acknowledgment received"
            send_socket.sendto(ack_message.encode(), (addr[0], ack_port))
            print(f"Sent acknowledgment to {addr[0]}")

if __name__ == '__main__':
    main()
