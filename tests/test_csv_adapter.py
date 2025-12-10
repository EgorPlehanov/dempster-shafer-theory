import unittest
import os
import sys
import csv
from pathlib import Path

# Добавляем путь к родительской директории
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_adapters import CsvAdapter

class TestCsvAdapter(unittest.TestCase):
    """Тесты для CsvAdapter"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.adapter = CsvAdapter()
        self.test_data_dir = Path(__file__).parent.parent / "data"
        
    def test_load_valid_csv(self):
        """Тест загрузки валидного CSV файла"""
        filepath = self.test_data_dir / "example_2_1.csv"
        # Преобразуем Path в строку
        data = self.adapter.load(str(filepath))
        
        self.assertIsInstance(data, dict)
        self.assertIn('frame_of_discernment', data)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 3)
    
    def test_transform_to_bpa(self):
        """Тест преобразования CSV данных в BPA"""
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
    
    def test_extract_frame_from_data(self):
        """Тест извлечения фрейма различений из данных"""
        csv_content = """subset,count
"{1}",5
"{1,2}",3
"{3}",2"""
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            data = self.adapter.load(temp_path)  # temp_path уже строка
            
            # Проверяем что фрейм извлечен корректно
            frame = data['frame_of_discernment']
            self.assertIn('1', frame)
            self.assertIn('2', frame)
            self.assertIn('3', frame)
            self.assertEqual(len(frame), 3)
            
        finally:
            os.unlink(temp_path)
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки CSV"""
        import tempfile
        
        test_data = {
            'data': {
                '{A}': 10,
                '{B}': 20,
                '{A,B}': 5
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            # Сохраняем данные
            self.adapter.save(test_data, temp_path)
            
            # Проверяем что файл создан
            self.assertTrue(os.path.exists(temp_path))
            
            # Проверяем содержимое файла
            with open(temp_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                self.assertEqual(rows[0], ['subset', 'count'])
                self.assertEqual(len(rows), 4)  # заголовок + 3 строки данных
                
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

if __name__ == '__main__':
    unittest.main()