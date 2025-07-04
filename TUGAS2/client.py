import socket

def main():
    host = '127.0.0.1'
    port = 45000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Terhubung ke server.")

        while True:
            msg = input("Ketik 'TIME' atau 'QUIT': ").strip()
            if not msg:
                continue

            s.sendall((msg + "\r\n").encode('utf-8'))

            if msg == "QUIT":
                print("Keluar dari server.")
                break

            data = s.recv(1024).decode('utf-8')
            print(f"Respon dari server: {repr(data)}")

if __name__ == "__main__":
    main()
