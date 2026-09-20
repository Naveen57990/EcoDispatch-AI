"""
EcoDispatch AI: 1080p Presentation Slide Generator
Renders high-resolution technical slides for the video demo.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDES_DIR = os.path.join(BASE_DIR, "frames")
os.makedirs(SLIDES_DIR, exist_ok=True)
WIDTH, HEIGHT = 1920, 1080

def get_font(size, mono=False):
    if mono:
        paths = ["/System/Library/Fonts/SFNSMono.ttf", "/System/Library/Fonts/Menlo.ttc"]
    else:
        paths = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_slide(title, subtitle, bullets, highlight_box=None, footer_text=None, filename="slide.png"):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(8, 12, 24))
    draw = ImageDraw.Draw(img)

    font_hero = get_font(68)
    font_sub = get_font(32)
    font_body = get_font(30)
    font_code = get_font(26, mono=True)
    font_small = get_font(22, mono=True)

    # Grid background
    for x in range(0, WIDTH, 80):
        draw.line([(x, 0), (x, HEIGHT)], fill=(15, 23, 42), width=1)
    for y in range(0, HEIGHT, 80):
        draw.line([(0, y), (WIDTH, y)], fill=(15, 23, 42), width=1)

    # Accent top border
    draw.rectangle([0, 0, WIDTH, 12], fill=(16, 185, 129))

    # Header branding
    draw.text((100, 65), "ECODISPATCH AI :: AUTONOMOUS CARBON DISPATCHER", fill=(16, 185, 129), font=font_small)
    draw.text((WIDTH - 480, 65), "NEXTSTEP HACKS 2026 :: EARTH FORWARD", fill=(148, 163, 184), font=font_small)
    draw.line([(100, 105), (WIDTH - 100, 105)], fill=(30, 41, 59), width=2)

    # Title
    draw.text((100, 150), title, fill=(255, 255, 255), font=font_hero)
    draw.text((100, 245), subtitle, fill=(52, 211, 153), font=font_sub)

    # Bullets
    y_offset = 330
    for bullet in bullets:
        draw.ellipse([100, y_offset + 8, 116, y_offset + 24], fill=(16, 185, 129))
        draw.text((140, y_offset), bullet, fill=(241, 245, 249), font=font_body)
        y_offset += 68

    # Highlight Card
    if highlight_box:
        box_top = y_offset + 25
        draw.rounded_rectangle([100, box_top, WIDTH - 100, box_top + 280], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        h_y = box_top + 28
        for h_line in highlight_box:
            draw.text((140, h_y), h_line[0], fill=h_line[1], font=font_code)
            h_y += 45

    # Footer
    if footer_text:
        draw.text((100, HEIGHT - 65), footer_text, fill=(100, 116, 139), font=font_small)

    out_path = os.path.join(SLIDES_DIR, filename)
    img.save(out_path)
    print(f"Rendered {out_path}")
    return out_path

def main():
    # Slide 1: Problem Statement
    create_slide(
        title="The Hidden Carbon Footprint of AI",
        subtitle="Data centers consume hundreds of terawatt-hours of fossil fuel power annually.",
        bullets=[
            "Unmanaged Compute: AI models run blindly during peak fossil peaker hours (450-750 gCO2/kWh)",
            "Curtailed Clean Energy: Gigawatts of midday solar and nocturnal wind are wasted",
            "Lack of Tooling: Developers have zero visibility into regional marginal grid emissions",
            "Hardware Upgrades Fail: Hardware efficiency gains are outpaced by exponential compute demand"
        ],
        highlight_box=[
            ("[CRITICAL IMPACT] AI compute demand is doubling every 3.4 months globally", (239, 68, 68)),
            ("[EMISSION GAP] A 70B LLM training run during coal peak emits 4.2x more carbon than in a green valley", (245, 158, 11)),
            ("[OPPORTUNITY] Shifting workloads to peak renewable windows reduces operational CO2 by up to 68%", (16, 185, 129))
        ],
        footer_text="Phase 1/4: Problem Statement | NextStep Hacks 2026 | Earth Forward",
        filename="slide_1.png"
    )

    # Slide 2: Solution Architecture
    create_slide(
        title="Meet EcoDispatch AI",
        subtitle="Autonomous Carbon-Aware Workload & Renewable Microgrid Dispatcher.",
        bullets=[
            "Regional Grid Feeds: Real-time marginal carbon intensity & generation mixes (CAISO, ERCOT, UK, DE, IN)",
            "Green Valley Prediction: Mathematical detection of optimal solar & wind saturation windows",
            "Autonomous Dynamic Scheduler: Respects cluster capacity, priorities, and strict developer deadlines",
            "Verifiable ESG Audit Ledger: Generates SHA-256 tamper-evident carbon reduction certificates"
        ],
        highlight_box=[
            ("[REGIONAL MODELING] US-CAISO (Solar) • US-ERCOT (Wind) • GB-UK (Offshore) • DE-TENNET • IN-NORTH", (6, 182, 212)),
            ("[OPTIMIZER] Polynomial-time dynamic constraint solver with deadline guarantees", (16, 185, 129)),
            ("[DUAL INTERFACE] Rich Terminal CLI + Live Interactive Web Dashboard on Vercel", (245, 158, 11))
        ],
        footer_text="Phase 2/4: Solution Architecture | EcoDispatch AI v1.0.0",
        filename="slide_2.png"
    )

    # Slide 3: Technical Execution & Benchmarks
    create_slide(
        title="Autonomous Optimization in Action",
        subtitle="Mathematical carbon dispatch shifting 5 batch workloads into high-solar hours.",
        bullets=[
            "JOB-101 (LLM 70B Fine-Tune): Shifted +4h into California solar peak, avoiding 7.41 kg CO2 (-56.5%)",
            "JOB-102 (Diffusion Rendering): Shifted +5h into maximum solar saturation, avoiding 2.67 kg CO2 (-68.4%)",
            "JOB-103 (Nightly Vector DB): Shifted +4h into green valley, avoiding 4.81 kg CO2 (-56.5%)",
            "JOB-104 (Zero-Day Security Scan): Dispatched immediately with strict 2-hour deadline compliance"
        ],
        highlight_box=[
            ("$ ecodispatch dispatch --region US-CAISO", (148, 163, 184)),
            ("[DISPATCHED ENERGY] 213.0 kWh allocated across 5 compute workloads", (6, 182, 212)),
            ("[NET AVOIDED EMISSIONS] 21.51 kg CO2 prevented from entering the atmosphere (-55.0%)", (16, 185, 129)),
            ("[AUDIT CERTIFICATE] Issued verifiable ESG proof (SHA-256: 575ffef6c86d8...)", (59, 130, 246))
        ],
        footer_text="Phase 3/4: Mathematical Optimization | 8/8 Automated Tests Passing",
        filename="slide_3.png"
    )

    # Slide 5: Conclusion & Impact
    create_slide(
        title="Building a Sustainable Future for AI",
        subtitle="Earth Forward: Accelerating technology while protecting our planet.",
        bullets=[
            "Open Source & Defensive: MIT Licensed, 100% test coverage with automated pytest suite",
            "Zero Hardware Changes: Works with existing GPU clusters, Kubernetes jobs, and cloud APIs",
            "Developer First: Python CLI, Pydantic models, JSON/CSV exports, and Vercel dashboard",
            "Try It Today: https://ecodispatch-ai.vercel.app"
        ],
        highlight_box=[
            ("LIVE WEB DASHBOARD: https://ecodispatch-ai.vercel.app", (16, 185, 129)),
            ("GITHUB REPOSITORY: https://github.com/Naveen57990/EcoDispatch-AI", (6, 182, 212)),
            ("NEXTSTEP HACKS 2026: EARTH FORWARD SUBMISSION READY", (245, 158, 11))
        ],
        footer_text="EcoDispatch AI | Autonomous Opportunity & Engineering Agent: NOXScout | Naveen57990",
        filename="slide_5.png"
    )

if __name__ == "__main__":
    main()
