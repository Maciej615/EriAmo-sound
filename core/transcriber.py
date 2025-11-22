# -*- coding: utf-8 -*-
# core/transcriber.py
# =============================================================================
# Audio Engine v0.3 - Psychoakustyka (Siren & Shaman Patch)
# =============================================================================

import os
import aubio
import numpy as np
from midiutil import MIDIFile
from pydub import AudioSegment

class AudioTranscriber:
    def __init__(self):
        self.samplerate = 44100
        self.hop_size = 512
        # Strojenie Standard E (do tabulatur)
        self.tuning_strings = [64, 59, 55, 50, 45, 40]

    def convert_to_wav(self, filepath):
        if filepath.lower().endswith('.wav'): return filepath
        # Konwersja MP3/inne na WAV
        audio = AudioSegment.from_file(filepath)
        wav_path = filepath + ".temp.wav"
        audio.export(wav_path, format="wav")
        return wav_path

    def analyze_psychoacoustics(self, notes):
        """
        Analizuje duszę utworu: Rytmika (The Hu) vs Wysokość (Tarja).
        """
        if not notes or len(notes) < 2:
            return {
                "density": 0, "pitch_range": 0, 
                "max_pitch": 0, "rhythm_consistency": 0
            }

        pitches = [n[1] for n in notes]
        times = [n[0] for n in notes]
        
        # 1. Analiza Wysokości (Dla Tarji/Tenorów)
        min_p, max_p = min(pitches), max(pitches)
        pitch_range = max_p - min_p
        
        # 2. Analiza Gęstości
        duration = times[-1] - times[0] if times else 1
        density = len(notes) / duration if duration > 0 else 0
        
        # 3. Analiza Rytmiczna (Dla The Hu / Szamanizmu)
        # Obliczamy różnice czasu między kolejnymi nutami (delta)
        deltas = np.diff(times)
        if len(deltas) > 0:
            # Odchylenie standardowe delty. Małe odchylenie = Równy Rytm (Marsz).
            # Duże odchylenie = Jazz/Chaos/Rubato.
            rhythm_std = np.std(deltas)
            # Odwracamy: Im mniejsze odchylenie, tym wyższa spójność (max 10)
            rhythm_consistency = 10.0 / (rhythm_std + 0.1)
        else:
            rhythm_consistency = 0

        return {
            "pitch_range": pitch_range,       # Epickość melodii
            "max_pitch": max_p,               # Wysoki rejestr (Siren Call)
            "density": density,               # Szybkość/Złożoność
            "rhythm_consistency": rhythm_consistency # Szamański Puls
        }

    def audio_to_midi(self, filename, output_midi="output.mid"):
        # --- Standardowa detekcja nut (jak w v0.2) ---
        print(f"[AUDIO] Analiza: {filename}")
        wav_file = self.convert_to_wav(filename)
        
        s = aubio.source(wav_file, self.samplerate, self.hop_size)
        pitch_o = aubio.pitch("yin", 2048, self.hop_size, self.samplerate)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(0.8)

        notes = []
        total_frames = 0
        
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()
            if confidence > 0.6 and pitch > 0:
                notes.append((total_frames / float(self.samplerate), int(round(pitch))))
            total_frames += read
            if read < self.hop_size: break

        if wav_file != filename and os.path.exists(wav_file):
            os.remove(wav_file)

        # Zapis MIDI
        mf = MIDIFile(1)
        mf.addTrackName(0, 0, "Amo Core")
        mf.addTempo(0, 0, 120)
        
        unique_notes = []
        last_note = -1
        # Prosta kwantyzacja do MIDI
        for t, p in notes:
            if p != last_note:
                mf.addNote(0, 0, p, t, 0.25, 100)
                unique_notes.append((t, p))
                last_note = p
                
        with open(output_midi, 'wb') as f: mf.writeFile(f)
        
        return unique_notes

    def generate_tab(self, midi_notes, output_txt="tab.txt"):
        # --- Generator Tabulatury (jak w v0.2) ---
        pitches = [n[1] for n in midi_notes] if midi_notes and isinstance(midi_notes[0], tuple) else midi_notes
        lines = {i: [] for i in range(6)} 
        
        for note in pitches:
            best_string, best_fret = -1, 100
            for s_idx, open_n in enumerate(self.tuning_strings):
                fret = note - open_n
                if 0 <= fret <= 24 and fret < best_fret:
                    best_fret, best_string = fret, s_idx
            for i in range(6):
                lines[i].append(f"-{best_fret}-".ljust(4, '-') if i == best_string else "----")
        
        with open(output_txt, "w") as f:
            f.write("=== AMO MUSICA TABULATURE ===\n\n")
            for i in range(0, len(lines[0]), 16):
                f.write("\n")
                for s in range(6): 
                    s_name = ['e','B','G','D','A','E'][s]
                    f.write(f"{s_name}|{''.join(lines[s][i:i+16])}|\n")
        return output_txt
