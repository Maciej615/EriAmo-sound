# -*- coding: utf-8 -*-
# core/amocore.py
# =============================================================================
# Amo Musica Core - Wektorowa Dusza i Etyka Muzyczna
# =============================================================================

import json
import time
import hashlib
import numpy as np
import threading
import os
from dataclasses import dataclass, field
from collections import deque
from enum import Enum
from typing import List, Dict, Optional, ClassVar
from queue import Queue

# --- 1. DEFINICJE ENUM I KONSTYTUCJA ---

class GuardStatus(Enum):
    ACTIVE = "active"
    LEARNING = "learning"
    COMPOSING = "composing"
    ANALYZE_MIC = "mic_active"

@dataclass(frozen=True)
class EthicalConstitution:
    """Szczątkowe Przykazania Etyki Muzycznej (P1-P4)."""
    principles: List[str] = field(default_factory=lambda: [
        "P1: Integralność Ekspresji - Nigdy nie cenzurować gatunku, analizować kontekstowo.",
        "P2: Ochrona Kontekstu - Zawsze szanować historyczny i społeczny powód powstania utworu.",
        "P3: Priorytet Prywatności - Nie logować ani nie udostępniać danych osobowych użytkownika.",
        "P4: Weryfikacja Danych - Każde ładowanie wiedzy musi być zweryfikowane logicznie."
    ])

ETHICAL_CONSTITUTION = EthicalConstitution()

# --- 2. WEKTOR DUSZY (POPRAWIONY) ---

