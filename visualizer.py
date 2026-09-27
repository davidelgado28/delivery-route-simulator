from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
from data_manager import Location


class RouteVisualizer:

    @staticmethod
    def plot_route_map(locations_sequence: List[Location], title: str = "Rota Otimizada de Entrega") -> None:
        lats = [loc.lat for loc in locations_sequence]
        lons = [loc.lon for loc in locations_sequence]
        plt.figure(figsize=(10, 6))
        plt.plot(lons, lats, color='#2b5c8f', linestyle='-', linewidth=2, zorder=1, label='Trajeto Otimizado')
        
        for i in range(len(locations_sequence) - 1):
            dx = lons[i+1] - lons[i]
            dy = lats[i+1] - lats[i]
            plt.arrow(
                lons[i], lats[i], dx * 0.8, dy * 0.8,
                head_width=0.002, head_length=0.003, fc='#e74c3c', ec='#e74c3c', zorder=2
            )
        plt.scatter(lons, lats, color='#e74c3c', s=80, zorder=3)
        plt.scatter([lons[0]], [lats[0]], color='#27ae60', s=150, zorder=4, label='Início/Fim (CD)')

        for idx, loc in enumerate(locations_sequence[:-1]):
            plt.annotate(
                f"{idx}. {loc.name}",
                (loc.lon, loc.lat),
                textcoords="offset points",
                xytext=(0, 8),
                ha='center',
                fontsize=9,
                weight='bold'
            )

        plt.title(title, fontsize=14, pad=15)
        plt.xlabel("Longitudinal", fontsize=10)
        plt.ylabel("Latitudinal", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_performance_comparison(
        current_metrics: Dict[str, Any],
        historical_averages: Optional[Dict[str, float]]
    ) -> None:
        if not historical_averages or historical_averages.get('avg_time') is None:
            print("\n[Aviso] Histórico insuficiente para gerar gráfico comparativo.")
            return

        categories = ['Tempo Estimado (min)', 'Consumo de Combustível (L)']
        current_values = [current_metrics['total_time_min'], current_metrics['fuel_consumed_l']]
        avg_values = [historical_averages['avg_time'], historical_averages['avg_fuel']]
        x = [0, 1]
        width = 0.35
        fig, ax = plt.subplots(figsize=(8, 5))
        rects1 = ax.bar([i - width/2 for i in x], current_values, width, label='Simulação Atual', color='#2980b9')
        rects2 = ax.bar([i + width/2 for i in x], avg_values, width, label='Média Histórica', color='#7f8c8d')
        ax.set_ylabel('Valores')
        ax.set_title('Desempenho da Rota: Simulação Atual vs Média Histórica', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.bar_label(rects1, fmt='%.1f', padding=3)
        ax.bar_label(rects2, fmt='%.1f', padding=3)
        fig.tight_layout()
        plt.show()
