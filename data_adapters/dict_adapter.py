from typing import Dict, Any, Optional
from .base_adapter import BaseDataAdapter

class DictAdapter(BaseDataAdapter):
    """Адаптер для работы с данными в формате Python словаря"""
    
    def load(self, filepath: str) -> Dict[str, Any]:
        """
        Загрузка данных из словаря (для совместимости с API)
        
        Args:
            filepath: Путь к файлу (не используется для этого адаптера,
                     но требуется для совместимости с API)
            
        Returns:
            Dict[str, Any]: Пустой словарь, так как для DictAdapter
                           данные передаются напрямую
        """
        # Для DictAdapter filepath не используется
        # Возвращаем пустой словарь для совместимости
        return {}
    
    def transform_to_bpa(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Преобразование данных из словаря в BPA
        
        Args:
            data: Данные в формате словаря
            
        Returns:
            Dict[str, float]: Базовые вероятностные назначения
        """
        if 'data' not in data:
            raise ValueError("Отсутствует ключ 'data' в словаре")
        
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
        Валидация данных в словаре
        
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
    
    def save(self, data: Dict[str, Any], filepath: Optional[str] = None):
        """
        Сохранение данных (не реализовано для словаря)
        
        Args:
            data: Данные для сохранения
            filepath: Не используется для этого адаптера,
                     но требуется для совместимости с API
        """
        # Для словаря сохранение в файл не требуется
        # Метод существует только для совместимости с API
        if filepath:
            # Можно добавить логирование или сохранение в JSON для отладки
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)