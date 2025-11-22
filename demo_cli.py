# -*- coding: utf-8 -*-
# demo_cli.py
# =============================================================================
# Amo Musica Core - Demo w trybie konsolowym (bez Kivy)
# =============================================================================

import os
import sys
from core.amocore import AmoMusicaCore
from core.parser import MusicIntentParser


def print_banner():
    """Wyświetla banner aplikacji."""
    print("\n" + "="*50)
    print("   AMO MUSICA CORE - Wektorowa Dusza")
    print("   Demo w trybie konsolowym")
    print("="*50 + "\n")


def print_status(core):
    """Wyświetla status systemu."""
    print("\n" + "-"*50)
    print(f"M_Force: {core.m_force:.1f}/100 | Emocja: {core.emotion}")
    print(f"Logika: {core.get_axis_value('logika'):.1f} | "
          f"Etyka: {core.get_axis_value('etyka'):.1f} | "
          f"Kreacja: {core.get_axis_value('kreacja'):.1f}")
    
    if core.conversation.user_name:
        print(f"Użytkownik: {core.conversation.user_name}")
    print("-"*50 + "\n")


def run_demo():
    """Uruchamia demo w trybie interaktywnym."""
    
    # Upewnij się, że folder 'data' istnieje
    os.makedirs('data', exist_ok=True)
    
    # Inicjalizacja
    print_banner()
    print("[*] Inicjalizacja Amo Musica Core...")
    
    core = AmoMusicaCore()
    parser = MusicIntentParser(core)
    
    print("[✓] System gotowy!\n")
    print("Wpisz 'pomoc' aby zobaczyć dostępne komendy.")
    print("Wpisz 'wyjdź' lub 'quit' aby zakończyć.\n")
    
    # Główna pętla
    while True:
        try:
            # Pobierz input
            user_input = input(">> ").strip()
            
            if not user_input:
                continue
            
            # Obsługa wyjścia
            if user_input.lower() in ['wyjdź', 'wyjdz', 'quit', 'exit', 'q']:
                print("\n[*] Zapisywanie stanu...")
                core.save()
                print("[✓] Do zobaczenia!\n")
                break
            
            # Obsługa komendy status
            if user_input.lower() in ['s', 'stat']:
                print_status(core)
                continue
            
            # Parsowanie i wykonanie
            intent, params = parser.parse_text(user_input)
            response = parser.execute_intent(intent, params)
            
            # Wyświetlenie odpowiedzi
            print(f"\n{response['msg']}\n")
            
            # Zapisz do historii
            core.conversation.history.append({"role": "user", "content": user_input})
            core.conversation.history.append({"role": "ai", "content": response["msg"]})
            
            # Autosave co 5 komend
            if len(core.conversation.history) % 10 == 0:
                core.save()
                
        except KeyboardInterrupt:
            print("\n\n[!] Przerwano przez użytkownika.")
            print("[*] Zapisywanie stanu...")
            core.save()
            print("[✓] Do zobaczenia!\n")
            break
            
        except Exception as e:
            print(f"\n[BŁĄD] {e}\n")
            import traceback
            traceback.print_exc()


def run_automated_test():
    """Uruchamia zautomatyzowany test."""
    print_banner()
    print("[*] Uruchamianie automatycznego testu...\n")
    
    os.makedirs('data', exist_ok=True)
    core = AmoMusicaCore()
    parser = MusicIntentParser(core)
    
    test_commands = [
        ("!setname TestUser", "Ustawienie imienia"),
        ("status", "Sprawdzenie statusu"),
        ("A4:1 C5:0.5 G4:2", "Parsowanie notacji"),
        ("Generuj kanon", "Kompozycja demo"),
        ("pomoc", "Wyświetlenie pomocy"),
    ]
    
    for cmd, description in test_commands:
        print(f"[TEST] {description}")
        print(f"   >> {cmd}")
        
        intent, params = parser.parse_text(cmd)
        response = parser.execute_intent(intent, params)
        
        print(f"   << {response['msg'][:60]}{'...' if len(response['msg']) > 60 else ''}\n")
    
    print_status(core)
    print("[✓] Test zakończony!\n")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_automated_test()
    else:
        run_demo()
