"""
Carbon Accounting & Verifiable ESG Audit Engine
Computes avoided carbon metrics and issues tamper-evident emission mitigation certificates.
"""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict
from ecodispatch.core.models import (
    DispatchDecision,
    GridRegion,
    AvoidedEmissionCertificate
)

class CarbonAccounting:
    def __init__(self, region: GridRegion):
        self.region = region

    def generate_certificate(self, decisions: List[DispatchDecision]) -> AvoidedEmissionCertificate:
        if not decisions:
            raise ValueError("Cannot generate certificate from empty dispatch decisions.")

        total_energy_kwh = sum(d.total_energy_kwh for d in decisions)
        baseline_g = sum(d.baseline_carbon_g for d in decisions)
        optimized_g = sum(d.optimized_carbon_g for d in decisions)
        avoided_g = sum(d.avoided_carbon_g for d in decisions)

        baseline_kg = baseline_g / 1000.0
        optimized_kg = optimized_g / 1000.0
        avoided_kg = avoided_g / 1000.0
        reduction_pct = (avoided_g / baseline_g * 100.0) if baseline_g > 0 else 0.0

        now = datetime.now(timezone.utc)
        cert_id = f"ECO-{self.region.value}-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        # Cryptographic tamper-evident hash
        payload = {
            "cert_id": cert_id,
            "issued_at": now.isoformat(),
            "region": self.region.value,
            "jobs_count": len(decisions),
            "total_energy_kwh": round(total_energy_kwh, 3),
            "baseline_kg": round(baseline_kg, 4),
            "optimized_kg": round(optimized_kg, 4),
            "avoided_kg": round(avoided_kg, 4),
            "job_ids": [d.job_id for d in decisions]
        }
        serialized = json.dumps(payload, sort_keys=True)
        audit_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        return AvoidedEmissionCertificate(
            certificate_id=cert_id,
            issued_at=now,
            region=self.region,
            total_jobs_dispatched=len(decisions),
            total_energy_consumed_kwh=round(total_energy_kwh, 2),
            baseline_emissions_kg_co2=round(baseline_kg, 3),
            optimized_emissions_kg_co2=round(optimized_kg, 3),
            net_avoided_kg_co2=round(avoided_kg, 3),
            reduction_percentage=round(reduction_pct, 1),
            audit_hash=audit_hash
        )

    def export_csv(self, decisions: List[DispatchDecision]) -> str:
        headers = [
            "Job ID", "Job Name", "Region", "Start (Hr)", "End (Hr)",
            "Energy (kWh)", "Baseline (gCO2)", "Optimized (gCO2)", "Avoided (gCO2)", "Avoided (%)", "Avg Renewable (%)"
        ]
        rows = [",".join(headers)]
        for d in decisions:
            row = [
                d.job_id,
                f'"{d.job_name}"',
                d.region.value,
                str(d.scheduled_start_hour),
                str(d.scheduled_end_hour),
                f"{d.total_energy_kwh:.2f}",
                f"{d.baseline_carbon_g:.1f}",
                f"{d.optimized_carbon_g:.1f}",
                f"{d.avoided_carbon_g:.1f}",
                f"{d.avoided_percentage:.1f}%",
                f"{d.average_renewable_percent:.1f}%"
            ]
            rows.append(",".join(row))
        return "\n".join(rows)
