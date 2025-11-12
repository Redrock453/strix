#!/bin/bash
# Туннель для доступа к Strix в dev-контейнере
# Использование: ./tunnel_setup.sh [local|remote]

set -e

CONTAINER_IP="10.0.15.231"
STRIX_PORT="8000"  # Порт для Strix API (если запустим)
SSH_PORT="2222"    # SSH порт контейнера

echo "🔧 Настройка туннеля для доступа к Strix"
echo "=========================================="
echo ""

# Проверяем режим работы
MODE="${1:-help}"

case "$MODE" in
    "local")
        echo "📍 Режим: Local Port Forwarding"
        echo ""
        echo "Использование с вашей локальной машины:"
        echo ""
        echo "ssh -L 8000:localhost:8000 -p $SSH_PORT user@$CONTAINER_IP"
        echo ""
        echo "После подключения, Strix будет доступен на: http://localhost:8000"
        ;;
    
    "remote")
        echo "📍 Режим: Remote Port Forwarding"
        echo ""
        echo "Пробросить локальный порт на удалённую машину:"
        echo ""
        echo "ssh -R 8000:localhost:8000 -p $SSH_PORT user@$CONTAINER_IP"
        ;;
    
    "expose")
        echo "📍 Режим: Expose via ngrok/cloudflare tunnel"
        echo ""
        
        # Проверяем наличие инструментов
        if command -v gh &> /dev/null; then
            echo "✅ GitHub CLI доступен - используйте GitHub Codespaces forwarding"
            echo ""
            echo "Команда для проброса порта через Codespaces:"
            echo "gh codespace ports forward $STRIX_PORT:$STRIX_PORT"
        fi
        
        if command -v docker &> /dev/null; then
            echo ""
            echo "✅ Docker доступен - можно использовать ngrok в контейнере:"
            echo ""
            echo "docker run -it --rm --net=host ngrok/ngrok:latest http $STRIX_PORT"
        fi
        ;;
    
    "test")
        echo "🧪 Тестовый сервер на порту $STRIX_PORT"
        echo ""
        
        # Запускаем простой HTTP сервер для теста
        echo "Запуск тестового Python HTTP сервера..."
        echo "Доступ: http://$CONTAINER_IP:$STRIX_PORT"
        echo ""
        echo "Нажмите Ctrl+C для остановки"
        echo ""
        
        cd /workspaces/strix
        python3 -m http.server $STRIX_PORT --bind 0.0.0.0
        ;;
    
    "strix")
        echo "🦉 Запуск Strix с проброшенным портом"
        echo ""
        echo "⚠️  Требуется настроенный .env файл"
        echo ""
        
        if [ ! -f "/workspaces/strix/.env" ]; then
            echo "❌ Файл .env не найден!"
            echo "Создайте .env с настройками API перед запуском"
            exit 1
        fi
        
        echo "Strix будет доступен через tool server на порту (настраивается в docker_runtime.py)"
        echo ""
        echo "Для ручного запуска tool server:"
        echo "python -m strix.runtime.tool_server --host 0.0.0.0 --port $STRIX_PORT"
        ;;
    
    "info")
        echo "📊 Информация о сети"
        echo ""
        echo "Внутренний IP: $CONTAINER_IP"
        echo "SSH порт: $SSH_PORT"
        echo "Предполагаемый Strix порт: $STRIX_PORT"
        echo ""
        echo "Открытые порты:"
        netstat -tlnp 2>/dev/null | grep LISTEN | awk '{print "  "$4}' | sort -u
        echo ""
        echo "Сетевые интерфейсы:"
        ip addr show | grep -E "^[0-9]+:|inet " | sed 's/^/  /'
        ;;
    
    *)
        echo "Доступные команды:"
        echo ""
        echo "  ./tunnel_setup.sh local    - инструкции для local port forwarding"
        echo "  ./tunnel_setup.sh remote   - инструкции для remote port forwarding"
        echo "  ./tunnel_setup.sh expose   - варианты публичного доступа (ngrok/cloudflare)"
        echo "  ./tunnel_setup.sh test     - запустить тестовый HTTP сервер"
        echo "  ./tunnel_setup.sh strix    - запустить Strix с доступом по сети"
        echo "  ./tunnel_setup.sh info     - показать сетевую информацию"
        echo ""
        echo "Быстрый старт:"
        echo "  1. ./tunnel_setup.sh test      # Запустить тестовый сервер"
        echo "  2. curl http://$CONTAINER_IP:$STRIX_PORT  # Проверить доступ"
        echo ""
        echo "Для GitHub Codespaces:"
        echo "  gh codespace ports forward $STRIX_PORT:$STRIX_PORT"
        ;;
esac

echo ""
