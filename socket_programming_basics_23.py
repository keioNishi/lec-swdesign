# -*- coding: utf-8 -*-
"""
Socket Programming Basics - Module for 23
Basic socket communication demonstration (English version for better compatibility)
"""

import socket
import threading
import time


class BasicSocketDemo:
    """Basic socket communication demonstration"""

    def __init__(self):
        self.host = 'localhost'
        self.tcp_port = 8001
        self.udp_port = 8002

    def create_tcp_socket(self):
        """Create and configure TCP socket"""
        print("=== TCP Socket Creation ===")

        # Create TCP socket (AF_INET=IPv4, SOCK_STREAM=TCP)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("TCP socket created successfully")

        # Display socket information
        print(f"Socket type: {tcp_socket.type}")
        print(f"Socket family: {tcp_socket.family}")

        tcp_socket.close()
        print("TCP socket closed\n")

    def create_udp_socket(self):
        """Create and configure UDP socket"""
        print("=== UDP Socket Creation ===")

        # Create UDP socket (AF_INET=IPv4, SOCK_DGRAM=UDP)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP socket created successfully")

        # Display socket information
        print(f"Socket type: {udp_socket.type}")
        print(f"Socket family: {udp_socket.family}")

        udp_socket.close()
        print("UDP socket closed\n")

    def tcp_server_demo(self):
        """Simple TCP server demonstration"""
        print("=== TCP Server Demo ===")

        try:
            # Create server socket and bind
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.tcp_port))
            server_socket.listen(1)

            print(f"TCP server listening on {self.host}:{self.tcp_port}...")

            # Set timeout for testing
            server_socket.settimeout(2.0)

            try:
                client_socket, client_address = server_socket.accept()
                print(f"Client {client_address} connected")

                # Receive data
                data = client_socket.recv(1024)
                print(f"Received data: {data.decode('utf-8')}")

                # Send response
                response = "Hello from TCP Server!"
                client_socket.send(response.encode('utf-8'))

                client_socket.close()

            except socket.timeout:
                print("Timeout: No client connection received")

        except Exception as e:
            print(f"TCP server error: {e}")
        finally:
            server_socket.close()
            print("TCP server terminated\n")

    def tcp_client_demo(self):
        """Simple TCP client demonstration"""
        print("=== TCP Client Demo ===")

        try:
            # Create client socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server
            client_socket.connect((self.host, self.tcp_port))
            print(f"Connected to TCP server {self.host}:{self.tcp_port}")

            # Send data
            message = "Hello from TCP Client!"
            client_socket.send(message.encode('utf-8'))
            print(f"Sent data: {message}")

            # Receive response
            response = client_socket.recv(1024)
            print(f"Received data: {response.decode('utf-8')}")

        except Exception as e:
            print(f"TCP client error: {e}")
        finally:
            client_socket.close()
            print("TCP client terminated\n")

    def socket_info_demo(self):
        """Socket information retrieval demonstration"""
        print("=== Socket Information Retrieval ===")

        # Get host information
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print(f"Hostname: {hostname}")
        print(f"Local IP: {local_ip}")

        # Get external service information (e.g., Google DNS)
        try:
            google_ip = socket.gethostbyname('google.com')
            print(f"google.com IP: {google_ip}")
        except Exception as e:
            print(f"External hostname resolution error: {e}")

        print()


def main():
    """Main function: Execute each demonstration"""
    print("Socket Programming Basic Demo")
    print("=" * 40)

    demo = BasicSocketDemo()

    # 1. Socket creation demo
    demo.create_tcp_socket()
    demo.create_udp_socket()

    # 2. Socket information retrieval
    demo.socket_info_demo()

    # 3. TCP communication demo (server in separate thread)
    print("Starting TCP communication demo...")

    # Start server in separate thread
    server_thread = threading.Thread(target=demo.tcp_server_demo)
    server_thread.daemon = True
    server_thread.start()

    # Wait for server startup
    time.sleep(0.5)

    # Execute client
    demo.tcp_client_demo()

    print("=" * 40)
    print("Demo completed")


if __name__ == "__main__":
    main()