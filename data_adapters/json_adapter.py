import json
from typing import Dict, Any
from .base_adapter import BaseDataAdapter

class JsonAdapter(BaseDataAdapter):
    """Адаптер для загрузки и сохранения данных в JSON формате"""
    
    def load(self, filepath: str) -> Dict[str, Any]:
        """
        Загрузка данных из JSON файла
        
        Args:
            filepath: Путь к JSON файлу
            
        Returns:
            Dict[str, Any]: Загруженные данные
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")
    
    def transform_to_bpa(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Преобразование данных из JSON формата в BPA
        
        Args:
            data: Данные в формате JSON
            
        Returns:
            Dict[str, float]: Базовые вероятностные назначения
        """
        if 'data' not in data:
            raise ValueError("Отсутствует ключ 'data' в JSON")
        
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
        Валидация JSON данных
        
        Args:
            data: Данные для валидации
            
        Returns:
            bool: True если данные валидны
        """
        required_fields = ['frame_of_discernment', 'data']
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Проверка что data - словарь
        if not isinstance(data['data'], dict):
            return False
        
        # Проверка что все значения числовые
        for value in data['data'].values():
            if not isinstance(value, (int, float)):
                return False
        
        return True
    
    def save(self, data: Dict[str, Any], filepath: str):
        """
        Сохранение данных в JSON файл
        
        Args:
            data: Данные для сохранения
            filepath: Путь для сохранения файла
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)