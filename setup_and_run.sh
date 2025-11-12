#!/bin/bash
# Автоматическая настройка и запуск Strix

set -e

echo "🚀 Настройка и запуск Strix..."
echo ""

# Проверка наличия LLM_API_KEY в окружении
if [ -z "$LLM_API_KEY" ]; then
    echo "⚠️  LLM_API_KEY не найден в переменных окружения"
    echo ""
    echo "Добавьте секрет в GitHub Codespaces:"
    echo "1. Откройте: https://github.com/settings/codespaces"
    echo "2. Нажмите 'New secret'"
    echo "3. Добавьте:"
    echo "   Имя: LLM_API_KEY"
    echo "   Значение: ваш API ключ"
    echo "   Repository: Redrock453/strix"
    echo ""
    read -p "Или введите ключ сейчас (Enter для пропуска): " api_key
    
    if [ -n "$api_key" ]; then
        export LLM_API_KEY="$api_key"
        echo "export LLM_API_KEY='$api_key'" >> ~/.bashrc
        echo "✅ Ключ сохранен"
    else
        echo "❌ Невозможно запустить без API ключа"
        exit 1
    fi
fi

# Проверка/установка STRIX_LLM
if [ -z "$STRIX_LLM" ]; then
    export STRIX_LLM="anthropic/claude-3-5-sonnet-20241022"
    echo "export STRIX_LLM='$STRIX_LLM'" >> ~/.bashrc
    echo "📝 Установлена модель: $STRIX_LLM"
fi

# Обновление .env файла
cat > .env << EOF
# ============================================================
# Strix Configuration (Auto-generated)
# ============================================================

LLM_API_KEY=${LLM_API_KEY}
STRIX_LLM=${STRIX_LLM}

STRIX_SANDBOX_MODE=false

# Uncomment for web search:
# PERPLEXITY_API_KEY=your-key-here
EOF

echo "✅ Конфигурация обновлена"
echo ""
echo "📦 Проверка окружения..."

# Проверка Docker
if ! docker ps > /dev/null 2>&1; then
    echo "⚠️  Docker не запущен. Запускаю..."
    sudo service docker start 2>/dev/null || true
fi

echo "✅ Docker работает"
echo ""

# Запуск Strix
echo "🦉 Запуск Strix..."
echo "Цель: ${1:-./strix}"
echo ""

if [ -z "$1" ]; then
    poetry run strix --target ./strix --instruction "Perform comprehensive security assessment of this cybersecurity tool"
else
    poetry run strix "$@"
fi
