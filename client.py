from random import randint
import socket
import threading
import time
import json
from pandas import DataFrame
stats = {}
HOST = "127.0.0.1"
PORT = 8000
Limit = 4
def client_task(client_id, requests_count ):
    for i in range(requests_count):
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            request = request = (
    "GET / HTTP/1.1\r\n"
    "Host: 127.0.0.1:8000\r\n"
    "Connection: close\r\n"
    "\r\n"
)
            s.send(request.encode())
            response = b""

            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk

            response = response.decode()
            blocked = False
            parts = response.split("\r\n\r\n")
            body = parts[1] if len(parts) > 1 else ""
            status = None
            if body:
                data = json.loads(body)
                
                status = data['success']
                if 'error' in data:
                       blocked = True
                                             
            else:
                status = False
            s.close()
            end = time.time()
            latency = end - start  
            stats[client_id + 1][f"request_{i+1}"] = {'latency': latency  , 'status' : status } 
            with open("enable.json", "r") as f:
                enable_security = json.load(f)["enabled"]
            if enable_security:
                stats[client_id + 1][f"request_{i+1}"]['blocked'] = blocked

        except Exception as e:
            print(f"[Client {client_id}] Error: {type(e).__name__}: {e}")


       
def run_simulation(requests , num_clients=10 ) :
    threads = []
    with open("enable.json", "r") as f:
                enable_security = json.load(f)["enabled"]
    start_time = time.time()
    for i in range(num_clients):
        stats[i + 1] = {'requests': requests[i]}
        t = threading.Thread(
            target=client_task,
            args=(i, requests[i])
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    total_requests = sum(requests)
    total_time = end_time - start_time
    stats['total_requests'] = total_requests
    stats['total_time'] = round(total_time, 2)
    if not enable_security:
       with open("stats_without_security.json", "w") as f:
           json.dump(stats, f , indent=4)
    else :
        with open("stats_with_security.json", "w") as f:
           json.dump(stats, f , indent=4)
    return stats
                



#py client.py