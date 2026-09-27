import sys
import random
from typing import List
from tabulate import tabulate
from data_manager import POCOS_DE_CALDAS_LOCATIONS, DatabaseManager
from graph_solver import GraphSolver
from simulator import RouteSimulator, SimulationConfig
from visualizer import RouteVisualizer

class RouteSimulatorCLI:

    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        self.locations = POCOS_DE_CALDAS_LOCATIONS
        self.solver = GraphSolver(self.locations)

    def print_header() -> None:
        print("\n" + "="*65)
        print("   OTIMIZADOR E SIMULADOR ESTATÍSTICO DE ROTAS - POÇOS DE CALDAS")
        print("="*65)

    def run_simulation_flow(self) -> None:
        print("\n--- Configuração da Simulação ---")
        print("Escolha as condições climáticas:")
        print("1. Sol / Limpo")
        print("2. Chuva Forte")
        print("3. Neblina")
        print("4. Aleatório")
        weather_opt = input("Opção (1-4) [Padrão: Aleatório]: ").strip()
        weather_map = {"1": "Sol", "2": "Chuva Forte", "3": "Neblina"}
        if weather_opt in weather_map:
            weather = weather_map[weather_opt]
        else:
            weather = random.choice(["Sol", "Chuva Forte", "Neblina"])

        print("\nHorário de tráfego:")
        print("1. Horário Normal")
        print("2. Horário de Pico")
        traffic_opt = input("Opção (1-2) [Padrão: Normal]: ").strip()
        traffic_peak = True if traffic_opt == "2" else False
        kml_input = input("\nConsumo médio do veículo em km/l [Padrão: 10.0]: ").strip()
        try:
            kml = float(kml_input) if kml_input else 10.0
        except ValueError:
            kml = 10.0

        route_sequence, total_distance = self.solver.solve_tsp_nearest_neighbor(start_id=0)
        config = SimulationConfig(weather=weather, traffic_peak=traffic_peak, vehicle_kml=kml)
        simulator = RouteSimulator(config)
        metrics = simulator.run_simulation(total_distance)
        route_names = [loc.name for loc in route_sequence]
        
        print("\n" + "-"*50)
        print("          RESULTADOS DA SIMULAÇÃO DE ROTA")
        print("-"*50)
        print(f" Sequência: {' -> '.join(route_names)}")
        print(f" Distância Total    : {metrics['total_distance_km']:.2f} km")
        print(f" Tempo Estimado     : {metrics['total_time_min']:.1f} min")
        print(f" Consumo de Custo   : {metrics['fuel_consumed_l']:.2f} Litros")
        print(f" Condição Clima     : {metrics['weather']}")
        print(f" Estado do Tráfego  : {metrics['traffic']}")
        print(f" Prob. de Atraso    : {metrics['delay_probability']:.1f}%")
        print("-" * 50)

        saved = self.db_manager.save_simulation(
            route_names=route_names,
            total_distance=metrics['total_distance_km'],
            total_time=metrics['total_time_min'],
            fuel_consumed=metrics['fuel_consumed_l'],
            weather=metrics['weather'],
            traffic=metrics['traffic'],
            delay_prob=metrics['delay_probability']
        )
        if saved:
            print("Registro de simulação salvo no banco de dados SQLite com sucesso.")

        show_charts = input("\nDeseja gerar a visualização gráfica da rota e métricas? (s/n): ").strip().lower()
        if show_charts == 's':
            averages = self.db_manager.get_historical_averages()
            RouteVisualizer.plot_route_map(route_sequence)
            RouteVisualizer.plot_performance_comparison(metrics, averages)

    def show_history_flow(self) -> None:
        history = self.db_manager.fetch_history()
        if not history:
            print("\n[!] Nenhum registro de histórico encontrado.")
            return

        table_data = []
        for reg in history[:10]:  
            table_data.append([
                reg['id'],
                reg['timestamp'],
                f"{reg['total_distance_km']} km",
                f"{reg['total_time_min']} min",
                f"{reg['fuel_consumed_l']} L",
                reg['weather'],
                reg['traffic_condition'],
                f"{reg['delay_probability']}%"
            ])

        headers = ["ID", "Data/Hora", "Distância", "Tempo", "Combustível", "Clima", "Tráfego", "Atraso %"]
        print("\n--- Histórico das Últimas Simulações ---")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def start(self) -> None:
        while True:
            self.print_header()
            print("1. Iniciar Nova Simulação de Rota")
            print("2. Visualizar Histórico de Simulações")
            print("3. Sair")
            
            choice = input("\nEscolha uma opção: ").strip()

            if choice == "1":
                self.run_simulation_flow()
            elif choice == "2":
                self.show_history_flow()
            elif choice == "3":
                print("\nSaindo do sistema. Até logo!")
                sys.exit(0)
            else:
                print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    app = RouteSimulatorCLI()
    app.start()
