"""
EcoDispatch AI Terminal CLI
Rich interactive interface for regional grid inspection, workload optimization, and ESG audit reporting.
"""
import argparse
import sys
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ecodispatch.core.models import GridRegion, ComputeJob, JobPriority
from ecodispatch.core.grid import GridEngine
from ecodispatch.core.scheduler import CarbonScheduler
from ecodispatch.core.accounting import CarbonAccounting

console = Console()

SAMPLE_JOBS = [
    ComputeJob(id="JOB-101", name="LLM Fine-Tuning Batch (Llama-3-70B)", compute_power_kw=18.5, duration_hours=4.0, deadline_hours=14.0, priority=JobPriority.HIGH),
    ComputeJob(id="JOB-102", name="Diffusion Image Generation Pipeline", compute_power_kw=8.0, duration_hours=2.0, deadline_hours=8.0, priority=JobPriority.MEDIUM),
    ComputeJob(id="JOB-103", name="Nightly Vector Embedding Re-Index", compute_power_kw=12.0, duration_hours=3.5, deadline_hours=18.0, priority=JobPriority.LOW),
    ComputeJob(id="JOB-104", name="Zero-Day Security Vulnerability Audit", compute_power_kw=6.0, duration_hours=1.0, deadline_hours=2.0, priority=JobPriority.CRITICAL),
    ComputeJob(id="JOB-105", name="Synthetic Data Distillation Worker", compute_power_kw=15.0, duration_hours=5.0, deadline_hours=20.0, priority=JobPriority.LOW)
]

def show_grid(region_name: str = "US-CAISO"):
    region = next((r for r in GridRegion if r.value == region_name or r.name.lower() == region_name.lower()), GridRegion.CAISO)
    engine = GridEngine(region)
    forecast = engine.generate_24h_forecast()

    console.print(Panel(
        f"[bold green]ECODISPATCH AI :: REGIONAL ELECTRICAL GRID INTELLIGENCE[/bold green]\n"
        f"[cyan]Region:[/cyan] {region.value} | [cyan]Timestamp:[/cyan] {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        border_style="green"
    ))

    table = Table(title=f"24-Hour Carbon & Generation Forecast ({region.value})", border_style="dim")
    table.add_column("Hour", justify="center", style="bold")
    table.add_column("Time", justify="center")
    table.add_column("Carbon Intensity", justify="right")
    table.add_column("Renewables %", justify="right")
    table.add_column("Solar (MW)", justify="right", style="yellow")
    table.add_column("Wind (MW)", justify="right", style="cyan")
    table.add_column("Fossil (MW)", justify="right", style="red")
    table.add_column("Window Classification", justify="center")

    for p in forecast:
        t_str = p.timestamp.strftime("%H:00")
        intensity_str = f"{p.carbon_intensity:.1f} g/kWh"
        if p.is_green_valley:
            tag = "[bold green]🌱 GREEN VALLEY[/bold green]"
            i_styled = f"[bold green]{intensity_str}[/bold green]"
        elif p.carbon_intensity > 350.0:
            tag = "[bold red]🚨 PEAK FOSSIL[/bold red]"
            i_styled = f"[bold red]{intensity_str}[/bold red]"
        else:
            tag = "[yellow]STANDARD[/yellow]"
            i_styled = f"[yellow]{intensity_str}[/yellow]"

        table.add_row(
            f"+{p.hour_offset}h",
            t_str,
            i_styled,
            f"{p.renewable_percentage:.1f}%",
            f"{p.solar_generation_mw:,.0f}",
            f"{p.wind_generation_mw:,.0f}",
            f"{p.fossil_generation_mw:,.0f}",
            tag
        )

    console.print(table)

