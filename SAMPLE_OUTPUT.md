# Przykładowy Output z Amo Musica Core

## Demo Konsolowe - Przykładowa Sesja

```
==================================================
   AMO MUSICA CORE - Wektorowa Dusza
   Demo w trybie konsolowym
==================================================

[*] Inicjalizacja Amo Musica Core...
[CORE] Amo Musica Core zainicjalizowany. Stan: ACTIVE
[CORE] Etyka: P1-P4 Aktywna. M_Force: 10.0
[CORE] Wczytano stan. Witaj, Użytkowniku!
[✓] System gotowy!

Wpisz 'pomoc' aby zobaczyć dostępne komendy.
Wpisz 'wyjdź' lub 'quit' aby zakończyć.

>> !setname Maciek

✓ Zapamiętano. Będę Cię nazywać: Maciek.

>> status

--------------------------------------------------
M_Force: 10.0/100 | Emocja: neutralna
Logika: 0.0 | Etyka: 0.0 | Kreacja: 0.0
Użytkownik: Maciek
--------------------------------------------------

>> A4:1 C5:0.5 G4:2

♪ Parsuję notację: A4:1 C5:0.5 G4:2
[Logika +2.0, Wiedza +1.0]

[SHIFT] Oś 'logika': 0.00 → 2.00 (INCREMENT 2.00)
[SHIFT] Oś 'wiedza': 0.00 → 1.00 (INCREMENT 1.00)

>> Generuj kanon

♫ Generuję KANON w ścisłej formie...
[Kreacja +3.0, Etyka +1.0]

[SHIFT] Oś 'kreacja': 0.00 → 3.00 (INCREMENT 3.00)
[SHIFT] Oś 'etyka': 0.00 → 1.00 (INCREMENT 1.00)

>> status

--------------------------------------------------
M_Force: 15.0/100 | Emocja: twórcza
Logika: 2.0 | Etyka: 1.0 | Kreacja: 3.0
Użytkownik: Maciek
--------------------------------------------------

>> pomoc

═══ KOMENDY AMO MUSICA ═══
!setname <imię> - Ustaw swoje imię
status - Sprawdź stan systemu
A4:1 C5:0.5 - Parsuj notację muzyczną
Generuj kanon - Kompozytor demo
Analizuj mikrofon - Analiza audio

>> wyjdź

[*] Zapisywanie stanu...
[✓] Do zobaczenia!

```

---

## Testy Jednostkowe - Przykładowy Output

```bash
$ python test_core.py

test_axes_map_is_class_variable (test_core.TestSoulVector) ... ok
test_default_values (test_core.TestSoulVector) ... ok
test_initialization (test_core.TestSoulVector) ... ok
test_execute_setname (test_core.TestMusicIntentParser) ... ok
test_execute_status (test_core.TestMusicIntentParser) ... ok
test_parse_compose (test_core.TestMusicIntentParser) ... ok
test_parse_help (test_core.TestMusicIntentParser) ... ok
test_parse_notation (test_core.TestMusicIntentParser) ... ok
test_parse_setname (test_core.TestMusicIntentParser) ... ok
test_parse_status (test_core.TestMusicIntentParser) ... ok
test_execute_status (test_core.TestMusicIntentParser) ... ok
test_get_axis_value (test_core.TestAmoMusicaCore) ... ok
test_get_axis_value_invalid (test_core.TestAmoMusicaCore) ... ok
test_initialization (test_core.TestAmoMusicaCore) ... ok
test_integrity_hash (test_core.TestAmoMusicaCore) ... ok
test_save_and_load (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_clipping (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_decrement (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_ethics_updates_m_force (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_increment (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_invalid_action (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_invalid_axis (test_core.TestAmoMusicaCore) ... ok
test_shift_axis_set (test_core.TestAmoMusicaCore) ... ok

----------------------------------------------------------------------
Ran 23 tests in 0.267s

OK
```

