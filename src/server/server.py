from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from time import sleep
import threading


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    listening_connections: list["Handler"] = []

    def send(self, content: str, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode())

    def send_json(self, content: dict, code=200):
        JSON = json.dumps(content)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(JSON)))
        self.end_headers()
        self.wfile.write(JSON.encode())

    @property
    def json(self):
        length = int(self.headers.get("content-length", 0))
        return json.loads(self.rfile.read(length).decode())

    @staticmethod
    def run_news(request: "Handler", updated_urls: bytes):
        request.wfile.write(b"data: ")
        request.wfile.write(updated_urls)
        request.wfile.write(b"\r\n\r\n")

    def do_GET(self):
        if self.path == "/listen":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            self.flush_headers()
            self.wfile.flush()
            with open("./images/urls.json", "rb") as f:
                updated_urls = f.read()
            self.run_news(self, updated_urls)
            self.listening_connections.append(self)

        elif self.path.endswith(".png"):
            try:
                with open("./images" + self.path, "rb") as f:
                    img = f.raw.read()
                size = str(len(img))
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Cache-Control", "no-cache, no-store")
                self.send_header("Content-Length", size)
                self.send_header("Connection", "keep-alive")
                self.end_headers()
                self.wfile.write(img)
                self.wfile.flush()
                return
            except FileNotFoundError:
                self.send("Not Found", 404)

        else:
            try:
                if self.path == "/":
                    self.path = "/index.html"
                with open("./public" + self.path, "rb") as f:
                    file = f.read()
                self.send_response(200)
                self.send_header("Content-Length", str(len(file)))
                self.end_headers()
                self.wfile.write(file)
            except FileNotFoundError:
                self.send("Not Found", 404)
            except IsADirectoryError:
                self.send("Not Found", 404)
                return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 80), Handler)
    server.handler = Handler
    print("Server started on http://localhost")

    def update_news(connections: list[Handler]):
        while True:
            print("updating news")
            with open("./images/urls.json", "rb") as f:
                updated_urls = f.read()
            for connection in connections:
                print(f"doing {connection.address_string()}")
                try:
                    Handler.run_news(connection, updated_urls)
                except OSError:
                    print(
                        f"removing {connection.address_string()} - no longer connected"
                    )
                    connections.remove(connection)
            sleep(60)

    threading.Thread(
        target=update_news, args=(server.handler.listening_connections,), daemon=True
    ).start()

    server.serve_forever()
