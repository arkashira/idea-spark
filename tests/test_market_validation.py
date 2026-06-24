from market_validation import analyze_demand, flag_saturated_niches, suggest_alternatives
import pytest

def test_analyze_demand():
    idea = "test_idea"
    search_volume = 100
    competition_score = 0.5
    pricing_data = [
        {"price": 10.0, "demand": 100},
        {"price": 20.0, "demand": 50}
    ]
    result = analyze_demand(idea, search_volume, competition_score, pricing_data)
    assert result["idea"] == idea
    assert result["demand_metrics"]["search_volume"] == search_volume
    assert result["demand_metrics"]["competition_score"] == competition_score
    assert result["willingness_to_pay"] == (10.0 * 100 + 20.0 * 50) / (100 + 50)

def test_flag_saturated_niches():
    ideas = ["test_idea1", "test_idea2"]
    demand_data = [
        {"idea": "test_idea1", "demand_metrics": {"search_volume": 1500}},
        {"idea": "test_idea2", "demand_metrics": {"search_volume": 500}}
    ]
    saturated_niches = flag_saturated_niches(ideas, demand_data)
    assert saturated_niches == ["test_idea1"]

def test_suggest_alternatives():
    saturated_niches = ["test_idea1"]
    all_ideas = ["test_idea1", "test_idea2", "test_idea3"]
    alternatives = suggest_alternatives(saturated_niches, all_ideas)
    assert alternatives == ["test_idea2", "test_idea3"]

def test_analyze_demand_edge_case():
    idea = "test_idea"
    search_volume = 0
    competition_score = 0.0
    pricing_data = []
    result = analyze_demand(idea, search_volume, competition_score, pricing_data)
    assert result["idea"] == idea
    assert result["demand_metrics"]["search_volume"] == search_volume
    assert result["demand_metrics"]["competition_score"] == competition_score
    assert result["willingness_to_pay"] == 0.0
