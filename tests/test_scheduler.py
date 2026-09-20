"""
Unit tests for Autonomous Carbon Scheduler
"""
import pytest
from datetime import datetime, timezone
from ecodispatch.core.models import GridRegion, ComputeJob, JobPriority
from ecodispatch.core.grid import GridEngine
from ecodispatch.core.scheduler import CarbonScheduler

@pytest.fixture
def caiso_scheduler():
    engine = GridEngine(GridRegion.CAISO, start_time=datetime(2026, 9, 20, 0, 0, tzinfo=timezone.utc))
    forecast = engine.generate_24h_forecast()
    return CarbonScheduler(GridRegion.CAISO, forecast, max_cluster_kw=50.0)

def test_deadline_enforcement(caiso_scheduler):
    # Job with duration 2h and strict deadline of 4h
    job = ComputeJob(
        id="TEST-1",
        name="Urgent Inference Job",
        compute_power_kw=5.0,
        duration_hours=2.0,
        deadline_hours=4.0,
        priority=JobPriority.HIGH
    )
    decision = caiso_scheduler.schedule_job(job)
    
    # Must finish by deadline
    assert decision.scheduled_end_hour <= 4
    assert decision.scheduled_start_hour >= 0

def test_carbon_reduction_optimization(caiso_scheduler):
    # Job submitted at hour 0 (midnight high fossil), deadline 16h (covers noon peak solar)
    job = ComputeJob(
        id="TEST-2",
        name="Flexible Training Run",
        compute_power_kw=10.0,
        duration_hours=3.0,
        deadline_hours=16.0,
        priority=JobPriority.LOW
    )
    decision = caiso_scheduler.schedule_job(job)
    
    # Optimizer should shift job to daytime green valley
    assert decision.scheduled_start_hour >= 6
    # Optimized emissions must be strictly lower than baseline unmanaged
    assert decision.optimized_carbon_g < decision.baseline_carbon_g
    assert decision.avoided_carbon_g > 0.0
    assert decision.avoided_percentage > 20.0

def test_cluster_capacity_limit(caiso_scheduler):
    job1 = ComputeJob(
        id="BIG-1",
        name="Large Cluster Job",
        compute_power_kw=45.0,
        duration_hours=1.0,
        deadline_hours=15.0
    )
    decision1 = caiso_scheduler.schedule_job(job1)

    # Second job of 15 kW cannot fit in the same slot as job1 (45 + 15 = 60 > 50)
    job2 = ComputeJob(
        id="BIG-2",
        name="Secondary Job",
        compute_power_kw=15.0,
        duration_hours=1.0,
        deadline_hours=15.0
    )
    decision2 = caiso_scheduler.schedule_job(job2)
    assert decision2.scheduled_start_hour != decision1.scheduled_start_hour
