# authorship_reporter_v59.py
# -*- coding: utf-8 -*-
"""
Raporter Atrybucji Autorstwa EriAmo v5.9
- Porównanie stylów między zdarzeniami
- Analiza wektorowa podobieństwa
"""
import pandas as pd
import numpy as np
import os
from amocore_v59 import AXES_LIST, EPHEMERAL_AXES, PERSISTENT_AXES


class AuthorshipReporter:
    """
    Analizator porównawczy stylów muzycznych.
    
    Porównuje wektory F (styl utworu) między zdarzeniami,
    uwzględniając rozróżnienie osi efemerycznych i trwałych.
    """
    DATA_PATH = "data/soul_history.csv"
    REPORT_DIR = "reports_attribution"

    def __init__(self):
        os.makedirs(self.REPORT_DIR, exist_ok=True)

    def get_event_vector(self, event_id: int) -> tuple:
        """
        Pobiera wektor F dla danego zdarzenia.
        
        Returns:
            (wektor_F, opis) lub (None, None)
        """
        try:
            df = pd.read_csv(self.DATA_PATH)
            row = df[df['id_event'] == int(event_id)]
            
            if row.empty:
                raise ValueError(f"ID {event_id} nie znaleziono")
            
            vector_f = np.array([row.iloc[0][f"F_{axis}"] for axis in AXES_LIST])
            description = row.iloc[0]['description']
            
            return vector_f, description
            
        except Exception as e:
            print(f"[RAPORT] Błąd: {e}")
            return None, None

    def create_report(self, id_a: int, id_b: int):
        """
        Porównuje dwa zdarzenia i generuje raport atrybucji.
        
        Uwzględnia:
        - Podobieństwo ogólne (wszystkie osie)
        - Podobieństwo trwałe (tylko osie persistent)
        - Podobieństwo efemeryczne (tylko osie ephemeral)
        """
        vec_a, name_a = self.get_event_vector(id_a)
        vec_b, name_b = self.get_event_vector(id_b)
        
        if vec_a is None or vec_b is None:
            return
        
        # Indeksy osi
        persistent_idx = [AXES_LIST.index(a) for a in PERSISTENT_AXES]
        ephemeral_idx = [AXES_LIST.index(a) for a in EPHEMERAL_AXES]
        
        # Funkcja pomocnicza do obliczania podobieństwa
        def cosine_sim(v1, v2):
            n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
            if n1 > 0 and n2 > 0:
                return np.dot(v1, v2) / (n1 * n2)
            return 0.0
        
        # 1. Podobieństwo ogólne
        sim_total = cosine_sim(vec_a, vec_b)
        
        # 2. Podobieństwo na osiach TRWAŁYCH (pamięć głęboka)
        vec_a_pers = vec_a[persistent_idx]
        vec_b_pers = vec_b[persistent_idx]
        sim_persistent = cosine_sim(vec_a_pers, vec_b_pers)
        
        # 3. Podobieństwo na osiach EFEMERYCZNYCH
        vec_a_eph = vec_a[ephemeral_idx]
        vec_b_eph = vec_b[ephemeral_idx]
        sim_ephemeral = cosine_sim(vec_a_eph, vec_b_eph)
        
        # WERDYKT - bazujemy głównie na osiach TRWAŁYCH!
        if sim_persistent > 0.92:
            verdict = "✅ POTWIERDZONO: TEN SAM STYL GŁĘBOKI"
            verdict_color = "\033[92m"
        elif sim_persistent > 0.75:
            verdict = "🔶 WYSOKIE PRAWDOPODOBIEŃSTWO (podobna wrażliwość)"
            verdict_color = "\033[93m"
        elif sim_persistent > 0.5:
            verdict = "🔷 MOŻLIWE PODOBIEŃSTWO (wspólne wpływy)"
            verdict_color = "\033[94m"
        else:
            verdict = "❌ RÓŻNE STYLE / AUTORZY"
            verdict_color = "\033[91m"
        
        # Wydruk raportu
        print("\n" + "="*70)
        print("🔬 RAPORT ATRYBUCJI AUTORSTWA v5.9")
        print("="*70)
        print(f"Obiekt A (ID {id_a}): {name_a}")
        print(f"Obiekt B (ID {id_b}): {name_b}")
        print("-"*70)
        
        print(f"\n📊 ANALIZA PODOBIEŃSTWA:")
        print(f"   Ogólne (wszystkie osie):     {sim_total:+.4f}")
        print(f"   💎 TRWAŁE (pamięć głęboka):   {sim_persistent:+.4f}  ← KLUCZOWE")
        print(f"   🔻 Efemeryczne (chwilowe):    {sim_ephemeral:+.4f}")
        
        print(f"\n{verdict_color}   WERDYKT: {verdict}\033[0m")
        
        print("\n" + "-"*70)
        print("📈 PORÓWNANIE WEKTOROWE (Delta = B - A):")
        print(f"{'Oś':<14} | {'Typ':<10} | {'A':<8} | {'B':<8} | {'Delta':<10}")
        print("-"*70)
        
        for i, axis in enumerate(AXES_LIST):
            val_a = vec_a[i]
            val_b = vec_b[i]
            delta = val_b - val_a
            
            # Typ osi
            if axis in EPHEMERAL_AXES:
                axis_type = "efemer."
                color = "\033[90m"  # Szary
            else:
                axis_type = "TRWAŁA"
                color = "\033[0m"   # Normalny
            
            # Zaznacz istotne różnice
            marker = ""
            if abs(delta) >= 3.0:
                marker = " ⚠️ ZNACZĄCA"
            elif abs(delta) >= 1.5:
                marker = " ↗"
            
            print(f"{color}{axis.capitalize():<14} | {axis_type:<10} | "
                  f"{val_a:<+8.1f} | {val_b:<+8.1f} | {delta:<+10.1f}{marker}\033[0m")
        
        print("="*70)
        
        # Interpretacja
        print("\n💡 INTERPRETACJA:")
        if sim_persistent > 0.75:
            print("   Wysokie podobieństwo na osiach TRWAŁYCH sugeruje wspólną")
            print("   wrażliwość estetyczną, głębokie wpływy lub tego samego autora.")
        if abs(sim_persistent - sim_ephemeral) > 0.3:
            print("   Duża rozbieżność między trwałym a efemerycznym może wskazywać")
            print("   na różne momenty twórcze tego samego autora.")
        
        print("="*70 + "\n")

    def list_events(self, limit: int = 20):
        """Wyświetla listę ostatnich zdarzeń."""
        try:
            df = pd.read_csv(self.DATA_PATH)
            if df.empty:
                print("Brak zdarzeń w historii.")
                return
            
            print("\n" + "="*60)
            print("📋 OSTATNIE ZDARZENIA")
            print("="*60)
            
            for _, row in df.tail(limit).iterrows():
                print(f"ID {int(row['id_event']):4d} | {row['mode']:<10} | {row['description'][:40]}")
            
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"Błąd: {e}")
