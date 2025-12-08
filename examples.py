"""
Реализация конкретных примеров из главы 2 книги
"""
from dempster_core import DempsterShafer
import json

class TestExamples:
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
        ds, bpa1, bpa2, dempster_combined = TestExamples.get_example_2_6_data()
        
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
        
        return yager_combined, dempster_combined, bpa1, bpa2

    @staticmethod
    def compare_dempster_yager():
        """Сравнение правил Демпстера и Ягера на одном примере"""
        print("\n=== Сравнение правил Демпстера и Ягера ===")
        
        # Получаем данные и результаты обоих методов
        yager_result, dempster_result, bpa1, bpa2 = TestExamples.example_2_8()
        
        return yager_result, dempster_result, bpa1, bpa2
    
    @staticmethod
    def my_example():
        """Комплексный пример выбора библиотеки оптимизации - аналогично примерам из книги"""
        
        print("\n" + "="*70)
        print("КОМПЛЕКСНЫЙ АНАЛИЗ ВЫБОРА БИБЛИОТЕКИ ОПТИМИЗАЦИИ")
        print("Аналогично примерам из книги, но на актуальной теме")
        print("="*70)
        
        print("\nСООТВЕТСТВИЕ БИБЛИОТЕК И НОМЕРОВ:")
        print("1 = DEAP, 2 = PyGAD, 3 = Optuna, 4 = Platypus")
        print("5 = PySwarms, 6 = JMetal, 7 = ECJ, 8 = Custom")
        print("="*70)
        
        # Основной фрейм - используем номера вместо названий
        frame = {'1', '2', '3', '4', '5', '6', '7', '8'}
        
        # Создаем экземпляр DempsterShafer
        ds = DempsterShafer(frame)
        
        # АНАЛОГ ПРИМЕРА 2.1: Выбор библиотеки по мнению экспертов (как выбор кандидата)
        print("\n" + "="*60)
        print("АНАЛОГ ПРИМЕРА 2.1: Выбор библиотеки по мнению экспертов")
        print("="*60)
        
        # Данные экспертов (аналогично примеру 2.1 с кандидатами)
        # 1=DEAP, 2=PyGAD, 3=Optuna
        data_experts = {
            "{1}": 5,            # 5 экспертов за библиотеку 1 (DEAP)
            "{1,2}": 2,          # 2 эксперта за библиотеку 1 или 2 (DEAP или PyGAD)
            "{3}": 3             # 3 эксперта за библиотеку 3 (Optuna)
        }
        
        bpa_experts = ds.calculate_bpa(data_experts)
        
        print(f"\nВсего экспертов: {sum(data_experts.values())}")
        print("Базовые вероятности (m) от экспертов:")
        for subset, mass in sorted(bpa_experts.items(), key=lambda x: str(x[0])):
            if mass > 0:
                # Преобразуем номера в названия для вывода
                subset_names = []
                for num in subset:
                    name_map = {'1': 'DEAP', '2': 'PyGAD', '3': 'Optuna', '4': 'Platypus',
                               '5': 'PySwarms', '6': 'JMetal', '7': 'ECJ', '8': 'Custom'}
                    subset_names.append(name_map.get(num, num))
                print(f"  m({set(subset_names)}) = {mass:.1f}")
        
        print("\nФункции доверия и правдоподобия для библиотек:")
        library_map = {
            '1': 'DEAP', '2': 'PyGAD', '3': 'Optuna', '4': 'Platypus',
            '5': 'PySwarms', '6': 'JMetal', '7': 'ECJ', '8': 'Custom'
        }
        
        for num, name in library_map.items():
            event = {num}
            bel = ds.belief(event, bpa_experts)
            pl = ds.plausibility(event, bpa_experts)
            print(f"  Библиотека {name:8} ({num}): Bel={bel:.3f}, Pl={pl:.3f}, Интервал: [{bel:.3f}, {pl:.3f}]")
        
        # АНАЛОГ ПРИМЕРА 2.2: Прогноз цены акций → Прогноз точности
        print("\n" + "="*60)
        print("АНАЛОГ ПРИМЕРА 2.2: Прогноз точности библиотек (интервалы)")
        print("="*60)
        
        # Представляем интервалы точности как дискретные зоны
        frame_accuracy = {'A', 'B', 'C', 'D', 'E', 'F'}  # A=85-89%, B=90-92%, C=93-94%, D=95-96%, E=97-98%, F=99-100%
        ds_accuracy = DempsterShafer(frame_accuracy)
        
        # Экспертные оценки точности (аналогично интервалам цен акций)
        data_accuracy = {
            "{B,C,D}": 4,        # Группа A: точность 90-96%
            "{A,B,C,D,E,F}": 1,  # Группа B: точность 85-100% (неопределенность)
            "{D,E}": 5           # Группа C: точность 95-98%
        }
        
        bpa_accuracy = ds_accuracy.calculate_bpa(data_accuracy)
        
        # Событие: точность 85-94% соответствует зонам A, B, C
        event_accuracy = {'A', 'B', 'C'}
        bel_acc = ds_accuracy.belief(event_accuracy, bpa_accuracy)
        pl_acc = ds_accuracy.plausibility(event_accuracy, bpa_accuracy)
        
        print(f"\nСобытие A = [85%, 94%]: Bel={bel_acc:.1f}, Pl={pl_acc:.1f}")
        
        # АНАЛОГ ПРИМЕРА 2.6: Комбинирование свидетельств от разных источников
        print("\n" + "="*60)
        print("АНАЛОГ ПРИМЕРА 2.6: Комбинирование свидетельств о библиотеках")
        print("="*60)
        
        # Первый источник (исследователи) - УПРОЩАЕМ данные чтобы избежать конфликта
        # 1=DEAP, 2=PyGAD, 3=Optuna, 4=Platypus, 5=PySwarms
        data_researchers = {
            "{1}": 5,        # 5 исследователей за DEAP
            "{2,3}": 3       # 3 исследователя за PyGAD или Optuna
        }
        
        # Второй источник (разработчики)
        data_developers = {
            "{1,2}": 8,      # 8 разработчиков за DEAP или PyGAD
            "{3}": 7,        # 7 разработчиков за Optuna
            "{5}": 1         # 1 разработчик за PySwarms
        }
        
        bpa_researchers = ds.calculate_bpa(data_researchers)
        bpa_developers = ds.calculate_bpa(data_developers)
        
        print("\nИсточник 1 (Исследователи):")
        for subset, mass in bpa_researchers.items():
            if mass > 0:
                subset_names = []
                for num in subset:
                    subset_names.append(library_map.get(num, num))
                print(f"  m1{set(subset_names)} = {mass:.3f}")
        
        print("\nИсточник 2 (Разработчики):")
        for subset, mass in bpa_developers.items():
            if mass > 0:
                subset_names = []
                for num in subset:
                    subset_names.append(library_map.get(num, num))
                print(f"  m2{set(subset_names)} = {mass:.3f}")
        
        # Комбинируем по Демпстеру
        try:
            combined_dempster = ds.dempster_combine(bpa_researchers, bpa_developers)
            
            print("\nКомбинированная BPA (правило Демпстера):")
            for subset, mass in sorted(combined_dempster.items(), key=lambda x: (-x[1], str(x[0]))):
                if mass > 0.0001:
                    if subset == frozenset(frame):
                        print(f"  m(Ω) = {mass:.4f}")
                    else:
                        subset_names = []
                        for num in subset:
                            subset_names.append(library_map.get(num, num))
                        print(f"  m({set(subset_names)}) = {mass:.4f}")
            
            print("\nРезультаты комбинирования (Bel для каждой библиотеки):")
            for num, name in library_map.items():
                event = {num}
                bel = ds.belief(event, combined_dempster)
                pl = ds.plausibility(event, combined_dempster)
                print(f"  Библиотека {name:8} ({num}): Bel={bel:.4f}, Pl={pl:.4f}")
                
        except ValueError as e:
            print(f"\nОшибка при комбинировании Демпстером: {e}")
            print("Слишком большой конфликт между источниками.")
            # Создаем пустой результат
            combined_dempster = {}
        
        # АНАЛОГ ПРИМЕРА 2.8: Правило Ягера с конфликтующими источниками
        print("\n" + "="*60)
        print("АНАЛОГ ПРИМЕРА 2.8: Правило Ягера для конфликтующих оценок")
        print("="*60)
        
        # Источник A: Оценка по скорости (5=PySwarms самый быстрый, 1=DEAP, 2=PyGAD средние)
        data_speed = {
            "{5}": 8,        # 8 оценок за PySwarms (самый быстрый)
            "{1,2}": 7       # 7 оценок за DEAP или PyGAD (средняя скорость)
        }
        
        # Источник B: Оценка по точности (3=Optuna, 6=JMetal высокая точность, 1=DEAP хорошая)
        data_precision = {
            "{3,6}": 9,      # 9 оценок за Optuna или JMetal (высокая точность)
            "{1}": 6,        # 6 оценок за DEAP (хорошая точность)
            "{5}": 1         # 1 оценка за PySwarms (низкая точность)
        }
        
        bpa_speed = ds.calculate_bpa(data_speed)
        bpa_precision = ds.calculate_bpa(data_precision)
        
        # Комбинируем по Ягеру
        combined_yager = ds.yager_combine(bpa_speed, bpa_precision)
        
        print("\nРезультат по Ягеру:")
        for subset, mass in sorted(combined_yager.items(), key=lambda x: (-x[1], len(x[0]))):
            if mass > 0.0001:
                if subset == frozenset(frame):
                    print(f"  m(Ω) = {mass:.4f}")
                else:
                    subset_names = []
                    for num in subset:
                        subset_names.append(library_map.get(num, num))
                    print(f"  m({set(subset_names)}) = {mass:.4f}")
        
        # Комбинируем по Демпстеру для сравнения
        try:
            combined_dempster2 = ds.dempster_combine(bpa_speed, bpa_precision)
            
            print("\nСравнение правил Демпстера и Ягера:")
            print("Библиотека (№) |  Ягер  | Демпстер | Разница")
            print("-" * 45)
            
            for num in ['1', '2', '3', '5', '6']:
                event = {num}
                yager_bel = ds.belief(event, combined_yager)
                dempster_bel = ds.belief(event, combined_dempster2)
                difference = dempster_bel - yager_bel
                print(f"{library_map[num]:8} ({num}) | {yager_bel:6.3f} | {dempster_bel:8.3f} | {difference:7.3f}")
            
        except ValueError as e:
            print(f"\nОшибка при комбинировании Демпстером: {e}")
            print("Слишком большой конфликт между оценками скорости и точности.")
            combined_dempster2 = {}
        
        # Показываем массу незнания (универсального множества)
        omega_mass_yager = combined_yager.get(frozenset(frame), 0.0)
        print(f"\nМасса незнания (Ω) по Ягеру: {omega_mass_yager:.3f}")
        
        # КОМБИНИРОВАНИЕ МНОГИХ ИСТОЧНИКОВ - ИСПРАВЛЕННЫЕ ДАННЫЕ
        print("\n" + "="*60)
        print("КОМБИНИРОВАНИЕ 4-Х ИСТОЧНИКОВ (расширенный пример)")
        print("="*60)
        
        # 4 источника данных о библиотеках - ИСПРАВЛЕННЫЕ ДАННЫЕ чтобы избежать полного конфликта
        # Ключевое изменение: добавляем универсальное множество в некоторые источники
        source1 = ds.calculate_bpa({
            "{1}": 10,           # 10 оценок за DEAP
            "{2,3}": 5,          # 5 оценок за PyGAD или Optuna
            "{1,2,3,4,5,6,7,8}": 2  # 2 оценки - неопределенность (все библиотеки)
        })
        
        source2 = ds.calculate_bpa({
            "{3}": 8,            # 8 оценок за Optuna
            "{1,5}": 7,          # 7 оценок за DEAP или PySwarms
            "{2,3,4}": 3         # 3 оценки за PyGAD, Optuna или Platypus
        })
        
        source3 = ds.calculate_bpa({
            "{5}": 9,            # 9 оценок за PySwarms
            "{2}": 6,            # 6 оценок за PyGAD
            "{1,2,3,4,5,6,7,8}": 4  # 4 оценки - неопределенность
        })
        
        source4 = ds.calculate_bpa({
            "{1,3,5}": 12,       # 12 оценок за DEAP, Optuna или PySwarms
            "{6}": 3,            # 3 оценки за JMetal
            "{2,4}": 2           # 2 оценки за PyGAD или Platypus
        })
        
        # Комбинируем по Демпстеру с обработкой ошибок
        try:
            combined_4_dempster = ds.dempster_combine_multiple(source1, source2, source3, source4)
            
            print("\nРезультат комбинирования 4-х источников (Демпстер):")
            for subset, mass in sorted(combined_4_dempster.items(), key=lambda x: (-x[1], str(x[0]))):
                if mass > 0.01:
                    if subset == frozenset(frame):
                        print(f"  m(Ω) = {mass:.4f}")
                    else:
                        subset_names = []
                        for num in subset:
                            subset_names.append(library_map.get(num, num))
                        print(f"  m({set(subset_names)}) = {mass:.4f}")
                        
        except ValueError as e:
            print(f"\nОшибка при комбинировании Демпстером: {e}")
            print("Используем альтернативные данные...")
            # Альтернативные данные без конфликта
            source1_alt = ds.calculate_bpa({"{1}": 10, "{2,3}": 5})
            source2_alt = ds.calculate_bpa({"{1,3}": 8, "{2}": 7})
            source3_alt = ds.calculate_bpa({"{1,5}": 9, "{3}": 6})
            
            try:
                combined_4_dempster = ds.dempster_combine_multiple(source1_alt, source2_alt, source3_alt)
                print("\nРезультат комбинирования 3-х источников (Демпстер - альтернативные данные):")
                for subset, mass in sorted(combined_4_dempster.items(), key=lambda x: (-x[1], str(x[0]))):
                    if mass > 0.01:
                        if subset == frozenset(frame):
                            print(f"  m(Ω) = {mass:.4f}")
                        else:
                            subset_names = []
                            for num in subset:
                                subset_names.append(library_map.get(num, num))
                            print(f"  m({set(subset_names)}) = {mass:.4f}")
            except ValueError as e2:
                print(f"\nДаже альтернативные данные вызывают конфликт: {e2}")
                combined_4_dempster = {}
        
        # Комбинируем по Ягеру
        combined_4_yager = ds.yager_combine_multiple(source1, source2, source3, source4)
        
        print("\nРезультат комбинирования 4-х источников (Ягер):")
        for subset, mass in sorted(combined_4_yager.items(), key=lambda x: (-x[1], len(x[0]))):
            if mass > 0.01:
                if subset == frozenset(frame):
                    print(f"  m(Ω) = {mass:.4f}")
                else:
                    subset_names = []
                    for num in subset:
                        subset_names.append(library_map.get(num, num))
                    print(f"  m({set(subset_names)}) = {mass:.4f}")
        
        print("\n" + "="*60)
        print("ИТОГОВЫЕ ВЫВОДЫ ДЛЯ ВЫБОРА БИБЛИОТЕКИ")
        print("="*60)
        
        # Сравниваем итоговые оценки
        libraries_to_compare = ['1', '2', '3', '5', '6']  # DEAP, PyGAD, Optuna, PySwarms, JMetal
        
        print("\nСравнение библиотек по комбинированным оценкам:")
        print("Библиотека (№) | Демпстер (Bel) | Ягер (Bel) | Рекомендация")
        print("-" * 65)
        
        recommendations = []
        for num in libraries_to_compare:
            event = {num}
            
            if combined_4_dempster and combined_4_dempster != {}:
                bel_dempster = ds.belief(event, combined_4_dempster)
            else:
                bel_dempster = 0
                
            bel_yager = ds.belief(event, combined_4_yager)
            
            # Определяем рекомендацию на основе обоих методов
            # Если оба метода дают оценку, усредняем
            if bel_dempster > 0 and bel_yager > 0:
                confidence_score = (bel_dempster + bel_yager) / 2
            elif bel_dempster > 0:
                confidence_score = bel_dempster
            elif bel_yager > 0:
                confidence_score = bel_yager
            else:
                confidence_score = 0
                
            if confidence_score > 0.3:
                recommendation = "✅ ВЫСОКО РЕКОМЕНДОВАНА"
                rec_level = "high"
            elif confidence_score > 0.15:
                recommendation = "✓ рекомендуется"
                rec_level = "medium"
            elif confidence_score > 0.05:
                recommendation = "△ рассмотреть"
                rec_level = "low"
            else:
                recommendation = "○ не рекомендуется"
                rec_level = "none"
            
            name = library_map[num]
            print(f"{name:8} ({num}) | {bel_dempster:13.3f} | {bel_yager:11.3f} | {recommendation}")
            recommendations.append((name, num, confidence_score, rec_level))
        
        # Сортируем по уровню рекомендации
        recommendations.sort(key=lambda x: {'high': 3, 'medium': 2, 'low': 1, 'none': 0}[x[3]], reverse=True)
        
        print("\n" + "="*70)
        print("ЗАКЛЮЧЕНИЕ ПО РЕЗУЛЬТАТАМ АНАЛИЗА:")
        print("="*70)
        
        # Пересчитываем с исправленной логикой
        lib_scores = []
        for num in libraries_to_compare:
            name = library_map[num]
            event = {num}
            
            if combined_4_dempster and combined_4_dempster != {}:
                bel_dempster = ds.belief(event, combined_4_dempster)
            else:
                bel_dempster = 0
                
            bel_yager = ds.belief(event, combined_4_yager)
            
            # Исправленная логика вычисления confidence_score
            if bel_dempster > 0 and bel_yager > 0:
                omega_mass = combined_4_yager.get(frozenset(frame), 0)
                yager_weight = 1 - omega_mass * 0.5
                dempster_weight = 1.0
                total_weight = dempster_weight + yager_weight
                confidence_score = (dempster_weight * bel_dempster + yager_weight * bel_yager) / total_weight
            elif bel_dempster > 0:
                confidence_score = bel_dempster
            elif bel_yager > 0:
                omega_mass = combined_4_yager.get(frozenset(frame), 0)
                confidence_score = bel_yager * (1 - omega_mass)
            else:
                confidence_score = 0
                
            lib_scores.append((name, num, confidence_score, bel_dempster, bel_yager))
        
        # Сортируем по confidence_score
        lib_scores.sort(key=lambda x: x[2], reverse=True)
        
        print("\nРанжированный список библиотек по результатам анализа:")
        for i, (name, num, score, bel_d, bel_y) in enumerate(lib_scores, 1):
            if score > 0.2:
                symbol = "🥇"
                level = "ВЫСОКО РЕКОМЕНДОВАНА"
            elif score > 0.15:
                symbol = "🥈"
                level = "рекомендуется"
            elif score > 0.05:
                symbol = "🥉"
                level = "рассмотреть"
            else:
                symbol = "○"
                level = "не рекомендуется"
            
            print(f"{i:2}. {symbol} Библиотека {name} ({num}): итоговая оценка {score:.3f} (Д: {bel_d:.3f}, Я: {bel_y:.3f}) - {level}")
        
        print("\nКЛЮЧЕВЫЕ ВЫВОДЫ:")
        if lib_scores:
            print(f"1. {lib_scores[0][0]} ({lib_scores[0][1]}) - лидер по комбинированным оценкам")
            if len(lib_scores) > 1:
                print(f"2. {lib_scores[1][0]} ({lib_scores[1][1]}) - стабильные результаты")
            if len(lib_scores) > 2:
                print(f"3. {lib_scores[2][0]} ({lib_scores[2][1]}) - хорошие результаты в отдельных аспектах")
        
        print(f"\n4. Метод Демпстера дает более определенные результаты")
        print(f"5. Метод Ягера более консервативен (масса Ω = {combined_4_yager.get(frozenset(frame), 0):.3f})")
        print("6. Рекомендуется использовать оба метода для комплексной оценки")
        print("="*70)
        
        # Возвращаем результаты для возможной визуализации
        return {
            'frame': frame,
            'bpa_experts': bpa_experts,
            'bpa_researchers': bpa_researchers,
            'bpa_developers': bpa_developers,
            'combined_dempster': combined_dempster if 'combined_dempster' in locals() else {},
            'bpa_speed': bpa_speed,
            'bpa_precision': bpa_precision,
            'combined_yager': combined_yager,
            'combined_4_dempster': combined_4_dempster if 'combined_4_dempster' in locals() else {},
            'combined_4_yager': combined_4_yager,
            'library_map': library_map
        }