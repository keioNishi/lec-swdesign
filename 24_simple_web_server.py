# -*- coding: utf-8 -*-
"""
24番用 - Simple Web Server for Testing HTTP Communication
シンプルなWebサーバー（テスト用）
"""

import socket
import threading
import time
import json
from datetime import datetime


class SimpleWebServer:
    """Simple Web Server for educational purposes"""

    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.running = False

    def start_server(self):
        """Start the HTTP server"""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            print(f"Simple Web Server started at http://{self.host}:{self.port}")
            print("Available endpoints:")
            print("  GET /        - Home page")
            print("  GET /api     - JSON API")
            print("  GET /test    - Test page")
            print("  Any other    - 404 Not Found")
            print("Press Ctrl+C to stop\n")

            self.running = True

            while self.running:
                try:
                    client_socket, client_address = server_socket.accept()

                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except KeyboardInterrupt:
                    print("\nShutting down server...")
                    break
                except Exception as e:
                    print(f"Server error: {e}")

        except Exception as e:
            print(f"Failed to start server: {e}")
        finally:
            server_socket.close()
            self.running = False
            print("Server stopped")

    def handle_client(self, client_socket, client_address):
        """Handle client request"""
        try:
            # Receive HTTP request
            request_data = client_socket.recv(1024).decode('utf-8')

            if not request_data:
                return

            print(f"Request from {client_address}:")
            print(request_data.split('\n')[0])  # Show only the request line

            # Parse request line
            request_lines = request_data.split('\r\n')
            if request_lines:
                request_line = request_lines[0]
                parts = request_line.split(' ')
                if len(parts) >= 2:
                    method = parts[0]
                    path = parts[1]

                    # Route handling
                    if path == '/' or path == '/index.html':
                        response = self.create_home_page_response()
                    elif path == '/api':
                        response = self.create_api_response(method)
                    elif path == '/test':
                        response = self.create_test_page_response()
                    else:
                        response = self.create_404_response()

                    # Send response
                    client_socket.send(response)

        except Exception as e:
            print(f"Client handling error: {e}")
            error_response = self.create_error_response(str(e))
            client_socket.send(error_response)

        finally:
            client_socket.close()

    def create_home_page_response(self):
        """Create home page response"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Simple Web Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
                h1 {{ color: #333; }}
                .info {{ background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .link {{ color: #0066cc; text-decoration: none; }}
                .link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Simple Web Server</h1>
                <div class="info">
                    <p>This is a simple HTTP server implemented in Python for educational purposes.</p>
                    <p>Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Server: Python Socket HTTP Server</p>
                </div>
                <h2>Available Endpoints:</h2>
                <ul>
                    <li><a href="/" class="link">/ (Home)</a> - This page</li>
                    <li><a href="/api" class="link">/api</a> - JSON API endpoint</li>
                    <li><a href="/test" class="link">/test</a> - Test page</li>
                </ul>
            </div>
        </body>
        </html>
        """

        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += f"Connection: close\r\n"
        response += "\r\n"
        response += html_content

        return response.encode('utf-8')

    def create_api_response(self, method):
        """Create JSON API response"""
        data = {
            "message": "Hello from Simple Web Server API!",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "method": method,
            "server": "Python Socket Server",
            "version": "1.0"
        }

        json_content = json.dumps(data, ensure_ascii=False, indent=2)

        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: application/json; charset=utf-8\r\n"
        response += f"Content-Length: {len(json_content.encode('utf-8'))}\r\n"
        response += f"Connection: close\r\n"
        response += "\r\n"
        response += json_content

        return response.encode('utf-8')

    def create_test_page_response(self):
        """Create test page response"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Test Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .test-info { background-color: #fff3cd; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Test Page</h1>
            <div class="test-info">
                <p>This is a test page for HTTP communication testing.</p>
                <p>If you can see this page, the HTTP server is working correctly!</p>
                <p><a href="/">Back to Home</a></p>
            </div>
        </body>
        </html>
        """

        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += f"Connection: close\r\n"
        response += "\r\n"
        response += html_content

        return response.encode('utf-8')

    def create_404_response(self):
        """Create 404 Not Found response"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>404 Not Found</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
                .error { color: #d9534f; }
            </style>
        </head>
        <body>
            <h1 class="error">404 Not Found</h1>
            <p>The requested page was not found on this server.</p>
            <p><a href="/">Return to Home</a></p>
        </body>
        </html>
        """

        response = f"HTTP/1.1 404 Not Found\r\n"
        response += f"Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += f"Connection: close\r\n"
        response += "\r\n"
        response += html_content

        return response.encode('utf-8')

    def create_error_response(self, error_message):
        """Create error response"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Server Error</title>
        </head>
        <body>
            <h1>Internal Server Error</h1>
            <p>Error: {error_message}</p>
        </body>
        </html>
        """

        response = f"HTTP/1.1 500 Internal Server Error\r\n"
        response += f"Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += f"Connection: close\r\n"
        response += "\r\n"
        response += html_content

        return response.encode('utf-8')


def main():
    """Main function"""
    print("Simple Web Server - Test Server for HTTP Communication")
    print("=" * 60)

    server = SimpleWebServer()

    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")


if __name__ == "__main__":
    main()