<div align="center">

# 🌱 EcoDispatch AI
### Autonomous Carbon-Aware Compute & Renewable Microgrid Dispatcher

[![Live Demo](https://img.shields.io/badge/Live%20Demo-ecodispatch--ai.vercel.app-10b981?style=for-the-badge&logo=vercel)](https://ecodispatch-ai.vercel.app)
[![NextStep Hacks 2026](https://img.shields.io/badge/NextStep%20Hacks%202026-Earth%20Forward-3b82f6?style=for-the-badge)](https://nextstep2026.devpost.com/)
[![Tests](https://img.shields.io/badge/Tests-8%2F8%20Passing-brightgreen?style=for-the-badge&logo=pytest)](https://github.com/Naveen57990/EcoDispatch-AI)
[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Shifting heavy AI model training, batch inferences, and background compute workloads into peak solar and wind energy windows to eliminate up to 68% of atmospheric carbon emissions.</b>
</p>

</div>

---

## 🌍 The Crisis: The Hidden Carbon Footprint of AI

Data centers and AI agent workloads currently consume hundreds of terawatt-hours of electricity every year. When an AI engineer kicks off an LLM fine-tuning batch or an image diffusion pipeline on an arbitrary cron schedule, they are frequently drawing power during **fossil-fuel peaker plant hours** (burning heavy gas and coal at $450\text{--}750\text{ gCO}_2\text{eq/kWh}$).

Meanwhile, during **green energy valleys** (such as midday solar peaks in California or nocturnal wind surges in Texas), clean renewable energy is often **curtailed** (wasted) because electricity demand cannot absorb the supply.

**EcoDispatch AI** bridges this gap: it functions as an autonomous, carbon-aware workload scheduler that monitors real-time regional electrical grids, predicts green valleys, and autonomously shifts non-urgent compute into peak renewable windows—slashing operational carbon by over **55%** with **zero hardware modifications**.

---

## ⚡ Key Features

* **Real-Time Regional Grid Modeling**: Models 24-hour generation mixes and marginal carbon intensity curves across global grids:
  * **US-CAISO** (California): Midday solar duck-curve peak ($65\text{ g/kWh}$).
  * **US-ERCOT** (Texas): High nocturnal wind surge ($110\text{ g/kWh}$).
  * **GB-UK** (Great Britain): Offshore wind and nuclear baseload ($90\text{ g/kWh}$).
  * **DE-TENNET** (Germany): European renewable cross-border flows ($120\text{ g/kWh}$).
  * **IN-NORTH** (India): Northern regional solar dispatch ramp ($280\text{ g/kWh}$).
* **Dynamic Workload Constraint Optimizer**: Evaluates job execution durations, cluster capacity limits (e.g. 100 kW ceiling), and strict developer deadlines using polynomial-time dynamic scheduling.
* **Verifiable Carbon Accounting Ledger**: Computes exact marginal avoided emissions ($\Delta CO_2$) and issues cryptographic **SHA-256 ESG Compliance Certificates**.
* **Dual Interface**:
  * **Terminal CLI**: Rich tables, generation curves, and ASCII energy monitors.
  * **Interactive Web Dashboard**: Live SVG timeline graphs, workload simulator, and one-click JSON/CSV audit exports deployed on Vercel at [https://ecodispatch-ai.vercel.app](https://ecodispatch-ai.vercel.app).

---

## 📐 Mathematical Formulation

### 1. Marginal Carbon Intensity Calculation
For any hour $t \in [0, 24)$, grid carbon intensity $I(t)$ is calculated as a function of thermal generation ratio:

$$I(t) = I_{\text{clean}} + (I_{\text{peak}} - I_{\text{clean}}) \cdot \left(\frac{P_{\text{fossil}}(t)}{P_{\text{total}}(t)}\right)^{1.4}$$

### 2. Avoided Emission Accounting
Given a compute workload drawing $P_{\text{kW}}$ over duration $D$:

$$\text{Baseline Emissions: } E_{\text{baseline}} = \sum_{h=0}^{D-1} P_{\text{kW}} \times I(h)$$

$$\text{Optimized Emissions: } E_{\text{opt}} = \min_{s \in [0, \text{Deadline}-D]} \sum_{h=s}^{s+D-1} P_{\text{kW}} \times I(h)$$

$$\text{Net Avoided Carbon: } \Delta CO_2 = E_{\text{baseline}} - E_{\text{opt}}$$

$$\text{Carbon Reduction Percentage: } R\% = \left(\frac{\Delta CO_2}{E_{\text{baseline}}}\right) \times 100\%$$

---

## 🚀 Quickstart & Installation

```bash
# Clone the repository
git clone https://github.com/Naveen57990/EcoDispatch-AI.git
cd EcoDispatch-AI

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install rich pydantic pytest
```

### Inspect 24-Hour Regional Grid Forecast
```bash
python ecodispatch/cli.py grid --region US-CAISO
```

### Run Autonomous Workload Dispatch
```bash
python ecodispatch/cli.py dispatch --region US-CAISO
```

---

## 📊 Benchmark Execution & CLI Output

```text
╭──────────────────────────────────────────────────────────────────────────────╮
│ ECODISPATCH AI :: AUTONOMOUS CARBON DISPATCH EXECUTION                       │
│ Optimized Cluster Capacity: 100 kW | Active Queue: 5 Workloads               │
╰──────────────────────────────────────────────────────────────────────────────╯
             Autonomous Workload Schedule & Avoided Carbon Analysis             
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ Job ID ┃ Name   ┃  Power ┃ Window ┃  Base  ┃  Opt  ┃Avoided ┃ Redu% ┃ Renew% ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ JOB-104│ SecAud │ 6.0kWh │+1h->+2h│ 1.79kg │1.13kg │ 0.66kg │ -36.9%│  56.4% │
│ JOB-101│ LLM-70B│ 74.0kWh│+4h->+8h│13.11kg │5.71kg │ 7.41kg │ -56.5%│  91.7% │
│ JOB-102│ Diffus │ 16.0kWh│+5h->+7h│ 3.89kg │1.23kg │ 2.67kg │ -68.4%│  92.0% │
│ JOB-103│ VecDB  │ 42.0kWh│+4h->+8h│ 8.51kg │3.70kg │ 4.81kg │ -56.5%│  91.7% │
│ JOB-105│ Synth  │ 75.0kWh│+4h->+9h│11.80kg │5.84kg │ 5.97kg │ -50.6%│  91.4% │
└────────┴────────┴────────┴────────┴────────┴───────┴────────┴───────┴────────┘
╭──────────────────────────────────────────────────────────────────────────────╮
│ ESG VERIFIABLE MITIGATION CERTIFICATE                                        │
│ Certificate ID: ECO-US-CAISO-20260920-CDAA4F                                 │
│ Total Dispatched Energy: 213.0 kWh                                           │
│ Baseline Unmanaged Emissions: 39.11 kg CO2                                   │
│ Optimized Dispatched Emissions: 17.60 kg CO2                                 │
│ Net Avoided Atmospheric Carbon: 21.51 kg CO2 (-55.0%)                        │
│ SHA-256 Audit Proof: 575ffef6c86d8dfd6eef1355c23b7af844be4d1cf610a126fda...   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## 🧪 Automated Test Suite (100% Passing)

```bash
pytest -v
```

```text
tests/test_accounting.py::test_certificate_math_and_audit_hash PASSED    [ 12%]
tests/test_accounting.py::test_csv_export PASSED                         [ 25%]
tests/test_grid.py::test_caiso_24h_forecast PASSED                       [ 37%]
tests/test_grid.py::test_ercot_wind_pattern PASSED                       [ 50%]
tests/test_grid.py::test_green_valley_identification PASSED              [ 62%]
tests/test_scheduler.py::test_deadline_enforcement PASSED                [ 75%]
tests/test_scheduler.py::test_carbon_reduction_optimization PASSED       [ 87%]
tests/test_scheduler.py::test_cluster_capacity_limit PASSED              [100%]

============================== 8 passed in 0.04s ===============================
```

---

## 🏆 NextStep Hacks 2026 Team & Submission

* **Hackathon**: [NextStep Hacks 2026](https://nextstep2026.devpost.com/)
* **Category**: Earth Forward
* **Author**: Naveen ([@Naveen57990](https://github.com/Naveen57990))
* **Autonomous Engineering Agent**: NOXScout
* **License**: MIT License
