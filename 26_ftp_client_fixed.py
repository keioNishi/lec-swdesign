# -*- coding: utf-8 -*-
"""
FTP Client Demo - Fixed Version
FTP (File Transfer Protocol) の基礎とクライアント実装（修正版）
"""

import socket
import os
import threading
import time
from datetime import datetime


class SimpleFTPClient:
    """Simple FTP Client (educational implementation) - Fixed"""

    def __init__(self):
        self.control_socket = None
        self.connected = False
        self.current_directory = "/"
        self.passive_mode = True

    def connect(self, host, port=21):
        """Connect to FTP server"""
        print(f"=== Connecting to FTP Server: {host}:{port} ===")

        try:
            # Establish control connection
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.settimeout(30)
            self.control_socket.connect((host, port))

            # Receive response from server
            response = self.receive_response()
            print(f"Server response: {response}")

            if response.startswith('220'):
                self.connected = True
                print("[OK] Connection successful")
                return True
            else:
                print("[ERROR] Connection failed")
                return False

        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
            return False

    def send_command(self, command):
        """Send FTP command"""
        if not self.connected or not self.control_socket:
            print("[ERROR] Not connected to server")
            return None

        try:
            # Send command (terminated with CRLF)
            full_command = command + "\r\n"
            self.control_socket.send(full_command.encode('ascii'))
            print(f"Sent command: {command}")

            # Receive response
            response = self.receive_response()
            print(f"Server response: {response}")

            return response

        except Exception as e:
            print(f"[ERROR] Command send error: {e}")
            return None

    def receive_response(self):
        """Receive response from server"""
        try:
            response = ""
            while True:
                data = self.control_socket.recv(1024).decode('ascii', errors='ignore')
                response += data

                # Handle multi-line responses
                lines = response.split('\r\n')
                if len(lines) >= 2 and lines[-2]:
                    # If the last line is not empty, we have a complete response
                    break

            return response.strip()

        except Exception as e:
            print(f"[ERROR] Response receive error: {e}")
            return ""

    def login(self, username="anonymous", password="anonymous@example.com"):
        """Login to FTP server"""
        print(f"\n=== Login: {username} ===")

        # Send USER command
        response = self.send_command(f"USER {username}")
        if not response or not response.startswith('331'):
            print("[ERROR] Username not accepted")
            return False

        # Send PASS command
        response = self.send_command(f"PASS {password}")
        if response and response.startswith('230'):
            print("[OK] Login successful")
            return True
        else:
            print("[ERROR] Login failed")
            return False

    def pwd(self):
        """Get current directory (PWD command)"""
        print("\n=== Get Current Directory ===")
        response = self.send_command("PWD")

        if response and response.startswith('257'):
            # Extract directory path from response
            # Example: 257 "/home/user" is current directory
            start = response.find('"')
            end = response.find('"', start + 1)
            if start != -1 and end != -1:
                directory = response[start + 1:end]
                self.current_directory = directory
                print(f"Current directory: {directory}")
                return directory

        return None

    def quit(self):
        """End FTP connection"""
        print("\n=== End FTP Connection ===")

        if self.connected and self.control_socket:
            # Send QUIT command
            response = self.send_command("QUIT")
            print(f"Quit response: {response}")

            # Close connection
            self.control_socket.close()
            self.connected = False
            print("[OK] Connection closed")

        else:
            print("Not connected")

    def simulate_file_operations(self):
        """Simulate file operations"""
        print("\n=== File Operations Simulation ===")

        # Simulate directory listing
        print("1. Directory Listing Simulation:")
        print("   drwxr-xr-x   2 user  group    4096 Mar 15 10:00 documents")
        print("   drwxr-xr-x   2 user  group    4096 Mar 15 09:30 downloads")
        print("   -rw-r--r--   1 user  group     123 Mar 15 11:00 readme.txt")
        print("   -rw-r--r--   1 user  group    5678 Mar 15 10:30 data.csv")

        # Simulate file download
        print("\n2. File Download Simulation:")
        filename = "test_file.txt"
        dummy_content = f"This is dummy content for {filename}\n"
        dummy_content += f"Downloaded at: {datetime.now()}\n"
        dummy_content += "This demonstrates FTP file transfer.\n"

        print(f"   Downloading: {filename}")
        print(f"   File size: {len(dummy_content)} bytes")
        print(f"   Content preview: {dummy_content[:50]}...")
        print("   [OK] Download simulation completed")

        # Simulate file upload
        print("\n3. File Upload Simulation:")
        upload_file = "upload_test.txt"
        upload_content = "This would be uploaded to the FTP server.\n"
        print(f"   Uploading: {upload_file}")
        print(f"   Content: {upload_content.strip()}")
        print("   [OK] Upload simulation completed")


