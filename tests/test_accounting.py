"""
Unit tests for Carbon Accounting & Verifiable Certificate Engine
"""
import pytest
from ecodispatch.core.models import GridRegion, DispatchDecision
from ecodispatch.core.accounting import CarbonAccounting

def test_certificate_math_and_audit_hash():
    accounting = CarbonAccounting(GridRegion.CAISO)
    decisions = [
        DispatchDecision(
            job_id="J1",
            job_name="Model Job",
            region=GridRegion.CAISO,
            scheduled_start_hour=11,
            scheduled_end_hour=13,
            total_energy_kwh=20.0,
            baseline_carbon_g=8000.0,
            optimized_carbon_g=3000.0,
            avoided_carbon_g=5000.0,
            avoided_percentage=62.5,
            average_renewable_percent=88.5
        ),
        DispatchDecision(
            job_id="J2",
            job_name="Batch ETL",
            region=GridRegion.CAISO,
            scheduled_start_hour=12,
            scheduled_end_hour=14,
            total_energy_kwh=10.0,
            baseline_carbon_g=4000.0,
            optimized_carbon_g=1500.0,
            avoided_carbon_g=2500.0,
            avoided_percentage=62.5,
            average_renewable_percent=90.0
        )
    ]
    
    cert = accounting.generate_certificate(decisions)
    
    assert cert.total_jobs_dispatched == 2
    assert cert.total_energy_consumed_kwh == 30.0
    assert cert.baseline_emissions_kg_co2 == 12.0  # (8000 + 4000) / 1000
    assert cert.optimized_emissions_kg_co2 == 4.5  # (3000 + 1500) / 1000
    assert cert.net_avoided_kg_co2 == 7.5          # 12.0 - 4.5
    assert cert.reduction_percentage == 62.5
    assert len(cert.audit_hash) == 64  # Valid SHA-256 string

def test_csv_export():
    accounting = CarbonAccounting(GridRegion.ERCOT)
    decisions = [
        DispatchDecision(
            job_id="J1",
            job_name="Wind Job",
            region=GridRegion.ERCOT,
            scheduled_start_hour=2,
            scheduled_end_hour=4,
            total_energy_kwh=15.0,
            baseline_carbon_g=6000.0,
            optimized_carbon_g=2000.0,
            avoided_carbon_g=4000.0,
            avoided_percentage=66.7,
            average_renewable_percent=85.0
        )
    ]
    csv_str = accounting.export_csv(decisions)
    assert "Job ID,Job Name,Region" in csv_str
    assert "J1,\"Wind Job\",US-ERCOT" in csv_str
    assert "-66.7%" in csv_str or "66.7%" in csv_str
