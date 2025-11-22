12#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# start.py
# =============================================================================
# Amo Musica Core - Quick Start Script
# =============================================================================

import sys
import os

def print_menu():
    """Wyświetla menu startowe."""
    print("\n" + "="*60)
    print("   🎵 AMO MUSICA CORE - Quick Start")
    print("="*60)
    print("\nWybierz tryb uruchomienia:\n")
    print("  [1] GUI Mode (Kivy) - Interfejs graficzny")
    print("  [2] CLI Mode - Tryb konsolowy (interaktywny)")
    print("  [3] Test Mode - Automatyczny test funkcji")
    print("  [4] Unit Tests - Uruchom testy jednostkowe")
    print("  [5] Info - Wyświetl informacje o systemie")
    print("  [0] Wyjście\n")
    print("="*60)


def check_dependencies():
    """Sprawdza czy wszystkie zależności są zainstalowane."""
    missing = []
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import kivy
    except ImportError:
        missing.append("kivy")
    
    if missing:
        print("\n⚠️  BRAKUJĄCE ZALEŻNOŚCI:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nZainstaluj zależności używając:")
        print("   pip install -r requirements.txt\n")
        return False
    
    return True


def show_info():
    """Wyświetla informacje o systemie."""
    from core.amocore import AmoMusicaCore, ETHICAL_CONSTITUTION
    
    print("\n" + "="*60)
    print("   📊 INFORMACJE O SYSTEMIE")
    print("="*60)
    
    print("\n🔹 Wersja: v0.1.0-fixed")
    print("🔹 Python:", sys.version.split()[0])
    print("🔹 Status: Stabilny 🟢")
    
    print("\n⚖️  KONSTYTUCJA ETYCZNA:")
    for principle in ETHICAL_CONSTITUTION.principles:
        print(f"   • {principle}")
    
    print("\n📂 Struktura plików:")
    print("   • core/amocore.py  - Rdzeń systemu")
    print("   • core/parser.py   - Parser intencji")
    print("   • main.py          - Aplikacja Kivy")
    print("   • demo_cli.py      - Demo konsolowe")
    print("   • test_core.py     - Testy jednostkowe")
    
    # Sprawdź czy istnieje plik zapisu
    if os.path.exists("data/amomusica.soul"):
        import json
        with open("data/amomusica.soul", "r") as f:
            data = json.load(f)
        
        print("\n💾 Zapisany stan znaleziony:")
        print(f"   • Użytkownik: {data.get('conversation', {}).get('user_name', 'Brak')}")
        print(f"   • M_Force: {data.get('m_force', 0):.1f}")
        print(f"   • Emocja: {data.get('emotion', 'Brak')}")
    else:
        print("\n💾 Brak zapisanego stanu (zostanie utworzony przy pierwszym uruchomieniu)")
    
    print("\n" + "="*60 + "\n")


def main():
    """Główna funkcja startowa."""
    
    # Sprawdź zależności
    if not check_dependencies():
        sys.exit(1)
    
    # Utwórz katalog data jeśli nie istnieje
    os.makedirs('data', exist_ok=True)
    
    while True:
        print_menu()
        choice = input("Wybierz opcję [0-5]: ").strip()
        
        if choice == "1":
            print("\n🚀 Uruchamianie GUI Mode...\n")
            import main
            main.AmoMusicaApp().run()
            break
            
        elif choice == "2":
            print("\n🚀 Uruchamianie CLI Mode...\n")
            import demo_cli
            demo_cli.run_demo()
            break
            
        elif choice == "3":
            print("\n🚀 Uruchamianie Test Mode...\n")
            import demo_cli
            demo_cli.run_automated_test()
            break
            
        elif choice == "4":
            print("\n🧪 Uruchamianie Unit Tests...\n")
            import test_core
            test_core.run_tests()
            break
            
        elif choice == "5":
            show_info()
            
        elif choice == "0":
            print("\n👋 Do zobaczenia!\n")
            break
            
        else:
            print("\n⚠️  Nieprawidłowy wybór. Spróbuj ponownie.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Przerwano przez użytkownika.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ BŁĄD: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
