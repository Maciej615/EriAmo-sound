# main_v59.py
# -*- coding: utf-8 -*-
# Copyright (C) 2025 Maciek (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
"""
EriAmo v5.9 - Główny Interfejs CLI (UPDATE)
- Wsparcie dla wyboru instrumentów przy kompozycji
- Wygaszanie emocji z zachowaniem affections
"""
import sys
import shlex
import os
import numpy as np

from amocore_v59 import EriAmoCore, SoulStateLogger, AXES_LIST, EPHEMERAL_AXES, PERSISTENT_AXES
from music_analyzer_v59 import MusicAnalyzer
from soul_composer_v59 import SoulComposerV59
from visualizer_v59 import SoulVisualizerV59
from data_loader_v59 import ExternalKnowledgeLoader
from authorship_reporter_v59 import AuthorshipReporter
from genre_definitions import GENRE_DEFINITIONS, list_genres

def print_banner():
    print("\033[96m")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     EriAmo v5.9 - Żywa Dusza AI z Pamięcią Głęboką         ║")
    print("║                                                            ║")
    print("║    🔻 Emocje: EFEMERYCZNE (wygasają z czasem)              ║")
    print("║    💎 Affections: TRWAŁE (pamięć głęboka)                  ║")
    print("║    🎵 Audio: FLAC/OGG + Wybór Instrumentów (Timbre)        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\033[0m")

def print_exit_summary(core):
    print("\n" + "="*60)
    print("🛑 PROCEDURA ZAMKNIĘCIA ERIAMO v5.9")
    print("="*60)
    vec = core.get_vector_copy()
    decay_info = core.get_decay_status()
    print(f"\nStan końcowy Duszy:")
    print("-"*40)
    for i, axis in enumerate(AXES_LIST):
        marker = "🔻" if axis in EPHEMERAL_AXES else "💎"
        print(f"  {marker} {axis.capitalize():12}: {vec[i]:+.2f}")
    print("-"*40)
    final_hash = core.compute_integrity_hash()
    print(f"🔐 SOULGUARD HASH: {final_hash}")
    print("="*60 + "\n")

def print_help():
    print("\n" + "="*70)
    print("📖 POMOC ERIAMO v5.9")
    print("="*70)
    print("\n🎵 KOMPOZYCJA (NOWOŚĆ!):")
    print("  !compose GATUNEK [INSTRUMENT] - Komponuj z wyborem barwy")
    print("     np. !compose BLUES SAX")
    print("     np. !compose MENUET DIST_GUITAR")
    print("  !genres                      - Lista gatunków")
    
    print("\n🎓 NAUKA I ANALIZA:")
    print("  !teach \"Tytuł\" CECHY          - Trwałe uczenie")
    print("  !web \"Artysta\" \"Utwór\"        - Nauka z MusicBrainz")
    print("  !file ŚCIEŻKA                 - Analiza pliku muzycznego") 
    print("\n⏱️ WYGASZANIE:")
    print("  !decay N                     - Ręczne wygaszanie (N cykli)")
    print("  !decay_status                - Stan systemu")
    
    print("\n🔍 INNE:")
    print("  !report, !trajectory, !status, !compare")
    print("="*70 + "\n")