def dispatch_jobs(region_name: str = "US-CAISO"):
    region = next((r for r in GridRegion if r.value == region_name or r.name.lower() == region_name.lower()), GridRegion.CAISO)
    engine = GridEngine(region)
    forecast = engine.generate_24h_forecast()

    scheduler = CarbonScheduler(region, forecast, max_cluster_kw=100.0)
    decisions = scheduler.schedule_batch(SAMPLE_JOBS)

    console.print(Panel(
        f"[bold green]ECODISPATCH AI :: AUTONOMOUS CARBON DISPATCH EXECUTION[/bold green]\n"
        f"[cyan]Optimized Cluster Capacity:[/cyan] 100 kW | [cyan]Active Queue:[/cyan] {len(SAMPLE_JOBS)} Workloads",
        border_style="green"
    ))

    table = Table(title="Autonomous Workload Schedule & Avoided Carbon Analysis", border_style="cyan")
    table.add_column("Job ID", style="bold")
    table.add_column("Workload Name", style="white")
    table.add_column("Power", justify="right", style="dim")
    table.add_column("Scheduled Window", justify="center", style="bold cyan")
    table.add_column("Baseline CO2", justify="right", style="red")
    table.add_column("Optimized CO2", justify="right", style="green")
    table.add_column("Avoided CO2", justify="right", style="bold green")
    table.add_column("Reduction", justify="right", style="bold yellow")
    table.add_column("Avg Renew %", justify="right", style="cyan")

    for d in decisions:
        table.add_row(
            d.job_id,
            d.job_name,
            f"{d.total_energy_kwh:.1f} kWh",
            f"+{d.scheduled_start_hour}h -> +{d.scheduled_end_hour}h",
            f"{d.baseline_carbon_g/1000.0:.2f} kg",
            f"{d.optimized_carbon_g/1000.0:.2f} kg",
            f"{d.avoided_carbon_g/1000.0:.2f} kg",
            f"-{d.avoided_percentage:.1f}%",
            f"{d.average_renewable_percent:.1f}%"
        )

    console.print(table)

    accounting = CarbonAccounting(region)
    cert = accounting.generate_certificate(decisions)

    cert_card = (
        f"[bold white]ESG VERIFIABLE MITIGATION CERTIFICATE[/bold white]\n"
        f"[cyan]Certificate ID:[/cyan] {cert.certificate_id}\n"
        f"[cyan]Total Dispatched Energy:[/cyan] {cert.total_energy_consumed_kwh:,.1f} kWh\n"
        f"[cyan]Baseline Unmanaged Emissions:[/cyan] [red]{cert.baseline_emissions_kg_co2:.2f} kg CO2[/red]\n"
        f"[cyan]Optimized Dispatched Emissions:[/cyan] [green]{cert.optimized_emissions_kg_co2:.2f} kg CO2[/green]\n"
        f"[cyan]Net Avoided Atmospheric Carbon:[/cyan] [bold green]{cert.net_avoided_kg_co2:.2f} kg CO2 (-{cert.reduction_percentage:.1f}%)[/bold green]\n"
        f"[dim]SHA-256 Audit Proof: {cert.audit_hash}[/dim]"
    )
    console.print(Panel(cert_card, border_style="bold green", expand=False))

def main():
    parser = argparse.ArgumentParser(description="EcoDispatch AI: Autonomous Carbon-Aware Compute Scheduler")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    grid_p = subparsers.add_parser("grid", help="Inspect 24h regional grid carbon forecast")
    grid_p.add_argument("--region", default="US-CAISO", help="Grid region (US-CAISO, US-ERCOT, GB-UK, DE-TENNET, IN-NORTH)")

    dispatch_p = subparsers.add_parser("dispatch", help="Run autonomous carbon-aware workload dispatch")
    dispatch_p.add_argument("--region", default="US-CAISO", help="Grid region")

    args = parser.parse_args()

    if args.command == "grid":
        show_grid(args.region)
    elif args.command == "dispatch" or args.command is None:
        dispatch_jobs(getattr(args, "region", "US-CAISO"))

if __name__ == "__main__":
    main()
