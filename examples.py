"""
Реализация конкретных примеров из главы 2 книги
"""
from dempster_core import DempsterShafer
import json

class BookExamples:
    """Реализация примеров из книги"""
    
    @staticmethod
    def example_2_1():
        """Пример 2.1 - Кандидаты на должность"""
        print("=== Пример 2.1: Кандидаты на должность ===")
        
        frame = {'1', '2', '3', '4'}
        ds = DempsterShafer(frame)
        
        # Данные экспертов
        data = {
            "{1}": 5,    # 5 экспертов за кандидата 1
            "{1,2}": 2,  # 2 эксперта за кандидатов 1 или 2  
            "{3}": 3     # 3 эксперта за кандидата 3
        }
        
        bpa = ds.calculate_bpa(data)
        print("Базовые вероятности (m):")
        for subset, mass in bpa.items():
            print(f"  m{set(subset)} = {mass:.1f}")
        
        # Расчет для каждого кандидата
        print("\nВероятности кандидатов:")
        for candidate in ['1', '2', '3', '4']:
            event = {candidate}
            bel = ds.belief(event, bpa)
            pl = ds.plausibility(event, bpa)
            print(f"  Кандидат {candidate}: Bel={bel:.1f}, Pl={pl:.1f}, Интервал: [{bel:.1f}, {pl:.1f}]")
        
        return bpa
    
    @staticmethod
    def example_2_2():
        """Пример 2.2 - Цены акций (интервалы)"""
        print("\n=== Пример 2.2: Прогноз цен акций ===")
        
        # Представляем интервалы как дискретные зоны
        frame = {'28-30', '30-32', '32-34', '34-36', '36-38', '38-40'}
        ds = DempsterShafer(frame)
        
        # Экспертные интервалы
        data = {
            "{30-32,32-34,34-36}": 4,  # A1 = [30,36]
            "{28-30,30-32,32-34,34-36,36-38,38-40}": 1,  # A2 = [28,40]  
            "{34-36,36-38}": 5         # A3 = [34,38]
        }
        
        bpa = ds.calculate_bpa(data)
        
        # Событие A = [28,32] соответствует зонам 28-30 и 30-32
        event = {'28-30', '30-32'}
        bel = ds.belief(event, bpa)
        pl = ds.plausibility(event, bpa)
        
        print(f"Событие A = [28,32]: Bel={bel:.1f}, Pl={pl:.1f}")
        return bpa
    
    @staticmethod
    def example_2_6():
        """Пример 2.6 - Комбинирование свидетельств"""
        print("\n=== Пример 2.6: Комбинирование свидетельств ===")
        
        frame = {'1', '2', '3', '4'}
        ds = DempsterShafer(frame)
        
        # Первый источник
        data1 = {
            "{1}": 5,
            "{2,3}": 3
        }
        
        # Второй источник  
        data2 = {
            "{1,2}": 8,
            "{3}": 7,
            "{4}": 1
        }
        
        bpa1 = ds.calculate_bpa(data1)
        bpa2 = ds.calculate_bpa(data2)
        
        print("Источник 1:")
        for subset, mass in bpa1.items():
            print(f"  m1{set(subset)} = {mass:.3f}")
            
        print("Источник 2:")
        for subset, mass in bpa2.items():
            print(f"  m2{set(subset)} = {mass:.3f}")
        
        # Комбинируем
        combined = ds.dempster_combine(bpa1, bpa2)
        
        print("\nКомбинированная BPA:")
        for subset, mass in combined.items():
            if mass > 0:
                print(f"  m12{set(subset)} = {mass:.4f}")
        
        # Функции доверия и правдоподобия
        print("\nРезультаты комбинирования:")
        for candidate in ['1', '2', '3', '4']:
            event = {candidate}
            bel = ds.belief(event, combined)
            pl = ds.plausibility(event, combined)
            print(f"  Предприятие {candidate}: Bel={bel:.4f}, Pl={pl:.4f}")
        
        return combined
    
    @staticmethod
    def get_example_2_6_data():
        """Возвращает данные примера 2.6 для использования в сравнении"""
        frame = {'1', '2', '3', '4'}
        ds = DempsterShafer(frame)
        
        # Данные из примера 2.6
        data1 = {"{1}": 5, "{2,3}": 3}
        data2 = {"{1,2}": 8, "{3}": 7, "{4}": 1}
        
        bpa1 = ds.calculate_bpa(data1)
        bpa2 = ds.calculate_bpa(data2)
        dempster_combined = ds.dempster_combine(bpa1, bpa2)
        
        return ds, bpa1, bpa2, dempster_combined

    @staticmethod
    def example_2_8():
        """Пример 2.8 - Правило Ягера"""
        print("\n=== Пример 2.8: Правило комбинирования Ягера ===")
        
        # Используем те же данные, что и в примере 2.6
        ds, bpa1, bpa2, dempster_combined = BookExamples.get_example_2_6_data()
        
        # Комбинируем по Ягеру
        yager_combined = ds.yager_combine(bpa1, bpa2)
        
        print("Результат по Ягеру:")
        for subset, mass in sorted(yager_combined.items(), key=lambda x: (-x[1], len(x[0]))):
            if mass > 0.0001:  # Показываем только значимые значения
                subset_str = "Ω" if subset == frozenset(ds.frame) else str(set(subset))
                print(f"  m({subset_str}) = {mass:.4f}")
        
        # Сравнение с Демпстером
        print("\nСравнение с правилом Демпстера:")
        print("Элемент |  Ягер  | Демпстер | Разница")
        print("-" * 40)
        
        for element in sorted(ds.frame):
            event = {element}
            yager_bel = ds.belief(event, yager_combined)
            dempster_bel = ds.belief(event, dempster_combined)
            difference = dempster_bel - yager_bel
            print(f"{element:7} | {yager_bel:6.3f} | {dempster_bel:8.3f} | {difference:7.3f}")
        
        # Показываем массу незнания (универсального множества)
        omega_mass_yager = yager_combined.get(frozenset(ds.frame), 0.0)
        print(f"\nМасса незнания (Ω) по Ягеру: {omega_mass_yager:.3f}")
        print(f"Коэффициент конфликта: {1 - omega_mass_yager - yager_combined.get(frozenset(), 0.0):.3f}")
        
        return yager_combined, dempster_combined, bpa1, bpa2

    @staticmethod
    def compare_dempster_yager():
        """Сравнение правил Демпстера и Ягера на одном примере"""
        print("\n=== Сравнение правил Демпстера и Ягера ===")
        
        # Получаем данные и результаты обоих методов
        yager_result, dempster_result, bpa1, bpa2 = BookExamples.example_2_8()
        
        return yager_result, dempster_result, bpa1, bpa2