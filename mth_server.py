from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
from random import randint
import json


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        def do_GET(self):
            try:    
                if randint(1, 100) <= 30:
                    data = {
                        "value": None,
                        "success": False,
                        'code': 500
                    }
                else:
                    data = {
                        "value": randint(0, 20),
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

def create_server(PORT = 8000):
    server = ThreadingServer(('', PORT), RequestHandler)
    print(f'Multithreaded server running on port {PORT}...')
    server.serve_forever()
create_server()
#py mth_server.py
