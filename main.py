"""
Главный файл консольного приложения
"""
from examples import TestExamples
from visualizer import DSVisualizer

def main():
    print("Теория Демпстера-Шейфера - реализация примеров из книги")
    print("=" * 50)
    
    while True:
        print("\nВыберите пример для запуска:")
        print("1. Пример 2.1 - Кандидаты на должность")
        print("2. Пример 2.2 - Прогноз цен акций") 
        print("3. Пример 2.6 - Комбинирование свидетельств (Демпстер)")
        print("4. Пример 2.8 - Правило комбинирования Ягера")
        print("5. Сравнение Демпстера и Ягера")
        print("6. Все примеры последовательно")
        print("7. Пример: Выбор библиотеки оптимизации (комплексный анализ)")
        print("0. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == '1':
            bpa = TestExamples.example_2_1()
            DSVisualizer.plot_belief_plausibility(bpa, "Пример 2.1: Кандидаты на должность")
            DSVisualizer.plot_bpa_distribution(bpa, "Пример 2.1: Распределение BPA")
            
        elif choice == '2':
            bpa = TestExamples.example_2_2()
            DSVisualizer.plot_bpa_distribution(bpa, "Пример 2.2: Распределение BPA")
            
        elif choice == '3':
            bpa = TestExamples.example_2_6()
            DSVisualizer.plot_belief_plausibility(bpa, "Пример 2.6: Комбинирование свидетельств")
            DSVisualizer.plot_bpa_distribution(bpa, "Пример 2.6: Распределение BPA")
            
        elif choice == '4':
            yager_result, _, _, _ = TestExamples.example_2_8()
            DSVisualizer.plot_bpa_distribution(yager_result, "Пример 2.8: Правило Ягера")
            
        elif choice == '5':
            yager_result, dempster_result, bpa1, bpa2 = TestExamples.compare_dempster_yager()
            DSVisualizer.compare_combination_methods(bpa1, bpa2, dempster_result, yager_result, 
                                                   "Сравнение Демпстера и Ягера")
            
            DSVisualizer.compare_combination_methods_detailed(bpa1, bpa2, dempster_result, yager_result, 
                                                    "Детальное сравнение методов")
            
        elif choice == '6':
            print("\nЗапуск всех примеров...")
            print("\n" + "="*60)
            
            # Пример 2.1
            print("\n>>> Пример 2.1: Кандидаты на должность")
            bpa_2_1 = TestExamples.example_2_1()
            DSVisualizer.plot_belief_plausibility(bpa_2_1, "Пример 2.1: Кандидаты на должность")
            DSVisualizer.plot_bpa_distribution(bpa_2_1, "Пример 2.1: Распределение BPA")
            
            input("\nНажмите Enter для продолжения к следующему примеру...")
            
            # Пример 2.2
            print("\n>>> Пример 2.2: Прогноз цен акций")
            bpa_2_2 = TestExamples.example_2_2()
            DSVisualizer.plot_bpa_distribution(bpa_2_2, "Пример 2.2: Распределение BPA")
            
            input("\nНажмите Enter для продолжения к следующему примеру...")
            
            # Пример 2.6
            print("\n>>> Пример 2.6: Комбинирование свидетельств (Демпстер)")
            bpa_2_6 = TestExamples.example_2_6()
            DSVisualizer.plot_belief_plausibility(bpa_2_6, "Пример 2.6: Комбинирование свидетельств")
            DSVisualizer.plot_bpa_distribution(bpa_2_6, "Пример 2.6: Распределение BPA")
            
            input("\nНажмите Enter для продолжения к следующему примеру...")
            
            # Пример 2.8
            print("\n>>> Пример 2.8: Правило комбинирования Ягера")
            yager_result, dempster_result, bpa1, bpa2 = TestExamples.example_2_8()
            DSVisualizer.plot_bpa_distribution(yager_result, "Пример 2.8: Правило Ягера")
            
            input("\nНажмите Enter для сравнения методов...")
            
            # Сравнение
            print("\n>>> Сравнение Демпстера и Ягера")
            DSVisualizer.compare_combination_methods(bpa1, bpa2, dempster_result, yager_result, 
                                                   "Сравнение Демпстера и Ягера")
            
            print("\n" + "="*60)
            print("Все примеры завершены!")

        elif choice == '7':
            print("\nЗапуск комплексного анализа выбора библиотеки оптимизации...")
            results = TestExamples.my_example()
            
            # Визуализация результатов
            if results:
                DSVisualizer.plot_belief_plausibility(
                    results['bpa_experts'], 
                    "Аналог примера 2.1: Выбор библиотеки по мнению экспертов"
                )
                
                DSVisualizer.plot_bpa_distribution(
                    results['combined_dempster'],
                    "Аналог примера 2.6: Комбинирование свидетельств о библиотеках"
                )
                
                DSVisualizer.compare_combination_methods(
                    results['bpa_speed'],
                    results['bpa_precision'],
                    results['combined_dempster'],
                    results['combined_yager'],
                    "Аналог примера 2.8: Сравнение Демпстера и Ягера для библиотек"
                )
            
        elif choice == '0':
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()