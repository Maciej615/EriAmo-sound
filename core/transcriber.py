# -*- coding: utf-8 -*-
# core/transcriber.py
# =============================================================================
# Audio Engine - Słuch Absolutny Systemu
# =============================================================================

import os
import aubio
from midiutil import MIDIFile
from pydub import AudioSegment

class AudioTranscriber:
    def __init__(self):
        self.samplerate = 44100
        self.hop_size = 512
        # Strojenie: Standard E (od najcieńszej 'e' do najgrubszej 'E')
        # MIDI numbers: e=64, B=59, G=55, D=50, A=45, E=40
        self.tuning_strings = [64, 59, 55, 50, 45, 40]

    def convert_to_wav(self, filepath):
        """Konwertuje mp3/inne do wav tymczasowo (aubio wymaga wav)."""
        if filepath.lower().endswith('.wav'):
            return filepath
        
        print(f"[AUDIO] Konwersja formatu dla: {filepath}...")
        audio = AudioSegment.from_file(filepath)
        wav_path = filepath + ".temp.wav"
        audio.export(wav_path, format="wav")
        return wav_path

    def audio_to_midi(self, filename, output_midi="output.mid"):
        """Analizuje audio i zwraca listę nut oraz generuje plik MIDI."""
        print(f"[AUDIO] Rozpoczynam ekstrakcję nut z: {filename}")
        wav_file = self.convert_to_wav(filename)
        
        # Konfiguracja Aubio (algorytm YIN jest dobry do pitch detection)
        s = aubio.source(wav_file, self.samplerate, self.hop_size)
        tolerance = 0.8
        pitch_o = aubio.pitch("yin", 2048, self.hop_size, self.samplerate)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)

        notes = []
        total_frames = 0
        
        # Pętla analizy ramka po ramce
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()

            # Filtrujemy szum (confidence > 0.6)
            if confidence > 0.6 and pitch > 0:
                midi_note = int(round(pitch))
                timestamp = total_frames / float(self.samplerate)
                notes.append((timestamp, midi_note))

            total_frames += read
            if read < self.hop_size: break

        # Sprzątanie pliku tymczasowego
        if wav_file != filename and os.path.exists(wav_file):
            os.remove(wav_file)

        if not notes:
            return []

        # --- Generowanie pliku MIDI ---
        mf = MIDIFile(1)
        mf.addTrackName(0, 0, "Amo Core Transcription")
        mf.addTempo(0, 0, 120) # Domyślne tempo

        current_time = 0
        unique_notes = [] 
        
        # Prosta kwantyzacja i usuwanie duplikatów
        last_note = -1
        for time_sec, note in notes:
            # Zapisujemy nową nutę tylko jeśli się zmieniła
            if note != last_note:
                # (track, channel, pitch, time, duration, volume)
                mf.addNote(0, 0, note, time_sec, 0.25, 100) 
                unique_notes.append(note)
                last_note = note

        with open(output_midi, 'wb') as out_f:
            mf.writeFile(out_f)
            
        return unique_notes

    def generate_tab(self, midi_notes, output_txt="tabulatura.txt"):
        """Generuje tekstową tabulaturę gitarową (Standard E)."""
        print("[AUDIO] Obliczam optymalne palcowanie...")
        
        # 6 strun
        lines = {i: [] for i in range(6)} 
        
        for note in midi_notes:
            best_string = -1
            best_fret = 100
            
            # Algorytm szukający najniższego progu (najłatwiejszego do zagrania)
            for str_idx, open_note in enumerate(self.tuning_strings):
                fret = note - open_note
                # Zakres gryfu (0-24 progi)
                if 0 <= fret <= 24:
                    if fret < best_fret:
                        best_fret = fret
                        best_string = str_idx
            
            # Rysowanie tabulatury
            for i in range(6):
                if i == best_string:
                    # Dodajemy padding żeby było równo
                    fret_str = str(best_fret)
                    lines[i].append(f"-{fret_str}-".ljust(4, '-'))
                else:
                    lines[i].append("----")
        
        # Zapis do pliku
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("=== AMO MUSICA CORE - TABULATURA ===\n")
            f.write("Strojenie: Standard E\n\n")
            
            chunk_size = 16 # Ilość nut w jednej linii
            num_notes = len(lines[0])
            
            for i in range(0, num_notes, chunk_size):
                f.write("\n")
                for str_idx in range(6):
                    chunk = "".join(lines[str_idx][i:i+chunk_size])
                    string_name = ["e", "B", "G", "D", "A", "E"][str_idx]
                    f.write(f"{string_name}|{chunk}|\n")
        
        return output_txt