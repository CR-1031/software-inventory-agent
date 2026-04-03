import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.scanner import Software, RegistryScanner


class TestSoftware(unittest.TestCase):
    """Тесты для класса Software"""
    
    def test_software_creation(self):
        """Тест создания объекта Software"""
        sw = Software("Python", "3.10", "PSF", "20240101")
        
        self.assertEqual(sw.name, "Python")
        self.assertEqual(sw.version, "3.10")
        self.assertEqual(sw.publisher, "PSF")
        self.assertEqual(sw.install_date, "20240101")
    
    def test_to_dict(self):
        """Тест преобразования в словарь"""
        sw = Software("Python", "3.10", "PSF", "20240101")
        result = sw.to_dict()
        
        self.assertEqual(result["name"], "Python")
        self.assertEqual(result["version"], "3.10")
        self.assertEqual(result["publisher"], "PSF")
        self.assertEqual(result["install_date"], "20240101")
    
    def test_is_valid_with_name(self):
        """Тест валидности при наличии имени"""
        sw = Software("Python", "", "", "")
        self.assertTrue(sw.is_valid())
    
    def test_is_valid_without_name(self):
        """Тест невалидности при отсутствии имени"""
        sw = Software("", "", "", "")
        self.assertFalse(sw.is_valid())
    
    def test_empty_software(self):
        """Тест пустого объекта"""
        sw = Software()
        self.assertEqual(sw.name, "")
        self.assertEqual(sw.version, "")
        self.assertEqual(sw.publisher, "")
        self.assertEqual(sw.install_date, "")


class TestRegistryScanner(unittest.TestCase):
    """Тесты для класса RegistryScanner"""
    
    def test_scanner_creation(self):
        """Тест создания сканера"""
        scanner = RegistryScanner()
        self.assertIsNotNone(scanner)
        self.assertTrue(scanner.include_32bit)
    
    def test_scanner_without_32bit(self):
        """Тест создания сканера без 32-бит"""
        scanner = RegistryScanner(include_32bit=False)
        self.assertFalse(scanner.include_32bit)
    
    def test_scan_returns_list(self):
        """Тест что scan возвращает список"""
        scanner = RegistryScanner()
        result = scanner.scan()
        self.assertIsInstance(result, list)
    
    def test_read_software_from_invalid_key(self):
        """Тест чтения из несуществующего ключа"""
        scanner = RegistryScanner()
        result = scanner.read_software_from_key(
            "HKEY_LOCAL_MACHINE", 
            "INVALID_KEY", 
            "test"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
