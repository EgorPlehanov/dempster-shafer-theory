from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

class BaseDataAdapter(ABC):
    """Абстрактный базовый класс для адаптеров данных"""
    
    @abstractmethod
    def load(self, filepath: str) -> Dict[str, Any]:
        """Загрузка данных из файла"""
        pass
    
    @abstractmethod
    def transform_to_bpa(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Преобразование данных в формат BPA (базовая вероятностная функция)"""
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """Валидация входных данных"""
        pass
    
    @abstractmethod
    def save(self, data: Dict[str, Any], filepath: str):
        """Сохранение данных в файл"""
        pass