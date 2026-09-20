"""
EcoDispatch AI: Natural Neural Explanatory Narration
Synthesizes conversational Indian English voiceover with natural human cadence and breathing pauses.
"""
import asyncio
import edge_tts
import os

VOICE = "en-IN-PrabhatNeural"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECTIONS = [
    (
        "part_1_human",
        "Hey everyone! Today, AI models, data centers, and cloud infrastructure consume hundreds of terawatt-hours of electricity every single year. "
        "When developers kick off an LLM training run or batch inference without thinking, they are frequently pulling power during peak fossil-fuel grid hours, burning coal and gas. "
        "Meanwhile, gigawatts of clean solar and wind energy are routinely wasted because demand isn't aligned with the grid."
    ),
    (
        "part_2_human",
        "That's why we built EcoDispatch AI: an autonomous, carbon-aware compute dispatcher engineered for the NextStep Hacks Earth Forward challenge. "
        "It continuously monitors regional electrical grids in real time, forecasts renewable generation curves, and dynamically shifts heavy workloads into peak green energy windows."
    ),
    (
        "part_3_human",
        "Our core dispatch engine evaluates workload execution duration, cluster capacity limits, and strict developer deadlines. "
        "Using polynomial constraint optimization, it schedules jobs right into the green valleys of California solar or Texas nocturnal wind, reducing operational carbon by up to sixty-eight percent, and issuing tamper-evident SHA-256 ESG audit certificates."
    ),
    (
        "part_4_human",
        "Now, let's watch our live production dashboard in action. "
        "As we switch between regional electrical grids like CAISO and ERCOT, the dynamic twenty-four hour intensity curve recalculates in real time. "
        "When we trigger the autonomous dispatcher, you can see workloads like LLM fine-tuning and diffusion rendering shifting automatically into high-solar hours, immediately cutting carbon emissions by fifty-five percent."
    ),
    (
        "part_5_human",
        "EcoDispatch AI is completely open-source, verified with an eight out of eight passing test suite, and deployed live right now on Vercel. "
        "It proves that we don't have to choose between advancing artificial intelligence and protecting our planet. "
        "Try it out today at ecodispatch-ai.vercel.app. Thank you!"
    )
]

async def generate_audio():
    for sec_id, text in SECTIONS:
        out_file = os.path.join(BASE_DIR, f"{sec_id}.mp3")
        comm = edge_tts.Communicate(text, VOICE, rate="-4%", pitch="+0Hz")
        await comm.save(out_file)
        print(f"Generated {out_file}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
