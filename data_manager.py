import sqlite3
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class Location:
    id: int
    name: str
    lat: float
    lon: float

POCOS_DE_CALDAS_LOCATIONS: List[Location] = [
    Location(0, "Centro (CD Principal)", -21.7889, -46.5654),
    Location(1, "Zona Sul", -21.8210, -46.5500),
    Location(2, "Jardim Kennedy", -21.8295, -46.5831),
    Location(3, "Cascatinha", -21.7820, -46.5800),
    Location(4, "Região Leste", -21.7850, -46.5350),
    Location(5, "Represa Bortolan", -21.7650, -46.6200),
    Location(6, "Vila Nova", -21.7750, -46.5600),
    Location(7, "Parque das Nações", -21.8000, -46.5400),
    Location(8, "San Antonio", -21.7920, -46.5900),
    Location(9, "Jardim Elisabete", -21.8100, -46.5680),
]

class DatabaseManager:

    def __init__(self, db_path: str = "delivery_history.db") -> None:
        self.db_path = db_path
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão ativa com o banco de dados."""
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS route_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            route_path TEXT NOT NULL,
            total_distance_km REAL NOT NULL,
            total_time_min REAL NOT NULL,
            fuel_consumed_l REAL NOT NULL,
            weather TEXT NOT NULL,
            traffic_condition TEXT NOT NULL,
            delay_probability REAL NOT NULL
        )
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
        except sqlite3.Error as e:
            print(f"[ERRO DB] Falha ao criar tabela: {e}")

    def save_simulation(
        self,
        route_names: List[str],
        total_distance: float,
        total_time: float,
        fuel_consumed: float,
        weather: str,
        traffic: str,
        delay_prob: float
    ) -> bool:
        """Salva uma simulação executada no banco de dados.

        Args:
            route_names: Lista ordenada de nomes dos locais visitados.
            total_distance: Distância total percorrida em km.
            total_time: Tempo estimado total em minutos.
            fuel_consumed: Combustível gasto em litros.
            weather: Condição climática da simulação.
            traffic: Estado do tráfego.
            delay_prob: Probabilidade de atraso em percentual (0-100).

        Returns:
            bool: True se inserido com sucesso, False caso contrário.
        """
        query = """
        INSERT INTO route_history 
        (route_path, total_distance_km, total_time_min, fuel_consumed_l, weather, traffic_condition, delay_probability)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query,
                    (
                        json.dumps(route_names, ensure_ascii=False),
                        round(total_distance, 2),
                        round(total_time, 2),
                        round(fuel_consumed, 2),
                        weather,
                        traffic,
                        round(delay_prob, 2)
                    )
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"[ERRO DB] Falha ao salvar histórico: {e}")
            return False

    def fetch_history(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM route_history ORDER BY id DESC"
        records = []
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                rows = cursor.execute(query).fetchall()
                for row in rows:
                    data = dict(row)
                    data['route_path'] = json.loads(data['route_path'])
                    records.append(data)
        except sqlite3.Error as e:
            print(f"[ERRO DB] Falha ao ler histórico: {e}")
        return records

    def get_historical_averages(self) -> Optional[Dict[str, float]]:
        query = "SELECT AVG(total_time_min) as avg_time, AVG(fuel_consumed_l) as avg_fuel FROM route_history"
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                row = cursor.execute(query).fetchone()
                if row and row['avg_time'] is not None:
                    return {
                        "avg_time": float(row['avg_time']),
                        "avg_fuel": float(row['avg_fuel'])
                    }
        except sqlite3.Error as e:
            print(f"[ERRO DB] Falha ao calcular médias: {e}")
        return None
