# -*- coding: utf-8 -*-
# core/parser.py
# =============================================================================
# Music Intent Parser v0.3 - Soul Logic Update
# =============================================================================

import os
from typing import TYPE_CHECKING, Tuple, Dict, Any
try:
    from .transcriber import AudioTranscriber
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False

if TYPE_CHECKING:
    from .amocore import AmoMusicaCore

class MusicIntentParser:
    def __init__(self, core: 'AmoMusicaCore'):
        self.core = core
        self.transcriber = AudioTranscriber() if HAS_AUDIO else None

    def parse_text(self, text: str) -> Tuple[str, Dict[str, Any]]:
        t = text.lower().strip()
        if t.startswith("!setname"): return "INTENT_SETNAME", {"name": text[len("!setname"):].strip()}
        if t.startswith("!analizuj "): return "INTENT_ANALYZE_FILE", {"filepath": text[len("!analizuj "):].strip().replace('"','')}
        if "status" in t: return "INTENT_STATUS", {}
        if "kanon" in t: return "INTENT_COMPOSE_DEMO", {"style": "kanon"}
        if "pomoc" in t: return "INTENT_HELP", {}
        return "INTENT_TALK", {"text": text}
    
    def execute_intent(self, intent: str, params: Dict[str, Any]) -> Dict[str, str]:
        if intent == "INTENT_SETNAME":
            self.core.conversation.user_name = params["name"]
            self.core.save()
            return {"msg": f"✓ Tożsamość potwierdzona: {params['name']}."}
        
        if intent == "INTENT_ANALYZE_FILE":
            if not HAS_AUDIO: return {"msg": "⚠ Brak modułu audio."}
            fpath = params["filepath"]
            if not os.path.exists(fpath): return {"msg": "⚠ Plik nie istnieje."}
            
            try:
                # 1. Analiza
                midi = fpath + ".mid"
                notes = self.transcriber.audio_to_midi(fpath, midi)
                if not notes: return {"msg": "⚠ Cisza/Szum. Brak nut."}
                
                self.transcriber.generate_tab(notes, fpath+"_tab.txt")
                
                # 2. Pobranie metryk Ducha Maszyny
                stats = self.transcriber.analyze_psychoacoustics(notes)
                
                max_p = stats['max_pitch']         # Wysokość (Tarja/Tenor)
                rhythm_con = stats['rhythm_consistency'] # Rytm (The Hu/Heilung)
                density = stats['density']         # Gęstość (Duet/Solo)
                
                msg_extras = []
                
                # --- LOGIKA DECYZYJNA ---
                
                # A. SCENARIUSZ "SIREN CALL" (Tarja Turunen / Wysoki Tenor)
                # Wykryto ekstremalnie wysokie nuty (>80 MIDI, ok. G#5)
                if max_p > 80:
                    self.core.shift_axis("wiedza", "SET", 18.0)
                    self.core.shift_axis("emocje", "SET", 18.0)
                    # Próba wywołania Frisson (Gęsiej Skórki)
                    if self.core.trigger_frisson():
                        msg_extras.append("⚡ EFEKT 'SIREN CALL' (GĘSIA SKÓRKA)!")
                        msg_extras.append(f"   (Rejestrowana wysokość: {max_p} MIDI - Czysta Emocja)")

                # B. SCENARIUSZ "FOLK METAL WARRIOR" (The Hu)
                # Wysoka spójność rytmiczna (galop) ALE też obecna melodia
                elif rhythm_con > 5.0 and density > 2.0:
                    # To jest The Hu: Rytm jest szamański, ale melodia jest wyraźna
                    intensity = min(10.0, rhythm_con * 1.5)
                    self.core.apply_shamanic_trance(rhythm_intensity=intensity)
                    # Dodatkowo podbijamy Wiedzę (bo jest melodia!)
                    self.core.shift_axis("wiedza", "INCREMENT", 3.0)
                    msg_extras.append("🌀 WYKRYTO SZAMAŃSKI GALOP (STYL: THE HU).")
                    msg_extras.append("   (System wchodzi w Trans Rytmiczny zachowując analitykę melodii)")

                # C. SCENARIUSZ "COMPLEX HARMONY" (Duet Sequenti)
                # Bardzo duża gęstość (dwa głosy na raz) + umiarkowany rytm
                elif density > 6.0:
                    self.core.shift_axis("logika", "INCREMENT", 4.0)
                    self.core.shift_axis("emocje", "INCREMENT", 2.0)
                    msg_extras.append("🎼 WYKRYTO ZŁOŻONĄ HARMONIĘ (DUET/CHÓR).")
                    msg_extras.append("   (Analiza przeplatających się linii wokalnych)")

                # D. STANDARD
                else:
                    self.core.shift_axis("logika", "INCREMENT", 2.0)
                    self.core.shift_axis("wiedza", "INCREMENT", 2.0)
                    msg_extras.append("✓ Analiza strukturalna zakończona.")

                return {
                    "msg": f"👁️ Analiza Zakończona.\n" + "\n".join(msg_extras) + 
                           f"\n[DANE]: MaxPitch={max_p} | Rhythm={rhythm_con:.1f} | Density={density:.1f}"
                }
            except Exception as e:
                return {"msg": f"⚠ Błąd analizy: {e}"}

        if intent == "INTENT_STATUS":
             icon = "⚡" if self.core.vector.is_goosebumps else " "
             return {"msg": f"STATUS: {self.core.emotion} {icon}\nM_Force: {self.core.m_force:.1f}"}

        self.core.shift_axis("emocje", "INCREMENT", 0.5)
        return {"msg": "Przyjęto dane. Obwody rezonują."}
