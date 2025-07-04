import socket
import os

SERVER_HOST = 'localhost'
SERVER_PORT = 45000

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(request.encode())
        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data
    return response.decode()

def list_files():
    req = "GET /list HTTP/1.0\r\n\r\n"
    print(send_request(req))

def upload_file():
    filepath = input("Masukkan path file (misalnya testing.txt): ").strip()
    if not os.path.exists(filepath):
        print("❌ File tidak ditemukan.")
        return

    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    req = f"POST /upload HTTP/1.0\r\n{filename}\r\n\r\n{content}"
    print(send_request(req))

def delete_file():
    filename = input("Masukkan nama file yang ingin dihapus: ").strip()
    req = f"DELETE /delete?file={filename} HTTP/1.0\r\n\r\n"
    print(send_request(req))

def menu():
    while True:
        print("\nMenu Client:")
        print("1. Lihat daftar file")
        print("2. Upload file")
        print("3. Hapus file")
        print("4. Keluar")
        choice = input("Pilihanmu: ").strip()

        if choice == '1':
            list_files()
        elif choice == '2':
            upload_file()
        elif choice == '3':
            delete_file()
        elif choice == '4':
            break
        else:
            print("❗ Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
