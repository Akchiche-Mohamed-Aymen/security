from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
import time
from random import randint
import json


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

requests_log = {}

MAX_REQUESTS = 5
WINDOW = 10

def check_rate_limit(client_ip):
    now = time.time()
    if client_ip not in requests_log:
        requests_log[client_ip] = []
    requests_log[client_ip] = [
        t for t in requests_log[client_ip]
        if now - t < WINDOW
    ]
    if len(requests_log[client_ip]) > MAX_REQUESTS:
        return True  

    requests_log[client_ip].append(now)
    return False

class RequestHandler(BaseHTTPRequestHandler):
    c = False
    with open('rate_limit.json', 'r') as f:
        c = json.load(f)['enabled']

    def do_GET(self):
        try:
            data = {}
            ip = self.client_address[0]
            if c and check_rate_limit(ip) :
                    data = {
                        "value": None,
                        "success": False , 
                        'code': 429
                    }
            else :
                data = {
                    "value": randint(0, 20) ,
                    "success": True,
                    'code': 200
                }
                sleep(1)
            self.send_response(data['code'])
            self.send_header("Content-type", "application/json")
            response = json.dumps(data)
            response_bytes = response.encode()
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)

        except Exception as e:
            print("Error:", e)
            self.send_error(500)

server = ThreadingServer(('', 8000), RequestHandler)
print('Multithreaded server running on port 8000...')
server.serve_forever()
#py mth_server.py