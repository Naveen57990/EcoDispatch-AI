"""
Unit tests for Grid Modeling Engine
"""
import pytest
from datetime import datetime, timezone
from ecodispatch.core.models import GridRegion
from ecodispatch.core.grid import GridEngine

def test_caiso_24h_forecast():
    engine = GridEngine(GridRegion.CAISO, start_time=datetime(2026, 9, 20, 0, 0, tzinfo=timezone.utc))
    forecast = engine.generate_24h_forecast()
    
    assert len(forecast) == 24
    
    # Solar should be 0 at midnight (hour 0)
    assert forecast[0].solar_generation_mw == 0.0
    
    # Solar should peak around midday (hour 12)
    solar_12 = forecast[12].solar_generation_mw
    assert solar_12 > 10000.0
    
    # Carbon intensity should be lowest during midday peak solar
    intensity_midnight = forecast[0].carbon_intensity
    intensity_noon = forecast[12].carbon_intensity
    assert intensity_noon < intensity_midnight

def test_ercot_wind_pattern():
    engine = GridEngine(GridRegion.ERCOT, start_time=datetime(2026, 9, 20, 0, 0, tzinfo=timezone.utc))
    forecast = engine.generate_24h_forecast()
    
    # In ERCOT, wind is stronger at night than afternoon
    wind_midnight = forecast[0].wind_generation_mw
    wind_noon = forecast[12].wind_generation_mw
    assert wind_midnight > wind_noon

def test_green_valley_identification():
    engine = GridEngine(GridRegion.CAISO)
    forecast = engine.generate_24h_forecast()
    
    green_valleys = [p for p in forecast if p.is_green_valley]
    assert len(green_valleys) >= 6
    # All green valleys must have lower intensity than non-valleys
    max_valley_intensity = max(p.carbon_intensity for p in green_valleys)
    non_valleys = [p for p in forecast if not p.is_green_valley]
    min_non_valley = min(p.carbon_intensity for p in non_valleys)
    assert max_valley_intensity <= min_non_valley
