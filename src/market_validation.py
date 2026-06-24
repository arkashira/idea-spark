import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DemandMetrics:
    search_volume: int
    competition_score: float

@dataclass
class PricingData:
    price: float
    demand: int

def calculate_willingness_to_pay(pricing_data: List[Dict]) -> float:
    total_revenue = sum(data['price'] * data['demand'] for data in pricing_data)
    total_demand = sum(data['demand'] for data in pricing_data)
    if total_demand == 0:
        return 0.0
    return total_revenue / total_demand

def analyze_demand(idea: str, search_volume: int, competition_score: float, pricing_data: List[Dict]) -> Dict:
    demand_metrics = DemandMetrics(search_volume, competition_score)
    willingness_to_pay = calculate_willingness_to_pay(pricing_data)
    return {
        "idea": idea,
        "demand_metrics": demand_metrics.__dict__,
        "willingness_to_pay": willingness_to_pay
    }

def flag_saturated_niches(ideas: List[str], demand_data: List[Dict]) -> List[str]:
    saturated_niches = []
    for idea in ideas:
        for data in demand_data:
            if data["idea"] == idea and data["demand_metrics"]["search_volume"] > 1000:
                saturated_niches.append(idea)
                break
    return saturated_niches

def suggest_alternatives(saturated_niches: List[str], all_ideas: List[str]) -> List[str]:
    return [idea for idea in all_ideas if idea not in saturated_niches]
