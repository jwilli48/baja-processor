import http.server
import threading
import requests


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.x, self.y, self.z = (0.0, 0.0, 0.0)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        self.wfile.write(
            bytes(str(self.x) + ' ' + str(self.y) + ' ' + str(self.z), 'utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = str(self.rfile.read(content_length), 'utf-8')
        self.x, self.y, self.z = [float(value) for value in body.split(' ')]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Response received' + bytes(body, 'utf-8'))


class ServerFacade:
    def __init__(self, host='localhost', port=8080, polling_interval=.1):
        self.server_address = (host, port)
        self.polling_interval = .1
        self.httpd = None

    def start_server(self):
        self.httpd = http.server.HTTPServer(self.server_address, ServerHandler)
        thread = threading.Thread(target=self.httpd.serve_forever, argsd=[
                                  self.polling_interval])
        thread.start()

    def save_data(self, data_str):
        requests.post(
            self.get_server_url(), data=data_str)

    def get_server_url(self):
        return 'http://%s:%d' % (self.server_address[0], self.server_address[1])
