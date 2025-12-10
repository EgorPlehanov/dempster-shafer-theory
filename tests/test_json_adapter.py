import unittest
import os
import sys
import json
from pathlib import Path

# Добавляем путь к родительской директории
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_adapters import JsonAdapter

class TestJsonAdapter(unittest.TestCase):
    """Тесты для JsonAdapter"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.adapter = JsonAdapter()
        self.test_data_dir = Path(__file__).parent.parent / "data"
        
    def test_load_valid_json(self):
        """Тест загрузки валидного JSON файла"""
        filepath = self.test_data_dir / "example_2_1.json"
        # Преобразуем Path в строку
        data = self.adapter.load(str(filepath))
        
        self.assertIsInstance(data, dict)
        self.assertIn('frame_of_discernment', data)
        self.assertIn('data', data)
        self.assertIn('parameters', data)
        
    def test_load_invalid_json(self):
        """Тест загрузки невалидного JSON файла"""
        # Создаем временный невалидный JSON
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.adapter.load(temp_path)  # temp_path уже строка
        finally:
            os.unlink(temp_path)
    
    def test_transform_to_bpa(self):
        """Тест преобразования данных в BPA"""
        test_data = {
            'frame_of_discernment': ['1', '2', '3'],
            'data': {
                '{1}': 5,
                '{2}': 3,
                '{3}': 2
            }
        }
        
        bpa = self.adapter.transform_to_bpa(test_data)
        
        self.assertIsInstance(bpa, dict)
        self.assertEqual(len(bpa), 3)
        self.assertAlmostEqual(sum(bpa.values()), 1.0, places=6)
    
    def test_validate_valid_data(self):
        """Тест валидации валидных данных"""
        valid_data = {
            'frame_of_discernment': ['1', '2', '3'],
            'data': {
                '{1}': 5.0,
                '{2}': 3.0
            }
        }
        
        self.assertTrue(self.adapter.validate(valid_data))
    
    def test_validate_invalid_data(self):
        """Тест валидации невалидных данных"""
        invalid_data = {
            'frame_of_discernment': ['1', '2'],
            # Отсутствует ключ 'data'
        }
        
        self.assertFalse(self.adapter.validate(invalid_data))
    
    def test_save_and_load(self):
        """Тест сохранения и последующей загрузки данных"""
        import tempfile
        
        test_data = {
            'frame_of_discernment': ['A', 'B', 'C'],
            'data': {
                '{A}': 10,
                '{B}': 20,
                '{A,B}': 5
            },
            'parameters': {
                'method': 'test'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # Сохраняем данные (преобразуем путь в строку)
            self.adapter.save(test_data, temp_path)
            
            # Загружаем данные (преобразуем путь в строку)
            loaded_data = self.adapter.load(temp_path)
            
            # Проверяем что данные совпадают
            self.assertEqual(test_data['frame_of_discernment'], 
                           loaded_data['frame_of_discernment'])
            self.assertEqual(test_data['data'], loaded_data['data'])
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

if __name__ == '__main__':
    unittest.main()