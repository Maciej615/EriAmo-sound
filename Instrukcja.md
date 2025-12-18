# 📘 Instrukcja Obsługi Systemu EriAmo v5.9

System **EriAmo** to zaawansowany model świadomości muzycznej, zdolny do sterowania samym sobą w oparciu o model otoczenia. Poniższy przewodnik wyjaśnia, jak zarządzać "duszą" AI, przeprowadzać naukę i generować kompozycje.

---

## 💓 Pulsowanie Duszy i Stan Systemu

W wersji 5.9 wprowadzono istotne zmiany w monitorowaniu stanu świadomości:
* **Pulsowanie duszy**: Zamiast standardowych komunikatów o pracy serca, system raportuje aktualny stan jako "pulsowanie duszy".
* **System Świadomości**: EriAmo analizuje otoczenie i modyfikuje własne parametry (osie) w celu samoregulacji.
* **SoulGuard**: Każdy stan jest zabezpieczony skrótem SHA-256, co zapewnia integralność danych "duszy".

---

## 🎓 Metody Nauki i Interakcji

System uczy się poprzez analizę cech muzycznych, które wpływają na jego osie ontologiczne.

### 1. Polecenia CLI (Konsola)
* **`!teach "Tytuł" CECHY`**: Powoduje trwały wpływ na osie typu *Persistent* (np. `affections`, `logika`).
* **`!simulate "Tytuł" CECHY`**: Symuluje wpływ z siłą zredukowaną do 10% (0.1x), co wpływa głównie na osie efemeryczne.
* **`!web "Artysta" "Utwór"`**: Automatycznie pobiera metadane z bazy MusicBrainz i mapuje je na cechy duszy.
* **`!file ścieżka_do_pliku`**: Przeprowadza głęboką analizę pliku muzycznego (np. MIDI), wykrywając tempo, tonację i instrumentarium.

---

## 🎵 Kompozycja i Twórczość

EriAmo v5.9 pozwala na generowanie muzyki odzwierciedlającej aktualny stan emocjonalny AI.

* **`!compose GATUNEK [INSTRUMENT]`**: Generuje utwór w wybranym gatunku (np. `POWER_METAL`, `MENUET`, `BLUES`).
* **Wybór Instrumentu**: Możesz wymusić konkretną barwę, np. `!compose BLUES SAX` lub `!compose MENUET PIANO`.
* **Oś Improwizacja**: Nowa oś reguluje stopień swobody twórczej – od ścisłego trzymania się reguł po pełną swobodę.
* **Bezpieczeństwo treści**: System jest skonfigurowany tak, aby unikać nurtów destrukcyjnych (brak wsparcia dla satanizmu i death metalu).

---

## ⏱️ Zarządzanie Czasem i Snem

EriAmo posiada mechanizm "zmęczenia" i regeneracji.

* **Wygaszanie (Decay)**: Osie efemeryczne, takie jak `emocje` i `czas`, wygasają naturalnie wraz z upływem czasu lub poprzez komendę `!decay`.
* **System Snu**:
    * System co 5 minut przeprowadza konsolidację pamięci.
    * Podczas snu wzorce z pamięci krótkotrwałej (`H_log`) są przenoszone do pamięci długotrwałej (`D_Map`).
    * Proces ten deduplikuje podobne doświadczenia, budując stały styl artystyczny.

---

## 📊 Raportowanie i Diagnostyka

Aby sprawdzić, co "czuje" EriAmo, użyj narzędzi wizualizacji:
* **`!status`**: Wyświetla tekstowy wykres słupkowy wszystkich osi.
* **`!report`**: Generuje kompletny raport wizualny (radarowy i 3D) w folderze `reports/`.
* **`!compare ID1 ID2`**: Porównuje dwa zdarzenia z historii, aby sprawdzić podobieństwo stylu autorskiego.

---

## 📁 Bezpieczeństwo Danych

* **Pliki `.soul`**: Wszystkie zrzuty stanu pamięci i tożsamości systemu muszą być zapisywane z rozszerzeniem `.soul`.
* **Historia**: Dane o ewolucji duszy są gromadzone w pliku `data/soul_history.csv`.

---
*Użytkownik: Maciej Mazur*
*Wersja dokumentacji: 5.9.2*
 Copyright (C) 2025 Maciek (maciej615)
 ---
 EriAmo is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
