#!/usr/bin/env python3
"""
Простой тестовый веб-сервер для проверки туннеля
Отображает информацию о подключении и сетевых настройках
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket
import sys
from datetime import datetime


class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET запросов."""
        
        # Информация о подключении
        client_ip = self.client_address[0]
        client_port = self.client_address[1]
        
        # Информация о сервере
        hostname = socket.gethostname()
        server_ip = socket.gethostbyname(hostname)
        
        if self.path == "/":
            # HTML страница с информацией
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🦉 Strix Tunnel Test Server</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .info-box {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
        }}
        .label {{
            font-weight: bold;
            color: #ffd700;
        }}
        .success {{
            text-align: center;
            font-size: 1.2em;
            margin: 20px 0;
            color: #90EE90;
        }}
        code {{
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🦉 Strix Tunnel Test Server</h1>
        
        <div class="success">
            ✅ Туннель работает успешно!
        </div>
        
        <div class="info-box">
            <div class="label">🌐 Информация о подключении:</div>
            <p>Ваш IP: <code>{client_ip}</code></p>
            <p>Ваш порт: <code>{client_port}</code></p>
            <p>Время: <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code></p>
        </div>
        
        <div class="info-box">
            <div class="label">🖥️ Информация о сервере:</div>
            <p>Hostname: <code>{hostname}</code></p>
            <p>Server IP: <code>{server_ip}</code></p>
            <p>Путь запроса: <code>{self.path}</code></p>
        </div>
        
        <div class="info-box">
            <div class="label">📡 Доступные эндпоинты:</div>
            <p>• <a href="/" style="color: #90EE90;">GET /</a> - эта страница</p>
            <p>• <a href="/api/status" style="color: #90EE90;">GET /api/status</a> - JSON статус</p>
            <p>• <a href="/api/health" style="color: #90EE90;">GET /api/health</a> - health check</p>
        </div>
        
        <div class="info-box">
            <div class="label">🔧 Следующие шаги:</div>
            <p>1. Если вы видите эту страницу - туннель настроен правильно</p>
            <p>2. Можете запустить Strix tool server на этом порту</p>
            <p>3. Или использовать порт для других сервисов</p>
        </div>
    </div>
</body>
</html>
            """
            
            self.wfile.write(html.encode())
            
        elif self.path == "/api/status" or self.path == "/api/health":
            # JSON API
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            data = {
                "status": "ok",
                "service": "Strix Tunnel Test Server",
                "timestamp": datetime.now().isoformat(),
                "client": {
                    "ip": client_ip,
                    "port": client_port
                },
                "server": {
                    "hostname": hostname,
                    "ip": server_ip
                }
            }
            
            self.wfile.write(json.dumps(data, indent=2).encode())
        
        else:
            # 404
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")
    
    def log_message(self, format, *args):
        """Логирование запросов."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.client_address[0]} - {format % args}")


def run_server(host="0.0.0.0", port=8000):
    """Запуск тестового сервера."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, TestHandler)
    
    print("=" * 60)
    print("🦉 Strix Tunnel Test Server")
    print("=" * 60)
    print(f"🌐 Server running on: http://{host}:{port}")
    print(f"📍 Local access: http://localhost:{port}")
    
    # Пытаемся получить внешний IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"🔗 Network access: http://{local_ip}:{port}")
    except Exception:
        pass
    
    print("")
    print("📡 Доступные эндпоинты:")
    print(f"   • GET /                - HTML страница с информацией")
    print(f"   • GET /api/status      - JSON статус")
    print(f"   • GET /api/health      - Health check")
    print("")
    print("⚙️  Настройка туннеля:")
    print(f"   GitHub Codespaces: gh codespace ports forward {port}:{port}")
    print(f"   SSH Local Forward: ssh -L {port}:localhost:{port} user@host")
    print(f"   Ngrok: docker run -it --rm --net=host ngrok/ngrok:latest http {port}")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print("")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        httpd.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(port=port)
