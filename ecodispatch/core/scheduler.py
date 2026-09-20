"""
Autonomous Carbon-Aware Workload Scheduler
Optimizes compute job execution windows against regional grid renewable curves to minimize carbon emissions.
"""
import math
from typing import List, Optional, Tuple
from ecodispatch.core.models import ComputeJob, DispatchDecision, GridRegion, CarbonForecastPoint, JobPriority

class CarbonScheduler:
    def __init__(self, region: GridRegion, forecast: List[CarbonForecastPoint], max_cluster_kw: float = 100.0):
        self.region = region
        self.forecast = forecast
        self.max_cluster_kw = max_cluster_kw
        # Maps hour_offset (0..23) -> current allocated kW
        self.grid_load: List[float] = [0.0] * 24

    def schedule_job(self, job: ComputeJob) -> DispatchDecision:
        duration = int(math.ceil(job.duration_hours))
        max_start = int(math.floor(job.deadline_hours)) - duration
        max_start = max(0, min(max_start, 24 - duration))

        # Baseline: execute immediately at hour 0
        baseline_carbon = self._calculate_carbon(0, duration, job.compute_power_kw)

        # Critical jobs with immediate urgency
        if job.priority == JobPriority.CRITICAL and max_start == 0:
            best_start = 0
        else:
            best_start = self._find_optimal_start(job, max_start, duration)

        # Allocate to cluster load
        for h in range(best_start, best_start + duration):
            self.grid_load[h] += job.compute_power_kw

        # Optimized carbon
        optimized_carbon = self._calculate_carbon(best_start, duration, job.compute_power_kw)
        avoided_carbon = max(0.0, baseline_carbon - optimized_carbon)
        avoided_pct = (avoided_carbon / baseline_carbon * 100.0) if baseline_carbon > 0 else 0.0

        # Average renewable percentage during scheduled window
        avg_renew = sum(self.forecast[h].renewable_percentage for h in range(best_start, best_start + duration)) / duration

        total_energy = job.compute_power_kw * job.duration_hours

        return DispatchDecision(
            job_id=job.id,
            job_name=job.name,
            region=self.region,
            scheduled_start_hour=best_start,
            scheduled_end_hour=best_start + duration,
            total_energy_kwh=round(total_energy, 2),
            baseline_carbon_g=round(baseline_carbon, 1),
            optimized_carbon_g=round(optimized_carbon, 1),
            avoided_carbon_g=round(avoided_carbon, 1),
            avoided_percentage=round(avoided_pct, 1),
            average_renewable_percent=round(avg_renew, 1),
            status="SCHEDULED"
        )

    def _find_optimal_start(self, job: ComputeJob, max_start: int, duration: int) -> int:
        best_hour = 0
        lowest_carbon = float("inf")

        for candidate_start in range(0, max_start + 1):
            # Check cluster capacity
            can_fit = True
            for h in range(candidate_start, candidate_start + duration):
                if self.grid_load[h] + job.compute_power_kw > self.max_cluster_kw:
                    can_fit = False
                    break
            
            if not can_fit:
                continue

            # Calculate total carbon for this window
            candidate_carbon = self._calculate_carbon(candidate_start, duration, job.compute_power_kw)

            # Check max carbon threshold constraint
            if job.max_carbon_threshold is not None:
                max_in_window = max(self.forecast[h].carbon_intensity for h in range(candidate_start, candidate_start + duration))
                if max_in_window > job.max_carbon_threshold:
                    # Penalize window violating hard threshold
                    candidate_carbon += 100000.0

            if candidate_carbon < lowest_carbon:
                lowest_carbon = candidate_carbon
                best_hour = candidate_start

        return best_hour

    def _calculate_carbon(self, start_hour: int, duration: int, power_kw: float) -> float:
        total_g = 0.0
        for h in range(start_hour, min(start_hour + duration, len(self.forecast))):
            intensity = self.forecast[h].carbon_intensity  # gCO2/kWh
            total_g += power_kw * 1.0 * intensity
        return total_g

    def schedule_batch(self, jobs: List[ComputeJob]) -> List[DispatchDecision]:
        # Sort jobs by priority and deadline
        priority_rank = {
            JobPriority.CRITICAL: 0,
            JobPriority.HIGH: 1,
            JobPriority.MEDIUM: 2,
            JobPriority.LOW: 3
        }
        sorted_jobs = sorted(jobs, key=lambda j: (priority_rank[j.priority], j.deadline_hours))
        return [self.schedule_job(job) for job in sorted_jobs]
