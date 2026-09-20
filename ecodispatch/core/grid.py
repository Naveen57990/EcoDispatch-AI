"""
Regional Electrical Grid Carbon Intensity & Renewable Modeling Engine
Simulates and models real-world 24-hour marginal carbon intensity curves and generation mixes.
"""
from datetime import datetime, timezone, timedelta
import math
from typing import List, Dict
from ecodispatch.core.models import GridRegion, CarbonForecastPoint

# Regional baseline parameters: (fossil_base_mw, solar_peak_mw, wind_base_mw, emission_factor)
REGION_PROFILES = {
    GridRegion.CAISO: {
        "solar_peak_mw": 14500.0,
        "wind_avg_mw": 2800.0,
        "fossil_base_mw": 8500.0,
        "clean_floor_intensity": 65.0,     # gCO2/kWh at peak solar
        "fossil_peak_intensity": 460.0,    # gCO2/kWh during evening ramp (duck curve)
    },
    GridRegion.ERCOT: {
        "solar_peak_mw": 11000.0,
        "wind_avg_mw": 18500.0,            # Huge nocturnal wind
        "fossil_base_mw": 24000.0,
        "clean_floor_intensity": 110.0,
        "fossil_peak_intensity": 520.0,
    },
    GridRegion.UK_NATIONAL_GRID: {
        "solar_peak_mw": 6500.0,
        "wind_avg_mw": 12000.0,
        "fossil_base_mw": 7000.0,
        "clean_floor_intensity": 90.0,
        "fossil_peak_intensity": 380.0,
    },
    GridRegion.GERMANY: {
        "solar_peak_mw": 16000.0,
        "wind_avg_mw": 15000.0,
        "fossil_base_mw": 18000.0,
        "clean_floor_intensity": 120.0,
        "fossil_peak_intensity": 580.0,
    },
    GridRegion.INDIA_NORTHERN: {
        "solar_peak_mw": 18000.0,
        "wind_avg_mw": 4500.0,
        "fossil_base_mw": 35000.0,
        "clean_floor_intensity": 280.0,
        "fossil_peak_intensity": 780.0,
    }
}

class GridEngine:
    def __init__(self, region: GridRegion = GridRegion.CAISO, start_time: datetime = None):
        self.region = region
        self.start_time = start_time or datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        self.profile = REGION_PROFILES.get(region, REGION_PROFILES[GridRegion.CAISO])

    def generate_24h_forecast(self) -> List[CarbonForecastPoint]:
        points = []
        raw_intensities = []

        for h in range(24):
            t = self.start_time + timedelta(hours=h)
            hour_of_day = t.hour

            # 1. Solar generation curve (sine wave between 6:00 and 19:00)
            if 6 <= hour_of_day <= 18:
                sun_angle = (hour_of_day - 6) / 12.0 * math.pi
                solar_mw = self.profile["solar_peak_mw"] * math.sin(sun_angle)
            else:
                solar_mw = 0.0

            # 2. Wind generation curve (nocturnal peak for ERCOT, steady for CAISO/UK)
            if self.region == GridRegion.ERCOT:
                # Peaks at midnight (hour 0-5), dips in afternoon
                wind_factor = 1.0 + 0.35 * math.cos((hour_of_day / 24.0) * 2 * math.pi)
            else:
                wind_factor = 1.0 + 0.15 * math.sin((hour_of_day / 24.0) * 2 * math.pi)
            wind_mw = self.profile["wind_avg_mw"] * wind_factor

            # 3. Fossil thermal requirement
            total_renewable = solar_mw + wind_mw
            fossil_mw = max(1500.0, self.profile["fossil_base_mw"] - total_renewable * 0.45)

            # 4. Compute carbon intensity (gCO2eq/kWh)
            total_gen = total_renewable + fossil_mw
            renew_pct = min(100.0, max(0.0, (total_renewable / total_gen) * 100.0))

            # Marginal intensity: higher fossil share = higher intensity
            fossil_ratio = fossil_mw / total_gen
            c_floor = self.profile["clean_floor_intensity"]
            c_ceil = self.profile["fossil_peak_intensity"]
            intensity = c_floor + (c_ceil - c_floor) * math.pow(fossil_ratio, 1.4)
            intensity = round(intensity, 1)

            raw_intensities.append(intensity)

            points.append({
                "hour_offset": h,
                "timestamp": t,
                "carbon_intensity": intensity,
                "renewable_percentage": round(renew_pct, 1),
                "solar_generation_mw": round(solar_mw, 1),
                "wind_generation_mw": round(wind_mw, 1),
                "fossil_generation_mw": round(fossil_mw, 1),
            })

        # Identify Green Valleys: lowest 30% intensity hours
        threshold = sorted(raw_intensities)[int(len(raw_intensities) * 0.30)]
        forecast_points = []
        for p in points:
            p["is_green_valley"] = p["carbon_intensity"] <= threshold
            forecast_points.append(CarbonForecastPoint(**p))

        return forecast_points

    def get_current_intensity(self) -> CarbonForecastPoint:
        return self.generate_24h_forecast()[0]
