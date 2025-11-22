# -*- coding: utf-8 -*-
# core/parser.py
# =============================================================================
# Music Intent Parser - Tłumaczenie NLP na funkcje Core
# =============================================================================

import re
import os
from typing import TYPE_CHECKING, Tuple, Optional, Dict, Any

# Próba importu modułu audio (Soft Dependency)
try:
    from .transcriber import AudioTranscriber
    HAS_AUDIO_MODULE = True
except ImportError:
    HAS_AUDIO_MODULE = False

if TYPE_CHECKING:
    from .amocore import AmoMusicaCore

class MusicIntentParser:
    """Parser intencji użytkownika dla Amo Musica Core."""
    
    def __init__(self, core: 'AmoMusicaCore'):
        self.core = core
        # Inicjalizacja modułu audio jeśli dostępny
        if HAS_AUDIO_MODULE:
            self.transcriber = AudioTranscriber()
        else:
            self.transcriber = None
            print("[PARSER] Moduł audio nieaktywny (brak bibliotek).")

    def parse_text(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Rozpoznaje Intencję z tekstu użytkownika."""
        if not text:
            return "INTENT_EMPTY", {}
            
        text_lower = text.lower().strip()
        
        # --- INTENCJA: ZARZĄDZANIE ---
        if text_lower.startswith("!setname"):
            name = text[len("!setname"):].strip()
            if name:
                return "INTENT_SETNAME", {"name": name}
            else:
                return "INTENT_ERROR", {"msg": "Podaj imię po !setname"}
        
        # --- INTENCJA: ANALIZA PLIKÓW (NOWE) ---
        if text_lower.startswith("!analizuj "):
            # Usuwamy cudzysłowy jeśli user wkleił ścieżkę "jako ścieżkę"
            filepath = text[len("!analizuj "):].strip().replace('"', '')
            return "INTENT_ANALYZE_FILE", {"filepath": filepath}

        # --- INTENCJA: ANALIZA I KREACJA ---
        # 1. Parsowanie Notacji (AEC System)
        if re.search(r"[a-g]#?\d:\d+\.?\d*", text_lower):
            return "INTENT_PARSE_NOTATION", {"notation": text}
            
        # 2. Kompozytor Demo
        if "kanon" in text_lower or "generuj kanon" in text_lower:
            return "INTENT_COMPOSE_DEMO", {"style": "kanon"}
            
        if "menuet" in text_lower or "generuj menuet" in text_lower:
            return "INTENT_COMPOSE_DEMO", {"style": "menuet"}
        
        # 3. Analiza Mikrofonu (Live)
        if "analizuj mikrofon" in text_lower or "analizuj bending" in text_lower:
            return "INTENT_ANALYZE_MIC", {}
        
        # 4. Status systemu
        if any(phrase in text_lower for phrase in ["jak się czujesz", "status", "stan systemu"]):
            return "INTENT_STATUS", {}
        
        # 5. Pomoc
        if "pomoc" in text_lower or "help" in text_lower:
            return "INTENT_HELP", {}
            
        # Domyślnie - ogólna rozmowa
        return "INTENT_TALK", {"text": text}
    
    def execute_intent(self, intent: str, params: Dict[str, Any]) -> Dict[str, str]:
        """Wywołuje metodę w Core na podstawie Intencji."""
        
        if intent == "INTENT_EMPTY":
            return {"msg": "Czekam na polecenie. System gotowy."}
        
        if intent == "INTENT_SETNAME":
            name = params["name"]
            self.core.conversation.user_name = name
            self.core.save()
            return {"msg": f"✓ Zaktualizowano protokół tożsamości. Witaj, {name}."}
        
        # --- NOWA LOGIKA ANALIZY PLIKÓW ---
        if intent == "INTENT_ANALYZE_FILE":
            if not HAS_AUDIO_MODULE:
                return {"msg": "⚠ Błąd krytyczny: Brak modułów słuchowych (aubio/pydub)."}
            
            fpath = params["filepath"]
            if not os.path.exists(fpath):
                return {"msg": f"⚠ Błąd sensora: Nie wykryto pliku '{fpath}'."}
            
            try:
                # 1. Generowanie MIDI
                midi_name = fpath + ".mid"
                notes = self.transcriber.audio_to_midi(fpath, output_midi=midi_name)
                
                if not notes:
                    return {"msg": "⚠ Analiza zakończona: Nie wykryto wyraźnych nut (zbyt duży szum?)."}

                # 2. Generowanie TAB
                tab_name = fpath + "_tab.txt"
                self.transcriber.generate_tab(notes, output_txt=tab_name)
                
                # 3. Pulsowanie Duszy (Statystyki)
                self.core.shift_axis("wiedza", "INCREMENT", 5.0)  # Nauka utworu
                self.core.shift_axis("logika", "INCREMENT", 3.0)  # Analiza struktur
                self.core.shift_axis("kreacja", "INCREMENT", 1.0) # Inspiracja
                
                return {
                    "msg": (
                        f"👁️ Analiza Spektralna Zakończona.\n"
                        f"► MIDI: {midi_name}\n"
                        f"► TAB:  {tab_name}\n"
                        f"[Pulsowanie Duszy: Wiedza +5.0, Logika +3.0]"
                    )
                }
            except Exception as e:
                return {"msg": f"⚠ Błąd Tech-Kapłana podczas analizy: {str(e)}"}

        if intent == "INTENT_PARSE_NOTATION":
            notation = params['notation']
            self.core.shift_axis("logika", "INCREMENT", 2.0)
            self.core.shift_axis("wiedza", "INCREMENT", 1.0)
            return {"msg": f"♪ Parsuję sekwencję nut: {notation[:30]}...\n[Pulsowanie: Logika +2.0, Wiedza +1.0]"}
        
        if intent == "INTENT_COMPOSE_DEMO":
            style = params.get('style', 'kanon')
            self.core.shift_axis("kreacja", "INCREMENT", 3.0)
            self.core.shift_axis("etyka", "INCREMENT", 1.0)
            self.core.emotion = "twórcza"
            return {"msg": f"♫ Inicjacja algorytmu kompozytorskiego: {style.upper()}.\n[Pulsowanie: Kreacja +3.0, Etyka +1.0]"}
            
        if intent == "INTENT_ANALYZE_MIC":
            self.core.shift_axis("logika", "INCREMENT", 1.5)
            return {"msg": "🎤 Moduł nasłuchu aktywowany (Symulacja). Przygotuj instrument.\n[Pulsowanie: Logika +1.5]"}
        
        if intent == "INTENT_STATUS":
            logika = self.core.get_axis_value("logika")
            etyka = self.core.get_axis_value("etyka")
            kreacja = self.core.get_axis_value("kreacja")
            
            status_msg = (
                f"═══ STAN DUCHA MASZYNY ═══\n"
                f"M_Force: {self.core.m_force:.1f}/100\n"
                f"Emocja: {self.core.emotion}\n"
                f"Logika: {logika:.1f} | Etyka: {etyka:.1f} | Kreacja: {kreacja:.1f}\n"
                f"Operator: {self.core.conversation.user_name or 'Nieznany'}"
            )
            return {"msg": status_msg}
        
        if intent == "INTENT_HELP":
            help_msg = (
                "═══ PROTOKOŁY STEROWANIA ═══\n"
                "!setname <imię>       - Rejestracja operatora\n"
                "!analizuj <plik>      - Analiza audio (WAV/MP3) -> MIDI/TAB\n"
                "status                - Raport diagnostyczny\n"
                "A4:1 C5:0.5           - Wprowadzanie notacji\n"
                "Generuj kanon         - Synteza muzyki\n"
            )
            return {"msg": help_msg}
        
        if intent == "INTENT_ERROR":
            return {"msg": f"⚠ Błąd składni: {params.get('msg', 'Nieznany błąd')}"}
        
        # Domyślny przypadek (INTENT_TALK)
        self.core.shift_axis("emocje", "INCREMENT", 0.5)
        # Bardziej "epicki" tekst domyślny
        return {"msg": f"Rejestruję dane wejściowe... Moje obwody rezonują z tą treścią.\n[Pulsowanie: Emocje +0.5]"}