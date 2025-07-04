import socket
import threading
from datetime import datetime

def handle_client(conn, addr):
    print(f"[TERHUBUNG] {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"[DARI {addr}] {repr(data)}")

            if data.strip() == "TIME":
                now = datetime.now()
                waktu = now.strftime("%H:%M:%S")
                response = f"JAM {waktu}\r\n"
                conn.sendall(response.encode('utf-8'))
            elif data.strip() == "QUIT":
                break

    print(f"[PUTUS] {addr}")

def main():
    host = '0.0.0.0'
    port = 45000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[INFO] Server berjalan di port {port}...\n")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[MATI] Server mati.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
