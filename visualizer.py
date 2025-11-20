"""
Улучшенная визуализация с использованием последних версий библиотек
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

try:
    from plotly import graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly не установлен. Интерактивные графики будут недоступны.")

class DSVisualizer:
    """Улучшенный визуализатор с использованием современных библиотек"""
    
    def __init__(self):
        # Настраиваем стиль для лучшего отображения
        plt.style.use('default')
        sns.set_theme(style="whitegrid")
    
    def _get_colors(self, n_colors):
        """Безопасное получение цветов для графиков"""
        # Используем встроенные палитры seaborn
        if n_colors <= 10:
            return sns.color_palette("husl", n_colors)
        else:
            return sns.color_palette("viridis", n_colors)
    
    @staticmethod
    def plot_belief_plausibility(bpa, title="Функции доверия и правдоподобия"):
        """Визуализация Bel и Pl с использованием современных возможностей"""
        elements = set()
        for subset in bpa.keys():
            elements.update(subset)
        
        elements = sorted(elements)
        beliefs = []
        plausibilities = []
        intervals = []
        
        from dempster_core import DempsterShafer
        ds = DempsterShafer(set(elements))
        
        for element in elements:
            event = {element}
            bel = ds.belief(event, bpa)
            pl = ds.plausibility(event, bpa)
            beliefs.append(bel)
            plausibilities.append(pl)
            intervals.append(pl - bel)  # Ширина интервала неопределенности
        
        # Создаем DataFrame для удобства
        df = pd.DataFrame({
            'Element': elements,
            'Belief': beliefs,
            'Plausibility': plausibilities,
            'Uncertainty': intervals
        })
        
        # Создаем график с subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # График 1: Bel и Pl
        x = np.arange(len(elements))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, beliefs, width, label='Доверие (Bel)', 
                       alpha=0.7, color='lightcoral')
        bars2 = ax1.bar(x + width/2, plausibilities, width, label='Правдоподобие (Pl)', 
                       alpha=0.7, color='lightseagreen')
        
        ax1.set_xlabel('Элементы')
        ax1.set_ylabel('Вероятность')
        ax1.set_title(f'{title} - Интервалы вероятностей')
        ax1.set_xticks(x)
        ax1.set_xticklabels(elements)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Добавляем значения на столбцы
        for i, (bel, pl) in enumerate(zip(beliefs, plausibilities)):
            ax1.text(i - width/2, bel + 0.01, f'{bel:.3f}', ha='center', fontsize=9)
            ax1.text(i + width/2, pl + 0.01, f'{pl:.3f}', ha='center', fontsize=9)
        
        # График 2: Неопределенность (разница между Pl и Bel)
        bars3 = ax2.bar(x, intervals, alpha=0.7, color='gold', label='Неопределенность')
        ax2.set_xlabel('Элементы')
        ax2.set_ylabel('Уровень неопределенности')
        ax2.set_title('Неопределенность (Pl - Bel)')
        ax2.set_xticks(x)
        ax2.set_xticklabels(elements)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Добавляем значения
        for i, unc in enumerate(intervals):
            ax2.text(i, unc + 0.01, f'{unc:.3f}', ha='center', fontsize=9)
        
        plt.tight_layout()
        plt.show()
        
        return df
    
    @staticmethod
    def plot_bpa_distribution(bpa, title="Распределение базовых вероятностей"):
        """Улучшенная визуализация распределения BPA"""
        # Создаем DataFrame для визуализации
        subsets = []
        masses = []
        
        for subset, mass in bpa.items():
            if mass > 0.0001:  # Игнорируем очень маленькие значения
                if not subset:  # Пустое множество
                    subset_str = "∅"
                elif subset == frozenset():  # Универсальное множество (в зависимости от реализации)
                    subset_str = "Ω"
                else:
                    subset_str = str(set(subset))
                subsets.append(subset_str)
                masses.append(mass)
        
        if not subsets:  # Если нет данных
            print("Нет данных для визуализации")
            return None
        
        df = pd.DataFrame({
            'Subset': subsets,
            'Mass': masses
        }).sort_values('Mass', ascending=False)
        
        # Создаем график
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График 1: Столбчатая диаграмма
        # Используем безопасную палитру цветов
        colors = sns.color_palette("husl", len(df))
        bars = ax1.bar(df['Subset'], df['Mass'], alpha=0.7, color=colors)
        ax1.set_xlabel('Фокальные элементы')
        ax1.set_ylabel('Базовая вероятность')
        ax1.set_title(f'{title} - Распределение масс')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Добавляем значения на столбцы
        for bar, mass in zip(bars, df['Mass']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{mass:.3f}', ha='center', va='bottom', fontsize=9)
        
        # График 2: Круговая диаграмма
        if len(df) > 1:  # Круговая диаграмма имеет смысл только для нескольких элементов
            ax2.pie(df['Mass'], labels=df['Subset'], autopct='%1.1f%%', startangle=90)
            ax2.set_title(f'{title} - Процентное распределение')
        else:
            ax2.text(0.5, 0.5, 'Недостаточно данных\nдля круговой диаграммы', 
                    ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title(f'{title} - Процентное распределение')
        
        plt.tight_layout()
        plt.show()
        
        return df
    
    @staticmethod
    def create_interactive_plot(bpa, title="Интерактивная визуализация"):
        """Интерактивная визуализация с использованием Plotly"""
        if not PLOTLY_AVAILABLE:
            print("Plotly не установлен. Используйте: pip install plotly")
            return None
            
        elements = set()
        for subset in bpa.keys():
            elements.update(subset)
        
        elements = sorted(elements)
        beliefs = []
        plausibilities = []
        
        from dempster_core import DempsterShafer
        ds = DempsterShafer(set(elements))
        
        for element in elements:
            event = {element}
            beliefs.append(ds.belief(event, bpa))
            plausibilities.append(ds.plausibility(event, bpa))
        
        # Создаем интерактивный график
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Доверие (Bel)',
            x=elements,
            y=beliefs,
            marker_color='lightcoral'
        ))
        
        fig.add_trace(go.Bar(
            name='Правдоподобие (Pl)',
            x=elements,
            y=plausibilities,
            marker_color='lightseagreen'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Элементы",
            yaxis_title="Вероятность",
            barmode='group',
            template='plotly_white'
        )
        
        fig.show()
        return fig
    
    @staticmethod
    def compare_combination_methods(bpa1, bpa2, dempster_result, yager_result, title="Сравнение методов комбинирования"):
        """Сравнение правил Демпстера и Ягера"""
        # Получаем все элементарные события из фрейма
        elements = set()
        for bpa in [bpa1, bpa2]:
            for subset in bpa.keys():
                elements.update(subset)
        
        elements = sorted(elements)
        
        from dempster_core import DempsterShafer
        ds = DempsterShafer(set(elements))
        
        comparison_data = []
        for element in elements:
            event = {element}
            comparison_data.append({
                'Element': element,
                'Source1_Bel': ds.belief(event, bpa1),
                'Source2_Bel': ds.belief(event, bpa2),
                'Dempster_Bel': ds.belief(event, dempster_result),
                'Yager_Bel': ds.belief(event, yager_result)
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Создаем график
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # График 1: Сравнение Bel для элементарных событий
        x = np.arange(len(df))
        width = 0.2
        
        bars1 = ax1.bar(x - width*1.5, df['Source1_Bel'], width, label='Источник 1', alpha=0.7, color='lightblue')
        bars2 = ax1.bar(x - width/2, df['Source2_Bel'], width, label='Источник 2', alpha=0.7, color='lightgreen')
        bars3 = ax1.bar(x + width/2, df['Dempster_Bel'], width, label='Демпстер', alpha=0.7, color='coral')
        bars4 = ax1.bar(x + width*1.5, df['Yager_Bel'], width, label='Ягер', alpha=0.7, color='gold')
        
        ax1.set_xlabel('Элементы')
        ax1.set_ylabel('Доверие (Bel)')
        ax1.set_title(f'{title} - Сравнение функций доверия')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df['Element'])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # График 2: Распределение масс для неэлементарных множеств
        ax2.set_title('Распределение масс для составных множеств')
        
        # Собираем данные для неэлементарных множеств
        non_elementary = {}
        for bpa, label in [(dempster_result, 'Демпстер'), (yager_result, 'Ягер')]:
            for subset, mass in bpa.items():
                if len(subset) > 1 or not subset:  # Неэлементарные множества и пустое
                    key = "Ω" if subset == frozenset(elements) else "∅" if not subset else str(set(subset))
                    if key not in non_elementary:
                        non_elementary[key] = {}
                    non_elementary[key][label] = mass
        
        # Создаем DataFrame для графика
        if non_elementary:
            non_elem_df = pd.DataFrame(non_elementary).T.fillna(0)
            colors = ['lightblue', 'lightcoral']
            non_elem_df.plot(kind='bar', ax=ax2, alpha=0.7, color=colors)
            ax2.set_ylabel('Базовая вероятность')
            ax2.tick_params(axis='x', rotation=45)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'Нет составных множеств\nдля сравнения', 
                    ha='center', va='center', transform=ax2.transAxes)
        
        plt.tight_layout()
        plt.show()
        
        return df
    
    @staticmethod
    def plot_interval_comparison(results_dict, title="Сравнение интервалов доверия"):
        """Сравнение интервалов [Bel, Pl] для разных методов или сценариев"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        scenarios = list(results_dict.keys())
        elements = set()
        
        # Собираем все элементы
        for scenario_data in results_dict.values():
            for element in scenario_data.keys():
                elements.add(element)
        
        elements = sorted(elements)
        
        # Цвета для разных сценариев
        scenario_colors = sns.color_palette("tab10", len(scenarios))
        
        # Рисуем интервалы для каждого элемента и сценария
        for i, element in enumerate(elements):
            y_pos = len(elements) - i - 1  # Чтобы первый элемент был сверху
            
            for j, (scenario, scenario_data) in enumerate(results_dict.items()):
                if element in scenario_data:
                    bel, pl = scenario_data[element]
                    # Линия интервала
                    ax.hlines(y_pos + j*0.2, bel, pl, colors=scenario_colors[j], 
                             linewidth=3, label=scenario if i == 0 else "")
                    # Точки для Bel и Pl
                    ax.scatter(bel, y_pos + j*0.2, color=scenario_colors[j], s=50, marker='|')
                    ax.scatter(pl, y_pos + j*0.2, color=scenario_colors[j], s=50, marker='|')
                    # Подпись значения
                    ax.text((bel + pl)/2, y_pos + j*0.2 + 0.1, f'[{bel:.2f}, {pl:.2f}]', 
                           ha='center', va='bottom', fontsize=8)
        
        ax.set_xlabel('Вероятность')
        ax.set_ylabel('Элементы')
        ax.set_title(title)
        ax.set_yticks(np.arange(len(elements)))
        ax.set_yticklabels(elements)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

    @staticmethod
    def compare_combination_methods_detailed(bpa1, bpa2, dempster_result, yager_result, title="Детальное сравнение методов"):
        """Детальное сравнение с отображением ВСЕХ множеств"""
        
        # Собираем ВСЕ множества из всех источников
        all_subsets = set()
        for bpa in [bpa1, bpa2, dempster_result, yager_result]:
            all_subsets.update(bpa.keys())
        
        # Преобразуем в читаемый формат
        subset_strings = []
        for subset in all_subsets:
            if not subset:  # Пустое множество
                subset_str = "∅"
            elif subset == frozenset():  # Универсальное множество
                subset_str = "Ω"
            else:
                subset_str = str(set(subset))
            subset_strings.append(subset_str)
        
        # Создаем данные для сравнения
        comparison_data = []
        
        for subset, subset_str in zip(all_subsets, subset_strings):
            if subset:  # Игнорируем пустое множество
                row = {'Subset': subset_str}
                
                # Bel для каждого источника/метода
                from dempster_core import DempsterShafer
                ds = DempsterShafer(set().union(*all_subsets))  # Создаем фрейм из всех элементов
                
                row['Source1_Bel'] = ds.belief(subset, bpa1) if subset in bpa1 or any(s.issubset(subset) for s in bpa1.keys()) else 0
                row['Source2_Bel'] = ds.belief(subset, bpa2) if subset in bpa2 or any(s.issubset(subset) for s in bpa2.keys()) else 0
                row['Dempster_Bel'] = ds.belief(subset, dempster_result)
                row['Yager_Bel'] = ds.belief(subset, yager_result)
                
                # BPA (базовые вероятности)
                row['Source1_BPA'] = bpa1.get(subset, 0)
                row['Source2_BPA'] = bpa2.get(subset, 0)
                row['Dempster_BPA'] = dempster_result.get(subset, 0)
                row['Yager_BPA'] = yager_result.get(subset, 0)
                
                comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        
        # Создаем комплексный график
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # График 1: Сравнение BPA (базовых вероятностей)
        x = np.arange(len(df))
        width = 0.15
        
        ax1.bar(x - width*1.5, df['Source1_BPA'], width, label='Источник 1 BPA', alpha=0.7, color='lightblue')
        ax1.bar(x - width/2, df['Source2_BPA'], width, label='Источник 2 BPA', alpha=0.7, color='lightgreen')
        ax1.bar(x + width/2, df['Dempster_BPA'], width, label='Демпстер BPA', alpha=0.7, color='coral')
        ax1.bar(x + width*1.5, df['Yager_BPA'], width, label='Ягер BPA', alpha=0.7, color='gold')
        
        ax1.set_xlabel('Множества')
        ax1.set_ylabel('Базовая вероятность (BPA)')
        ax1.set_title('Сравнение БАЗОВЫХ вероятностей')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df['Subset'], rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # График 2: Сравнение Bel (функций доверия)
        ax2.bar(x - width*1.5, df['Source1_Bel'], width, label='Источник 1 Bel', alpha=0.7, color='lightblue')
        ax2.bar(x - width/2, df['Source2_Bel'], width, label='Источник 2 Bel', alpha=0.7, color='lightgreen')
        ax2.bar(x + width/2, df['Dempster_Bel'], width, label='Демпстер Bel', alpha=0.7, color='coral')
        ax2.bar(x + width*1.5, df['Yager_Bel'], width, label='Ягер Bel', alpha=0.7, color='gold')
        
        ax2.set_xlabel('Множества')
        ax2.set_ylabel('Доверие (Bel)')
        ax2.set_title('Сравнение ФУНКЦИЙ ДОВЕРИЯ')
        ax2.set_xticks(x)
        ax2.set_xticklabels(df['Subset'], rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # График 3: BPA источников (детально)
        source1_data = {str(set(k)) if k else "∅": v for k, v in bpa1.items() if v > 0}
        source2_data = {str(set(k)) if k else "∅": v for k, v in bpa2.items() if v > 0}
        
        ax3.bar(range(len(source1_data)), list(source1_data.values()), alpha=0.7, color='lightblue')
        ax3.set_xticks(range(len(source1_data)))
        ax3.set_xticklabels(list(source1_data.keys()), rotation=45)
        ax3.set_title('Источник 1: Распределение BPA')
        ax3.set_ylabel('BPA')
        ax3.grid(True, alpha=0.3)
        
        # График 4: BPA источников (детально)
        ax4.bar(range(len(source2_data)), list(source2_data.values()), alpha=0.7, color='lightgreen')
        ax4.set_xticks(range(len(source2_data)))
        ax4.set_xticklabels(list(source2_data.keys()), rotation=45)
        ax4.set_title('Источник 2: Распределение BPA')
        ax4.set_ylabel('BPA')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Выводим таблицу для ясности
        print("\n" + "="*80)
        print("ДЕТАЛЬНАЯ ТАБЛИЦА СРАВНЕНИЯ")
        print("="*80)
        print(f"{'Множество':<10} | {'Src1 BPA':<8} | {'Src2 BPA':<8} | {'Demp BPA':<8} | {'Yager BPA':<8} | {'Src1 Bel':<8} | {'Src2 Bel':<8} | {'Demp Bel':<8} | {'Yager Bel':<8}")
        print("-" * 100)
        
        for _, row in df.iterrows():
            print(f"{row['Subset']:<10} | {row['Source1_BPA']:8.3f} | {row['Source2_BPA']:8.3f} | {row['Dempster_BPA']:8.3f} | {row['Yager_BPA']:8.3f} | {row['Source1_Bel']:8.3f} | {row['Source2_Bel']:8.3f} | {row['Dempster_Bel']:8.3f} | {row['Yager_Bel']:8.3f}")
        
        return df