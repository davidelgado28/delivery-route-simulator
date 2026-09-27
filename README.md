# delivery-route-simulator

Projeto em Python desenvolvido para resolução do Problema do Caixeiro Viajante (TSP) e algoritmos de menor caminho (Dijkstra), associado à simulação estatística Monte Carlo leve para previsão de atrasos e consumo sob incertezas operacionais.

O projeto utiliza a cidade de **Poços de Caldas - MG** como cenário real de simulação.

## Funcionalidades

- **Otimização de Grafos**: Resolução de rotas utilizando a heurística do Vizinho Mais Próximo para TSP e Dijkstra para caminhos mínimos.
- **Simulação Probabilística**: Modelagem de interferências climáticas (Sol, Neblina, Chuva) e de tráfego (Horário de Pico vs Normal) sobre tempo e combustível.
- **Persistência de Dados**: Histórico automático salvo em banco de dados SQLite (`delivery_history.db`).
- **Visualização Interativa**: Geração de mapa 2D do trajeto otimizado e gráficos comparativos de desempenho frente às médias históricas com Matplotlib.

## Tecnologias Utilizadas

- **Python 3.9+**
- **Matplotlib**: Plotagem de mapas de rota e gráficos comparativos.
- **SQLite3**: Banco de dados relacional embutido.
- **Tabulate**: Formatação de tabelas no terminal CLI.
- **Data Classes & Type Hints**: Boas práticas e código fortemente tipado.

## Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/delivery-route-simulator.git](https://github.com/seu-usuario/delivery-route-simulator.git)
   cd delivery-route-simulator