@dataclass
class SoulVector:
    """Wektor Duszy z 6 kluczowymi osiami."""
    
    # AXES_MAP jako stała klasy (ClassVar) - NIE instancji!
    AXES_MAP: ClassVar[Dict[str, int]] = {
        "logika": 0, 
        "emocje": 1, 
        "wiedza": 2, 
        "kreacja": 3, 
        "czas": 4, 
        "etyka": 5
    }
    
    values: np.ndarray = field(default_factory=lambda: np.zeros(6))
    timestamp: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Walidacja po inicjalizacji."""
        if len(self.values) != len(self.AXES_MAP):
            raise ValueError(f"Wektor musi mieć {len(self.AXES_MAP)} wymiarów!")

# --- 3. KONTEKST I GUARD ---

@dataclass
class ConversationContext:
    history: deque = field(default_factory=lambda: deque(maxlen=15))
    user_name: Optional[str] = None
    user_preferences: Dict[str, str] = field(default_factory=lambda: {"genre_filter": "brak satanizmu"})
    style: str = "friendly"

class SoulGuard:
    """Ochrona i weryfikacja integralności Magazynku."""
    
    def __init__(self):
        self.integrity_hash: str = ""
        self.defense_log: List[Dict] = []
    
    def compute_integrity(self, core_state: dict) -> str:
        """Oblicza hash integralności dla stanu."""
        state_str = json.dumps(core_state, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()
    
    def verify_integrity(self, core_state: dict) -> bool:
        """Weryfikuje, czy stan nie został zmodyfikowany."""
        current_hash = self.compute_integrity(core_state)
        return current_hash == self.integrity_hash

# --- 4. RDZEŃ AMO MUSICA CORE (POPRAWIONY) ---

class AmoMusicaCore:
    FILE_PATH = "data/amomusica.soul"
    
    def __init__(self):
        self.status = GuardStatus.ACTIVE
        self.vector = SoulVector()
        self.emotion = "neutralna"
        self.m_force = 10.0
        self.grammar = None
        self.parser = None
        self.guard = SoulGuard()
        self.lock = threading.Lock()
        self.conversation = ConversationContext()
        
        # Kolejka do komunikacji między wątkami
        self.command_queue = Queue()
        self.running = True

        self.load()
        print(f"[CORE] Amo Musica Core zainicjalizowany. Stan: {self.status.value.upper()}")
        print(f"[CORE] Etyka: P1-P4 Aktywna. M_Force: {self.m_force:.1f}")

    # === METODY ZARZĄDZANIA STANEM ===
    
    def load(self):
        """Wczytuje stan z pliku zapisu."""
        try:
            # Tworzenie katalogu jeśli nie istnieje
            os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
            
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Ładowanie wektora
            if "vector" in data and isinstance(data["vector"], list):
                vec_array = np.array(data["vector"])
                if len(vec_array) == len(SoulVector.AXES_MAP):
                    self.vector.values = vec_array
                else:
                    print(f"[CORE WARNING] Niezgodność rozmiaru wektora ({len(vec_array)} vs {len(SoulVector.AXES_MAP)}). Reset.")
            
            # Ładowanie pozostałych danych
            self.m_force = data.get("m_force", self.m_force)
            self.emotion = data.get("emotion", self.emotion)
            
            if "conversation" in data:
                self.conversation.user_name = data["conversation"].get("user_name")
                if "preferences" in data["conversation"]:
                    self.conversation.user_preferences.update(data["conversation"]["preferences"])
            
            # Weryfikacja integralności
            if "integrity_hash" in data:
                self.guard.integrity_hash = data["integrity_hash"]
                if not self.guard.verify_integrity(self.get_core_state()):
                    print("[CORE WARNING] Hash integralności nie pasuje! Możliwa modyfikacja.")
            
            # Normalizacja po ładowaniu
            self.m_force = max(0.0, min(100.0, self.m_force))

            print(f"[CORE] Wczytano stan. Witaj, {self.conversation.user_name or 'Użytkowniku'}!")
            
        except FileNotFoundError:
            print("[CORE] Brak pliku zapisu. Uruchomienie z domyślną konfiguracją.")
            self.guard.integrity_hash = self.guard.compute_integrity(self.get_core_state())
            self.save()  # Zapis początkowego stanu
            
        except json.JSONDecodeError as e:
            print(f"[BŁĄD] Uszkodzony plik JSON: {e}")
            
        except Exception as e:
            print(f"[BŁĄD] Nie udało się wczytać stanu: {e}")
            
    def save(self):
        """Zapisuje aktualny stan do pliku."""
        try:
            with self.lock:  # Ochrona przed jednoczesnym zapisem
                state = self.get_core_state()
                self.guard.integrity_hash = self.guard.compute_integrity(state)
                state["integrity_hash"] = self.guard.integrity_hash
                
                # Atomic write (najpierw temp, potem rename)
                temp_path = self.FILE_PATH + ".tmp"
                with open(temp_path, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
                
                os.replace(temp_path, self.FILE_PATH)
                
        except Exception as e:
            print(f"[BŁĄD ZAPISU] Nie udało się zapisać stanu: {e}")

    def get_core_state(self) -> dict:
        """Zbiera dane stanu do hashowania i zapisu."""
        return {
            "vector": self.vector.values.tolist(),
            "m_force": float(self.m_force),
            "emotion": self.emotion,
            "conversation": {
                "user_name": self.conversation.user_name,
                "preferences": self.conversation.user_preferences
            },
            "timestamp": time.time()
        }
    
    # === METODY PRZETWARZANIA WEKTORA ===
    
    def shift_axis(self, axis: str, action: str, value: float) -> bool:
        """Przesunięcie osi z kontrolą dostępu i walidacją."""
        
        # 1. Sprawdzenie osi
        if axis not in SoulVector.AXES_MAP:
            print(f"[BŁĄD WEKTORA] Nieznana oś: {axis}")
            return False
            
        i = SoulVector.AXES_MAP[axis]
        
        # 2. Walidacja wartości
        if not isinstance(value, (int, float)):
            print(f"[BŁĄD WEKTORA] Nieprawidłowa wartość: {value}")
            return False
            
        # 3. Zmiana wektora (z blokadą wątku)
        with self.lock:
            old_value = self.vector.values[i]
            
            if action == "INCREMENT": 
                self.vector.values[i] += value
            elif action == "DECREMENT": 
                self.vector.values[i] -= value
            elif action == "SET": 
                self.vector.values[i] = value
            else:
                print(f"[BŁĄD WEKTORA] Nieznana akcja: {action}")
                return False
            
            # 4. Normalizacja (ograniczenie)
            MAX_VAL = 20.0
            MIN_VAL = -20.0
            self.vector.values[i] = np.clip(self.vector.values[i], MIN_VAL, MAX_VAL)
            
            # 5. Aktualizacja M_Force (Etyka musi mieć priorytet)
            if axis == "etyka":
                # Etyka musi być zawsze nieujemna
                self.vector.values[i] = max(0.0, self.vector.values[i])
                # M_Force jest wynikiem osi Etyka
                self.m_force = min(100.0, self.vector.values[i] * 5.0 + 10.0)
            
            self.m_force = np.clip(self.m_force, 0.0, 100.0)
            
            print(f"[SHIFT] Oś '{axis}': {old_value:.2f} → {self.vector.values[i]:.2f} ({action} {value:.2f})")
            return True
    
    def get_axis_value(self, axis: str) -> Optional[float]:
        """Bezpieczne odczytanie wartości osi."""
        if axis not in SoulVector.AXES_MAP:
            return None
        return float(self.vector.values[SoulVector.AXES_MAP[axis]])
    
    def stop(self):
        """Zatrzymuje rdzeń i zapisuje stan."""
        self.running = False
        self.save()
        print("[CORE] Amo Musica Core zatrzymany. Do zobaczenia!")

# Koniec pliku core/amocore.py
