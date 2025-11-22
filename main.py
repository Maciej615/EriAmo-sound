# -*- coding: utf-8 -*-
# main.py
# =============================================================================
# Amo Musica Core Starter (Kivy Threading - POPRAWIONA WERSJA)
# =============================================================================

import threading
import time
import os
from queue import Queue, Empty

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

from core.amocore import AmoMusicaCore
from core.parser import MusicIntentParser


class AmoMusicaApp(App):
    
    def build(self):
        # 1. Rdzeń AI
        self.ai_core = AmoMusicaCore()
        self.ai_core.parser = MusicIntentParser(self.ai_core)
        
        # 2. Kolejka odpowiedzi do UI
        self.response_queue = Queue()
        
        # 3. Interfejs Użytkownika
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Status label
        self.status_label = Label(
            text="[Amo Musica Core]\nSystem gotowy. Wpisz !setname TwojeImię", 
            font_size='16sp',
            size_hint_y=0.3
        )
        root.add_widget(self.status_label)
        
        # Historia konwersacji
        self.history_label = Label(
            text="Historia konwersacji pojawi się tutaj...",
            font_size='14sp',
            size_hint_y=0.5,
            halign='left',
            valign='top'
        )
        self.history_label.bind(size=self.history_label.setter('text_size'))
        root.add_widget(self.history_label)
        
        # Input box i przycisk
        input_box = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=5)
        
        self.text_input = TextInput(
            hint_text='Wpisz komendę lub pytanie...',
            multiline=False,
            size_hint_x=0.8
        )
        self.text_input.bind(on_text_validate=self.on_submit)
        
        submit_btn = Button(
            text='Wyślij',
            size_hint_x=0.2
        )
        submit_btn.bind(on_press=self.on_submit)
        
        input_box.add_widget(self.text_input)
        input_box.add_widget(submit_btn)
        root.add_widget(input_box)
        
        # 4. Uruchomienie Core w WĄTKU TLA (POPRAWIONE!)
        self.ai_thread = threading.Thread(target=self.run_ai_loop, daemon=True)
        self.ai_thread.start()
        
        # 5. Aktualizacja UI
        Clock.schedule_interval(self.update_ui, 0.1)
        
        # 6. Symulacja (opcjonalnie - do testów)
        Clock.schedule_once(self.simulate_user_input, 2)
        
        return root
    
    def run_ai_loop(self):
        """Główna pętla przetwarzania AI (działa w tle) - NAPRAWIONA!"""
        print("[AI THREAD] Wątek AI uruchomiony.")
        
        while self.ai_core.running:
            try:
                # Pobierz komendę z kolejki (timeout 0.1s)
                command = self.ai_core.command_queue.get(timeout=0.1)
                
                if command is None:  # Sygnał zatrzymania
                    break
                
                # Przetwórz komendę
                user_input = command.get("input", "")
                if user_input:
                    response = self.process_command(user_input)
                    # Wyślij odpowiedź z powrotem do UI
                    self.response_queue.put(response)
                    
            except Empty:
                # Brak komend - czekaj dalej
                continue
            except Exception as e:
                print(f"[AI THREAD ERROR] {e}")
                self.response_queue.put({"error": str(e)})
        
        print("[AI THREAD] Wątek AI zatrzymany.")
    
    def process_command(self, user_input: str) -> dict:
        """Przetwarza komendę użytkownika (wywoływane w wątku AI)."""
        try:
            # 1. Parsowanie
            intent, params = self.ai_core.parser.parse_text(user_input)
            
            # 2. Wykonanie
            response = self.ai_core.parser.execute_intent(intent, params)
            
            # 3. Zapisanie do historii
            with self.ai_core.lock:
                self.ai_core.conversation.history.append({
                    "role": "user", 
                    "content": user_input
                })
                self.ai_core.conversation.history.append({
                    "role": "ai", 
                    "content": response["msg"]
                })
                self.ai_core.save()
            
            return {"success": True, "response": response["msg"]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def on_submit(self, instance):
        """Obsługa wysłania tekstu przez użytkownika."""
        user_input = self.text_input.text.strip()
        
        if user_input:
            # Wyślij do wątku AI
            self.ai_core.command_queue.put({"input": user_input})
            self.text_input.text = ""  # Wyczyść input
    
    def simulate_user_input(self, dt):
        """Symuluje wejście użytkownika w celu przetestowania Core."""
        test_inputs = [
            "!setname Maciek",
            "status",
            "A4:1 C5:0.5 G4:2",
            "Generuj Kanon"
        ]
        
        for inp in test_inputs:
            self.ai_core.command_queue.put({"input": inp})
            time.sleep(0.5)
    
    def update_ui(self, dt):
        """Aktualizuje UI na podstawie odpowiedzi z AI."""
        
        # 1. Sprawdź odpowiedzi z AI
        try:
            while not self.response_queue.empty():
                response = self.response_queue.get_nowait()
                
                if response.get("error"):
                    print(f"[UI ERROR] {response['error']}")
                    
        except Empty:
            pass
        
        # 2. Aktualizuj status (POPRAWIONE!)
        with self.ai_core.lock:
            try:
                # Użycie AXES_MAP zamiast nieistniejącego AXES
                logika_val = self.ai_core.get_axis_value("logika")
                etyka_val = self.ai_core.get_axis_value("etyka")
                kreacja_val = self.ai_core.get_axis_value("kreacja")
                
                self.status_label.text = (
                    f"═══ AMO MUSICA CORE ═══\n"
                    f"M_Force: {self.ai_core.m_force:.1f} | Emocja: {self.ai_core.emotion}\n"
                    f"Logika: {logika_val:.1f} | Etyka: {etyka_val:.1f} | Kreacja: {kreacja_val:.1f}"
                )
                
                # 3. Aktualizuj historię
                if self.ai_core.conversation.history:
                    history_text = ""
                    # Pokaż ostatnie 6 wiadomości
                    recent = list(self.ai_core.conversation.history)[-6:]
                    
                    for msg in recent:
                        role = "TY" if msg["role"] == "user" else "AMO"
                        history_text += f"[{role}] {msg['content']}\n\n"
                    
                    self.history_label.text = history_text.strip()
                    
            except Exception as e:
                print(f"[UI UPDATE ERROR] {e}")
    
    def on_stop(self):
        """Wywoływane przy zamykaniu aplikacji."""
        print("[APP] Zamykanie aplikacji...")
        self.ai_core.stop()
        self.ai_core.command_queue.put(None)  # Sygnał zatrzymania
        self.ai_thread.join(timeout=2)
        return True


if __name__ == '__main__':
    # Upewnij się, że folder 'data' istnieje
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print("═══════════════════════════════════════")
    print("   AMO MUSICA CORE - Wektorowa Dusza")
    print("═══════════════════════════════════════")
    
    AmoMusicaApp().run()

# Koniec pliku main.py
