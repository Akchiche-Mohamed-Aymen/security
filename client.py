from random import randint
import socket
import threading
import time
import json

HOST = "127.0.0.1"
PORT = 8000
Limit = 4
success_count = {'sum': 0 }
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
            
            parts = response.split("\r\n\r\n")
            body = parts[1] if len(parts) > 1 else ""
            message = ''
            # Parse JSON response
            if body:
                data = json.loads(body)
                message = f"[Client {client_id}] Request {i+1} -> getting : {data['value']} in security exam"
                if data['success']:
                    success_count['sum'] += 1
            else:
                message = f"[Client {client_id}] Request {i+1} -> No response body"
            s.close()
            end = time.time()
            latency = end - start
            print(f"{message} | latency: {latency:.2f} seconds")

        except Exception as e:
            print(f"[Client {client_id}] Error: {type(e).__name__}: {e}")


def run_simulation(num_clients=10 , type_request = 1) :
    threads = []
    start_time = time.time()
    requests = []
    for i in range(num_clients):
        if type_request == 1:
            requests_per_client = randint(1, 5)
        elif type_request == 2:
            requests_per_client = randint(6, 10)
        else:
            requests_per_client = randint(10, 20)
        requests.append(requests_per_client)
        t = threading.Thread(
            target=client_task,
            args=(i, requests_per_client)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    print("\n--- Simulation Finished ---")
    total_requests = sum(requests)
    total_time = end_time - start_time
    print(f"Total requests: {total_requests}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f'Throughput: {success_count["sum"] / total_time:.2f} requests/sec')
    print(f"Total successful responses: {success_count['sum']} / {total_requests} ")
    print(f'Failed responses: {total_requests - success_count["sum"]}  requests')


if __name__ == "__main__":
    print('Choice 1: Low load (5 clients, 2 requests each)')
    print('Choice 2: Medium load (10 clients, 5 requests each)')
    print('Choice 3: High load (20 clients, 10 requests each)')
    choice = int(input("Enter your choice (1-3): "))
    if choice == 1:
        run_simulation(num_clients=5, type_request = choice)
    elif choice == 2:
        run_simulation(num_clients=10, type_request = choice)
    else:
        run_simulation(num_clients=20, type_request = choice)

#py client.py