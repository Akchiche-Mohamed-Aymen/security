from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint
import json
import time

rate_limit = 4
time_window = 1         
punishment_time = 2     
req = {}
class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


class RequestHandler(BaseHTTPRequestHandler):

    def is_blocked(self, ip):
        if ip in req and "blocked_until" in req[ip]:
            if time.time() < req[ip]["blocked_until"]:
                return True
        return False
    def do_GET(self):
            with open("enable.json", "r") as f:
                self.enable_security = json.load(f)["enabled"]
                print(f"--------------------> {self.enable_security}")
            ip = self.client_address[0]
            now = time.time()
            if ip not in req:
                req[ip] = {
                    "count": 0,
                    "start_time": now,
                    "blocked_until": 0
                }

            user = req[ip]

            #  Check punishment (temporary blocking)
            if now < user["blocked_until"] and self.enable_security:
                self.send_response(429)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Too many requests. Temporarily blocked.",
                    "code": 429
                }).encode())
                return

            # 🔄 Reset window if 10 seconds passed
            if now - user["start_time"] > time_window and self.enable_security:
                user["count"] = 0
                user["start_time"] = now

            user["count"] += 1

            # ❌ Rate limit exceeded → apply punishment
            if user["count"] > rate_limit and self.enable_security:
                user["blocked_until"] = now + punishment_time
                user["count"] = 0

                self.send_response(429)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Rate limit exceeded. You are temporarily blocked.",
                    "code": 429
                }).encode())
                return

            try:
                if randint(1, 100) <= 30:
                    data = {
                        "value": None,
                        "success": False,
                        "code": 500
                    }
                else:
                    data = {
                        "value": randint(0, 20),
                        "success": True,
                        "code": 200
                    }

                self.send_response(data['code'])
                self.send_header("Content-type", "application/json")

                response = json.dumps(data).encode()
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)

            except Exception as e:
                print("Error:", e)
                self.send_error(500)


def create_server(PORT=8000):
    server = ThreadingServer(('', PORT), RequestHandler)
    print(f"Server running on port {PORT}...")
    server.serve_forever()


