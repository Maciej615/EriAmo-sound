# -*- coding: utf-8 -*-
# test_core.py
# =============================================================================
# Testy Jednostkowe dla Amo Musica Core
# =============================================================================

import unittest
import os
import json
import numpy as np
from core.amocore import AmoMusicaCore, SoulVector, GuardStatus
from core.parser import MusicIntentParser


class TestSoulVector(unittest.TestCase):
    """Testy dla klasy SoulVector."""
    
    def test_initialization(self):
        """Test inicjalizacji wektora."""
        vec = SoulVector()
        self.assertEqual(len(vec.values), 6)
        self.assertEqual(len(vec.AXES_MAP), 6)
        
    def test_axes_map_is_class_variable(self):
        """Test, czy AXES_MAP jest zmienną klasy."""
        vec1 = SoulVector()
        vec2 = SoulVector()
        # AXES_MAP powinno być tym samym obiektem dla wszystkich instancji
        self.assertIs(vec1.AXES_MAP, vec2.AXES_MAP)
        
    def test_default_values(self):
        """Test domyślnych wartości wektora."""
        vec = SoulVector()
        np.testing.assert_array_equal(vec.values, np.zeros(6))


class TestAmoMusicaCore(unittest.TestCase):
    """Testy dla klasy AmoMusicaCore."""
    
    def setUp(self):
        """Przygotowanie przed każdym testem."""
        # Użyj tymczasowego pliku
        self.test_file = "data/test_amomusica.soul"
        AmoMusicaCore.FILE_PATH = self.test_file
        self.core = AmoMusicaCore()
        
    def tearDown(self):
        """Czyszczenie po każdym teście."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_file + ".tmp"):
            os.remove(self.test_file + ".tmp")
    
    def test_initialization(self):
        """Test inicjalizacji rdzenia."""
        self.assertEqual(self.core.status, GuardStatus.ACTIVE)
        self.assertEqual(self.core.emotion, "neutralna")
        self.assertEqual(self.core.m_force, 10.0)
        self.assertTrue(self.core.running)
    
    def test_shift_axis_increment(self):
        """Test zwiększania wartości osi."""
        initial = self.core.get_axis_value("logika")
        result = self.core.shift_axis("logika", "INCREMENT", 5.0)
        
        self.assertTrue(result)
        self.assertEqual(self.core.get_axis_value("logika"), initial + 5.0)
    
    def test_shift_axis_decrement(self):
        """Test zmniejszania wartości osi."""
        self.core.shift_axis("logika", "SET", 10.0)
        result = self.core.shift_axis("logika", "DECREMENT", 3.0)
        
        self.assertTrue(result)
        self.assertEqual(self.core.get_axis_value("logika"), 7.0)
    
    def test_shift_axis_set(self):
        """Test ustawiania wartości osi."""
        result = self.core.shift_axis("emocje", "SET", 15.0)
        
        self.assertTrue(result)
        self.assertEqual(self.core.get_axis_value("emocje"), 15.0)
    
    def test_shift_axis_clipping(self):
        """Test ograniczania wartości osi."""
        # Próba przekroczenia maksimum
        self.core.shift_axis("logika", "SET", 100.0)
        self.assertEqual(self.core.get_axis_value("logika"), 20.0)
        
        # Próba przekroczenia minimum
        self.core.shift_axis("logika", "SET", -100.0)
        self.assertEqual(self.core.get_axis_value("logika"), -20.0)
    
    def test_shift_axis_ethics_updates_m_force(self):
        """Test aktualizacji M_Force przez oś etyki."""
        self.core.shift_axis("etyka", "SET", 10.0)
        expected_m_force = min(100.0, 10.0 * 5.0 + 10.0)
        self.assertEqual(self.core.m_force, expected_m_force)
    
    def test_shift_axis_invalid_axis(self):
        """Test obsługi nieprawidłowej osi."""
        result = self.core.shift_axis("nieistniejąca", "INCREMENT", 5.0)
        self.assertFalse(result)
    
    def test_shift_axis_invalid_action(self):
        """Test obsługi nieprawidłowej akcji."""
        result = self.core.shift_axis("logika", "INVALID", 5.0)
        self.assertFalse(result)
    
    def test_get_axis_value(self):
        """Test odczytu wartości osi."""
        self.core.shift_axis("wiedza", "SET", 12.5)
        value = self.core.get_axis_value("wiedza")
        self.assertEqual(value, 12.5)
    
    def test_get_axis_value_invalid(self):
        """Test odczytu nieprawidłowej osi."""
        value = self.core.get_axis_value("nieistniejąca")
        self.assertIsNone(value)
    
    def test_save_and_load(self):
        """Test zapisu i wczytania stanu."""
        # Ustaw wartości
        self.core.shift_axis("logika", "SET", 15.0)
        self.core.shift_axis("etyka", "SET", 8.0)
        self.core.conversation.user_name = "TestUser"
        
        # Zapisz
        self.core.save()
        
        # Stwórz nową instancję (powinna wczytać stan)
        new_core = AmoMusicaCore()
        
        self.assertEqual(new_core.get_axis_value("logika"), 15.0)
        self.assertEqual(new_core.get_axis_value("etyka"), 8.0)
        self.assertEqual(new_core.conversation.user_name, "TestUser")
    
    def test_integrity_hash(self):
        """Test hashowania integralności."""
        self.core.save()
        
        # Hash powinien być ustawiony
        self.assertNotEqual(self.core.guard.integrity_hash, "")
        
        # Weryfikacja powinna przejść
        state = self.core.get_core_state()
        self.assertTrue(self.core.guard.verify_integrity(state))


class TestMusicIntentParser(unittest.TestCase):
    """Testy dla parsera intencji."""
    
    def setUp(self):
        """Przygotowanie przed każdym testem."""
        AmoMusicaCore.FILE_PATH = "data/test_parser.soul"
        self.core = AmoMusicaCore()
        self.parser = MusicIntentParser(self.core)
        
    def tearDown(self):
        """Czyszczenie po każdym teście."""
        if os.path.exists("data/test_parser.soul"):
            os.remove("data/test_parser.soul")
    
    def test_parse_setname(self):
        """Test parsowania komendy setname."""
        intent, params = self.parser.parse_text("!setname TestUser")
        self.assertEqual(intent, "INTENT_SETNAME")
        self.assertEqual(params["name"], "TestUser")
    
    def test_parse_notation(self):
        """Test parsowania notacji muzycznej."""
        intent, params = self.parser.parse_text("A4:1 C5:0.5")
        self.assertEqual(intent, "INTENT_PARSE_NOTATION")
        self.assertIn("notation", params)
    
    def test_parse_compose(self):
        """Test parsowania komendy kompozycji."""
        intent, params = self.parser.parse_text("Generuj kanon")
        self.assertEqual(intent, "INTENT_COMPOSE_DEMO")
        self.assertEqual(params["style"], "kanon")
    
    def test_parse_status(self):
        """Test parsowania komendy status."""
        intent, params = self.parser.parse_text("status")
        self.assertEqual(intent, "INTENT_STATUS")
    
    def test_parse_help(self):
        """Test parsowania komendy pomocy."""
        intent, params = self.parser.parse_text("pomoc")
        self.assertEqual(intent, "INTENT_HELP")
    
    def test_execute_setname(self):
        """Test wykonania komendy setname."""
        intent, params = self.parser.parse_text("!setname Alice")
        response = self.parser.execute_intent(intent, params)
        
        self.assertIn("msg", response)
        self.assertEqual(self.core.conversation.user_name, "Alice")
    
    def test_execute_status(self):
        """Test wykonania komendy status."""
        intent, params = self.parser.parse_text("status")
        response = self.parser.execute_intent(intent, params)
        
        self.assertIn("msg", response)
        self.assertIn("M_Force", response["msg"])


def run_tests():
    """Uruchamia wszystkie testy."""
    # Upewnij się, że katalog data istnieje
    os.makedirs("data", exist_ok=True)
    
    # Uruchom testy
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
