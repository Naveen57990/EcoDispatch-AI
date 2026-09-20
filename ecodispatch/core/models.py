"""
Core Data Models for EcoDispatch AI
Pydantic v2 data structures for grid intensity, compute jobs, and carbon accounting.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class GridRegion(str, Enum):
    CAISO = "US-CAISO"          # California ISO (high solar peak midday)
    ERCOT = "US-ERCOT"          # Texas Interconnection (high nocturnal wind)
    UK_NATIONAL_GRID = "GB-UK"  # Great Britain National Grid
    GERMANY = "DE-TENNET"       # Germany Central Europe
    INDIA_NORTHERN = "IN-NORTH" # Northern Regional Load Despatch

class JobPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class CarbonForecastPoint(BaseModel):
    hour_offset: int = Field(..., ge=0, le=24, description="Hour offset from current time (0 to 24)")
    timestamp: datetime
    carbon_intensity: float = Field(..., description="Marginal carbon intensity in gCO2eq/kWh")
    renewable_percentage: float = Field(..., ge=0.0, le=100.0, description="Percentage of grid powered by renewables")
    solar_generation_mw: float = Field(default=0.0, description="Solar power output in MW")
    wind_generation_mw: float = Field(default=0.0, description="Wind power output in MW")
    fossil_generation_mw: float = Field(default=0.0, description="Coal and gas generation in MW")
    is_green_valley: bool = Field(default=False, description="True if this hour is an optimal low-carbon window")

class ComputeJob(BaseModel):
    id: str
    name: str
    compute_power_kw: float = Field(..., gt=0.0, description="Average power draw of compute cluster in kilowatts")
    duration_hours: float = Field(..., gt=0.0, description="Estimated execution duration in hours")
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deadline_hours: float = Field(..., gt=0.0, description="Maximum allowable delay from submission in hours")
    max_carbon_threshold: Optional[float] = Field(default=None, description="Maximum tolerable carbon intensity in gCO2/kWh")
    priority: JobPriority = Field(default=JobPriority.MEDIUM)

class DispatchDecision(BaseModel):
    job_id: str
    job_name: str
    region: GridRegion
    scheduled_start_hour: int
    scheduled_end_hour: int
    total_energy_kwh: float
    baseline_carbon_g: float
    optimized_carbon_g: float
    avoided_carbon_g: float
    avoided_percentage: float
    average_renewable_percent: float
    status: str = "SCHEDULED"

class AvoidedEmissionCertificate(BaseModel):
    certificate_id: str
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    region: GridRegion
    total_jobs_dispatched: int
    total_energy_consumed_kwh: float
    baseline_emissions_kg_co2: float
    optimized_emissions_kg_co2: float
    net_avoided_kg_co2: float
    reduction_percentage: float
    audit_hash: str
