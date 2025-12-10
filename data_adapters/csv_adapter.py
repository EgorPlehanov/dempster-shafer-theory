import csv
from typing import Dict, Any, List
from .base_adapter import BaseDataAdapter

class CsvAdapter(BaseDataAdapter):
    """Адаптер для загрузки и сохранения данных в CSV формате"""
    
    def load(self, filepath: str) -> Dict[str, Any]:
        """
        Загрузка данных из CSV файла
        
        Args:
            filepath: Путь к CSV файлу
            
        Returns:
            Dict[str, Any]: Загруженные данные
        """
        try:
            data = {'frame_of_discernment': [], 'data': {}}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    if 'subset' not in row or 'count' not in row:
                        raise ValueError("CSV файл должен содержать колонки 'subset' и 'count'")
                    
                    subset = row['subset']
                    try:
                        count = float(row['count'])
                    except ValueError:
                        raise ValueError(f"Некорректное значение count для subset {subset}")
                    
                    data['data'][subset] = count
            
            # Извлекаем frame_of_discernment из данных
            all_elements = set()
            for subset_str in data['data'].keys():
                # Убираем фигурные скобки и разбиваем по запятым
                elements = subset_str.strip("{}").split(",")
                elements = [e.strip() for e in elements if e.strip()]
                all_elements.update(elements)
            
            data['frame_of_discernment'] = list(all_elements)
            
            return data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    def transform_to_bpa(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Преобразование данных из CSV формата в BPA
        
        Args:
            data: Данные в формате CSV
            
        Returns:
            Dict[str, float]: Базовые вероятностные назначения
        """
        if 'data' not in data or not data['data']:
            raise ValueError("Отсутствуют данные в CSV")
        
        # Нормализация базовых вероятностей
        bpa_data = data['data']
        total = sum(bpa_data.values())
        
        if total == 0:
            raise ValueError("Сумма базовых вероятностей равна 0")
        
        # Нормализация до суммы 1
        normalized_bpa = {k: v/total for k, v in bpa_data.items()}
        return normalized_bpa
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Валидация CSV данных
        
        Args:
            data: Данные для валидации
            
        Returns:
            bool: True если данные валидны
        """
        if 'data' not in data:
            return False
        
        if not data['data']:
            return False
        
        # Проверка что все значения числовые
        for value in data['data'].values():
            if not isinstance(value, (int, float)):
                return False
        
        return True
    
    def save(self, data: Dict[str, Any], filepath: str):
        """
        Сохранение данных в CSV файл
        
        Args:
            data: Данные для сохранения
            filepath: Путь для сохранения файла
        """
        if 'data' not in data:
            raise ValueError("Отсутствует ключ 'data' для сохранения в CSV")
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['subset', 'count'])
            
            for subset, count in data['data'].items():
                writer.writerow([subset, count])