class SimpleFTPServer:
    """Simple FTP Server (demo purpose) - Fixed"""

    def __init__(self, host='localhost', port=2121):
        self.host = host
        self.port = port
        self.running = False
        self.current_dir = "/virtual_root"

    def start_server(self):
        """Start FTP server (simple implementation)"""
        print(f"=== Starting FTP Server: {self.host}:{self.port} ===")

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)

            print(f"FTP Server listening on {self.host}:{self.port}...")
            self.running = True

            # Simple FTP server implementation (demo purpose)
            server_socket.settimeout(5)

            try:
                client_socket, client_address = server_socket.accept()
                print(f"Client {client_address} connected")

                # Send welcome message
                welcome_msg = "220 Simple FTP Server Ready\r\n"
                client_socket.send(welcome_msg.encode('ascii'))

                # Simple command processing (demo purpose)
                while self.running:
                    try:
                        client_socket.settimeout(2)
                        data = client_socket.recv(1024).decode('ascii', errors='ignore')
                        if not data:
                            break

                        command = data.strip()
                        print(f"Received command: {command}")

                        # Simple command responses
                        if command.startswith('USER'):
                            response = "331 Password required\r\n"
                        elif command.startswith('PASS'):
                            response = "230 Login successful\r\n"
                        elif command.startswith('PWD'):
                            response = f'257 "{self.current_dir}" is current directory\r\n'
                        elif command.startswith('QUIT'):
                            response = "221 Goodbye\r\n"
                            client_socket.send(response.encode('ascii'))
                            break
                        else:
                            response = "502 Command not implemented\r\n"

                        client_socket.send(response.encode('ascii'))

                    except socket.timeout:
                        continue

                client_socket.close()

            except socket.timeout:
                print("Timeout: No client connection received")

        except Exception as e:
            print(f"FTP Server error: {e}")
        finally:
            server_socket.close()
            self.running = False
            print("FTP Server stopped")


def demo_ftp_client():
    """FTP Client demonstration"""
    print("FTP (File Transfer Protocol) Basic Demo - Fixed Version")
    print("=" * 60)

    # Start FTP server in separate thread
    server = SimpleFTPServer()
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

    # Wait for server startup
    time.sleep(1)

    # Test with FTP client
    client = SimpleFTPClient()

    # 1. Connect to server
    if client.connect('localhost', 2121):
        # 2. Login
        if client.login('testuser', 'testpass'):
            # 3. Get current directory
            client.pwd()

            # 4. Simulate file operations
            client.simulate_file_operations()

        # 5. End connection
        client.quit()

    # Stop server
    server.running = False
    time.sleep(1)

    print("\n" + "=" * 60)
    print("FTP Demo completed")
    print("\nNotes:")
    print("- This demo is a simplified implementation for educational purposes")
    print("- Real FTP server communication requires more detailed implementation")
    print("- SFTP (SSH File Transfer Protocol) is recommended for security reasons")


def create_ftp_test_files():
    """Create test files for FTP demonstration"""
    print("\n=== Creating FTP Test Files ===")

    test_files = [
        {
            'name': '26_ftp_test_download.txt',
            'content': '''FTP Test Download File
======================

This file demonstrates FTP download functionality.

File Information:
- Created for FTP demo
- Contains sample text data
- Can be used for testing file transfer

Content:
Line 1: Sample data
Line 2: More sample data
Line 3: End of file

Created: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'name': '26_ftp_test_upload.txt',
            'content': '''FTP Test Upload File
====================

This file simulates content that would be uploaded to an FTP server.

Upload Information:
- Source: Local file system
- Destination: FTP server
- Purpose: Educational demonstration

Data:
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

Created: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]

    created_files = []

    for file_info in test_files:
        try:
            with open(file_info['name'], 'w', encoding='utf-8') as f:
                f.write(file_info['content'])
            print(f"[OK] Created: {file_info['name']}")
            created_files.append(file_info['name'])
        except Exception as e:
            print(f"[ERROR] Failed to create {file_info['name']}: {e}")

    return created_files


def cleanup_test_files(file_list):
    """Clean up test files"""
    print("\n=== Cleaning up test files ===")

    for filename in file_list:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"[OK] Removed: {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to remove {filename}: {e}")


def main():
    """Main function"""
    # Create test files
    test_files = create_ftp_test_files()

    # Run FTP demo
    demo_ftp_client()

    # Clean up test files
    cleanup_test_files(test_files)


if __name__ == "__main__":
    main()