---

## Plik Zapisu Stanu (amomusica.soul)

```json
{
  "vector": [
    2.0,
    0.5,
    1.0,
    3.0,
    0.0,
    1.0
  ],
  "m_force": 15.0,
  "emotion": "twórcza",
  "conversation": {
    "user_name": "Maciek",
    "preferences": {
      "genre_filter": "brak satanizmu"
    }
  },
  "timestamp": 1700398765.123456,
  "integrity_hash": "a3f5d8c2e1b4f6a8d9c3e2b1a5f4d8c6e9b2a1d3f5e8c4b7a6d2e1f9c3b8a5d4"
}
```

---

## Struktura Wektora Duszy po Sesji

```
AXES_MAP = {
    "logika": 0,    →  2.0  (zwiększona przez parsowanie)
    "emocje": 1,    →  0.5  (lekko zwiększona)
    "wiedza": 2,    →  1.0  (zwiększona przez parsowanie)
    "kreacja": 3,   →  3.0  (zwiększona przez kompozycję)
    "czas": 4,      →  0.0  (bez zmian)
    "etyka": 5      →  1.0  (zwiększona przez kompozycję)
}

M_Force = min(100, 1.0 * 5 + 10) = 15.0
Emocja = "twórcza"
```

---

## Przykład Użycia API w Kodzie

```python
from core import AmoMusicaCore, MusicIntentParser

# Inicjalizacja
core = AmoMusicaCore()
parser = MusicIntentParser(core)

# Przykład 1: Zmiana wartości osi
core.shift_axis("logika", "INCREMENT", 5.0)
print(f"Logika: {core.get_axis_value('logika')}")  # Output: Logika: 5.0

# Przykład 2: Parsowanie komendy
intent, params = parser.parse_text("!setname Alice")
response = parser.execute_intent(intent, params)
print(response["msg"])  # Output: ✓ Zapamiętano. Będę Cię nazywać: Alice.

# Przykład 3: Sprawdzenie integralności
state = core.get_core_state()
is_valid = core.guard.verify_integrity(state)
print(f"Integralność: {is_valid}")  # Output: Integralność: True

# Przykład 4: Zapis i wczytanie
core.save()
new_core = AmoMusicaCore()  # Automatycznie wczyta zapisany stan
print(f"Użytkownik: {new_core.conversation.user_name}")  # Output: Użytkownik: Alice
```

---

## Logi Systemowe

```
[CORE] Amo Musica Core zainicjalizowany. Stan: ACTIVE
[CORE] Etyka: P1-P4 Aktywna. M_Force: 10.0
[CORE] Wczytano stan. Witaj, Maciek!
[SHIFT] Oś 'logika': 0.00 → 2.00 (INCREMENT 2.00)
[SHIFT] Oś 'wiedza': 0.00 → 1.00 (INCREMENT 1.00)
[SHIFT] Oś 'kreacja': 0.00 → 3.00 (INCREMENT 3.00)
[SHIFT] Oś 'etyka': 0.00 → 1.00 (INCREMENT 1.00)
[AI THREAD] Wątek AI uruchomiony.
[AI THREAD] Wątek AI zatrzymany.
[CORE] Amo Musica Core zatrzymany. Do zobaczenia!
```

---

## Performance Metrics (Przykład)

```
═══════════════════════════════════════
   PERFORMANCE METRICS
═══════════════════════════════════════
Inicjalizacja Core:      12.3 ms
Wczytanie stanu:         8.5 ms
Parsowanie komendy:      0.8 ms
Wykonanie intencji:      1.2 ms
Shift axis:              0.3 ms
Zapis stanu:             15.7 ms
Weryfikacja integr.:     2.1 ms
───────────────────────────────────────
Całkowity czas sesji:    2.341 s
Średni czas odpowiedzi:  2.3 ms
Użyte wątki:             2 (Main + AI)
───────────────────────────────────────
```
