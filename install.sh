#!/bin/bash
# install.sh - Instalator Amo Musica Core

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     AMO MUSICA CORE - Instalator Automatyczny             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo

# Sprawdź Python
echo "[1/5] Sprawdzanie wersji Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nie jest zainstalowany!"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION znaleziony"

# Sprawdź pip
echo
echo "[2/5] Sprawdzanie pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip nie jest zainstalowany!"
    exit 1
fi
echo "✓ pip znaleziony"

# Tworzenie katalogu data
echo
echo "[3/5] Tworzenie katalogu danych..."
mkdir -p data
echo "✓ Katalog data/ utworzony"

# Instalacja zależności
echo
echo "[4/5] Instalacja zależności..."
pip3 install -r requirements.txt
echo "✓ Zależności zainstalowane"

# Test instalacji
echo
echo "[5/5] Uruchamianie testów..."
python3 test_core.py
TEST_STATUS=$?

echo
echo "════════════════════════════════════════════════════════════"

if [ $TEST_STATUS -eq 0 ]; then
    echo "✅ INSTALACJA ZAKOŃCZONA SUKCESEM!"
    echo
    echo "Aby uruchomić aplikację, wpisz:"
    echo "  python3 start.py      # Menu startowe"
    echo "  python3 main.py       # GUI (Kivy)"
    echo "  python3 demo_cli.py   # Konsola"
else
    echo "⚠️  Testy nie przeszły. Sprawdź błędy powyżej."
    exit 1
fi

echo "════════════════════════════════════════════════════════════"