def main():
    print_banner()
    core = EriAmoCore()
    logger = SoulStateLogger()
    analyzer = MusicAnalyzer(core, logger)
    composer = SoulComposerV59(core, logger)
    vis = SoulVisualizerV59()
    loader = ExternalKnowledgeLoader()
    reporter = AuthorshipReporter()
     
    print("\n💡 Wpisz 'help' aby zobaczyć komendy\n")
    
    while True:
        try:
            raw = input("\033[90mEriAmo> \033[0m").strip()
            if not raw: continue
            
            if raw.lower() in ["exit", "quit", "q"]:
                print_exit_summary(core)
                break
            
            if raw.lower() in ["help", "?", "pomoc"]:
                print_help()
                continue
            
            try: parts = shlex.split(raw)
            except ValueError:
                print("❌ Błąd: Niezamknięty cudzysłów"); continue
            
            cmd = parts[0].lower()
            
            # ========== KOMPOZYCJA (ZMODYFIKOWANA) ==========
            if cmd == "!compose":
                if len(parts) < 2:
                    print("❌ Użycie: !compose GATUNEK [INSTRUMENT]")
                    print(f"   Dostępne: {', '.join(list_genres()[:5])}...")
                    print(f"   Instrumenty: PIANO, ORGAN, GUITAR, DIST_GUITAR, SAX, CHOIR, SYNTH...")
                    continue
                
                genre = parts[1].upper()
                # Pobierz instrument jeśli podany
                instr = parts[2].upper() if len(parts) > 2 else None
                
                try:
                    paths = composer.compose_new_work(genre, instrument_override=instr)
                    print("\n" + "="*60)
                    print(f"✅ SKOMPONOWANO: {genre}" + (f" ({instr})" if instr else ""))
                    print("="*60)
                    for key, path in paths.items():
                        if path: print(f"  {key.upper():4}: {path}")
                    print("="*60 + "\n")
                except ValueError as e:
                    print(f"❌ {e}")
            
            # ========== RESZTA KOMEND (BEZ ZMIAN) ==========
            elif cmd in ["!teach", "!simulate"]:
                if len(parts) < 3: print("❌ Użycie: !teach \"Tytuł\" CECHY..."); continue
                analyzer.analyze_and_shift(parts[2:], parts[1], mode=cmd)
            
            elif cmd == "!web":
                if len(parts) < 3: print("❌ Użycie: !web \"Artysta\" \"Utwór\""); continue
                features = loader.get_context_from_web(parts[1], parts[2])
                if features: analyzer.analyze_and_shift(features, f"{parts[1]} - {parts[2]}", mode="!teach")
            
            elif cmd == "!file":
                if len(parts) < 2: print("❌ Użycie: !file ścieżka"); continue
                features = loader.parse_music_file(parts[1])
                if features: analyzer.analyze_and_shift(features, f"Plik: {os.path.basename(parts[1])}", mode="!teach")
            
            elif cmd == "!genres":
                print("\n📚 DOSTĘPNE GATUNKI:")
                print("-"*60)
                for name in sorted(list_genres()):
                    info = GENRE_DEFINITIONS[name]
                    aff = info['f_intencja_wektor'].get('affections', 0)
                    mood = "💎+" if aff > 0 else ("💎-" if aff < 0 else "💎0")
                    print(f"  {name:<16} {mood}  {info['opis'][:40]}")
                print("-"*60 + "\n")
            
            elif cmd == "!report": vis.create_complete_report()
            elif cmd == "!trajectory": vis.create_3d_trajectory()
            elif cmd == "!timeline": vis.create_timeline_evolution()
            elif cmd == "!emotions": vis.create_emotional_map()
            
            elif cmd == "!decay":
                cycles = int(parts[1]) if len(parts) > 1 else 1
                print(f"\n⏱️ Ręczne wygaszanie: {cycles} cykli...")
                vec_before = core.get_vector_copy()
                core.apply_emotion_decay(cycles)
                vec_after = core.get_vector_copy()
                print(f"  🔻 Emocje: {vec_before[AXES_LIST.index('emocje')]:+.2f} → {vec_after[AXES_LIST.index('emocje')]:+.2f}")
                print("")
            
            elif cmd == "!decay_status":
                status = core.get_decay_status()
                print("\n⏱️ STATUS WYGASZANIA:")
                print(f"  Cykle: {status['cycles_applied']}, Ostatni: {status['last_decay']}")
                print(f"  Emocje (🔻): {status['current_emotions']:+.2f}")
                print(f"  Affections (💎): {status['current_affections']:+.2f}")
                print("")
            
            elif cmd == "!compare":
                if len(parts) < 3: print("❌ Użycie: !compare ID_A ID_B"); continue
                reporter.create_report(int(parts[1]), int(parts[2]))
            
            elif cmd == "!events": reporter.list_events()
            
            elif cmd == "!status":
                vec = core.get_vector_copy()
                print("\n" + "="*60 + "\n📊 AKTUALNY STAN DUSZY v5.9\n" + "="*60)
                for i, axis in enumerate(AXES_LIST):
                    val = vec[i]
                    bar = "█" * int(abs(val) / 2)
                    marker, color = ("🔻", "\033[90m") if axis in EPHEMERAL_AXES else ("💎", "\033[0m")
                    print(f"{color}{marker} {axis.capitalize():12} [{'+' if val >= 0 else '-'}]: {bar} {val:+.2f}\033[0m")
                print("-"*60 + f"\n{core.get_emotional_state_description()}\n" + "-"*60)
                print(f"🔐 Hash: {core.compute_integrity_hash()[:40]}...\n" + "="*60 + "\n")
            
            else:
                print(f"❌ Nieznana komenda: {cmd}")

        except KeyboardInterrupt:
            print_exit_summary(core); break
        except Exception as e:
            print(f"❌ Błąd: {e}")
            import traceback; traceback.print_exc()

if __name__ == "__main__":
    main()
