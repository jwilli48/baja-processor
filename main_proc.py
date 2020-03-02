import http.server
import threading
import accel_proxy as ap
import serial
import time
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


server_address = ('localhost', 8080)
httpd = http.server.HTTPServer(server_address, ServerHandler)

thread = threading.Thread(target=httpd.serve_forever, args=[.1])
thread.start()

ameter = ap.AccelProxy()
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate='115200',
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
packets = 0

while True:
    # read data
    x, y, z = [value for value in ameter.read_xyz()]
    data_str = '%0.3f %0.3f %0.3f' % (x, y, z)

    # print so pi can save data to file
    print(data_str)

    # send data
    packets = packets + 1
    ser.write(('%d %0.3f %0.3f %0.3f' % (packets, x, y, z)).encode("ascii"))

    # save to simple server
    requests.post('http://localhost:8080', data=data_str)
    # small delay
    time.sleep(0.2)
