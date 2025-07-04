import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

STORAGE_DIR = './storage'

class HttpServer:
    def __init__(self):
        self.sessions = {}
        self.types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.txt': 'text/plain',
            '.html': 'text/html'
        }

    def response(self, kode=404, message='Not Found', messagebody=bytes(), headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = []
        resp.append("HTTP/1.0 {} {}\r\n".format(kode, message))
        resp.append("Date: {}\r\n".format(tanggal))
        resp.append("Connection: close\r\n")
        resp.append("Server: myserver/1.0\r\n")
        resp.append("Content-Length: {}\r\n".format(len(messagebody)))
        for kk in headers:
            resp.append("{}: {}\r\n".format(kk, headers[kk]))
        resp.append("\r\n")

        if type(messagebody) != bytes:
            messagebody = messagebody.encode()

        response_headers = ''.join(resp).encode()
        return response_headers + messagebody

    def proses(self, data):
        try:
            lines = data.split("\r\n")
            if not lines:
                return self.response()

            request_line = lines[0]
            method, path, *_ = request_line.split()

            if method == 'GET' and path == '/list':
                files = os.listdir(STORAGE_DIR)
                return self.response(200, "OK", "\n".join(files))

            elif method == 'POST' and path == '/upload':
                filename = lines[1].strip()
                body_index = data.find("\r\n\r\n")
                content = data[body_index+4:] if body_index != -1 else ""

                if not filename:
                    return self.response(400, "Bad Request", "Filename missing")
                if not content.strip():
                    return self.response(400, "Bad Request", "No file content")

                filepath = os.path.join(STORAGE_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return self.response(200, "OK", f"File '{filename}' uploaded")

            elif method == 'DELETE' and path.startswith('/delete'):
                query = parse_qs(urlparse(path).query)
                filename = query.get('file', [None])[0]
                if not filename:
                    return self.response(400, "Bad Request", "Missing file parameter")

                filepath = os.path.join(STORAGE_DIR, filename)
                if not os.path.exists(filepath):
                    return self.response(404, "Not Found", "File not found")

                os.remove(filepath)
                return self.response(200, "OK", f"File '{filename}' deleted")

            else:
                return self.response(404, "Not Found", "Route not found")

        except Exception as e:
            return self.response(500, "Internal Server Error", f"Exception: {str(e)}")
