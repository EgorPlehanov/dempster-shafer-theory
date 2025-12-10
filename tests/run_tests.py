#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов проекта
"""

import unittest
import sys
from pathlib import Path

def run_all_tests():
    """Запуск всех тестов"""
    # Добавляем путь к проекту
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Определяем директорию с тестами
    test_dir = project_root / "tests"
    
    # Загружаем все тесты
    loader = unittest.TestLoader()
    suite = loader.discover(str(test_dir), pattern="test_*.py")
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем результат
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)