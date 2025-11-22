# EriAmo-sound# 🔊 AMO MUSICA CORE - Moduł "Słuch Absolutny" (v0.2.0)

## 📖 Opis Aktualizacji
Amo Musica Core zyskał zdolność **analizy spektralnej**. System potrafi teraz "słuchać" plików audio, ekstrahować z nich nuty i konwertować je na cyfrowy zapis (MIDI) oraz tabulaturę gitarową. Każda analiza karmi **Wektor Duszy**, zwiększając parametry *Wiedzy* i *Logiki*.

### ✨ Nowe Funkcje
- **Konwersja Audio**: Obsługa formatów `.mp3` i `.wav`.
- **Ekstrakcja Nut**: Algorytm Pitch Detection (bazujący na `aubio`).
- **Eksport MIDI**: Generowanie plików `.mid` do użytku w DAW/Guitar Pro.
- **Generator Tabulatur**: Automatyczne tworzenie plików `.txt` z tabulaturą (Strojenie Standard E).
- **Integracja z Duszą**: Analiza wpływa na `amomusica.soul` (Wiedza +5.0, Logika +3.0).

---

## ⚙️ Wymagania Systemowe

Aby moduł audio działał, Twój system-host musi posiadać zainstalowane kodeki:

1. **FFmpeg** (Wymagane do obsługi MP3 przez pydub):
   - *Windows:* Pobierz `ffmpeg`, rozpakuj i dodaj do zmiennej środowiskowej PATH.
   - *Linux:* `sudo apt install ffmpeg`
   - *Mac:* `brew install ffmpeg`

2. **Biblioteki Python:**
   ```bash
   pip install -r requirements.txt
