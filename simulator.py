import random
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from data_manager import Location


@dataclass
class SimulationConfig:
    weather: str                      
    traffic_peak: bool               
    vehicle_kml: float = 10.0       
    base_speed_kmh: float = 40.0     


class RouteSimulator:
    WEATHER_SPEED_FACTORS = {
        "Sol": 1.00,
        "Neblina": 0.85,
        "Chuva Forte": 0.70
    }
    WEATHER_DELAY_RISK = {
        "Sol": 0.05,
        "Neblina": 0.20,
        "Chuva Forte": 0.40
    }
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

    def run_simulation(self, total_distance_km: float) -> Dict[str, Any]:
        traffic_factor = 0.65 if self.config.traffic_peak else 1.00
        traffic_str = "Pico" if self.config.traffic_peak else "Normal"
        weather_factor = self.WEATHER_SPEED_FACTORS.get(self.config.weather, 1.0)
        effective_speed = self.config.base_speed_kmh * traffic_factor * weather_factor
        speed_noise = random.gauss(0, 2.5) 
        final_speed = max(15.0, effective_speed + speed_noise)  
        time_hours = total_distance_km / final_speed
        total_time_min = time_hours * 60.0
        efficiency_modifier = 1.0
        if self.config.traffic_peak:
            efficiency_modifier *= 1.25  
        if self.config.weather == "Chuva Forte":
            efficiency_modifier *= 1.10

        effective_kml = self.config.vehicle_kml / efficiency_modifier
        fuel_consumed = total_distance_km / effective_kml
        base_delay_prob = self.WEATHER_DELAY_RISK.get(self.config.weather, 0.1)
        if self.config.traffic_peak:
            base_delay_prob += 0.35
        delay_probability = min(0.98, max(0.02, random.gauss(base_delay_prob, 0.05))) * 100.0

        return {
            "total_distance_km": total_distance_km,
            "total_time_min": total_time_min,
            "fuel_consumed_l": fuel_consumed,
            "effective_speed_kmh": final_speed,
            "weather": self.config.weather,
            "traffic": traffic_str,
            "delay_probability": delay_probability
        }
