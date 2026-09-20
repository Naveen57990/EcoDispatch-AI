# AI Disclosure & Transparency Statement — EcoDispatch AI

In accordance with hackathon ethics guidelines and transparency best practices:

### 1. Project Conception and Architecture
The problem formulation, mathematical models (marginal avoided carbon formulation $\Delta E = E_{\text{kWh}} \times (I_{\text{base}} - I_{\text{opt}})$), heuristic scheduling constraints, and multi-region grid architecture were designed and engineered specifically for NextStep Hacks 2026.

### 2. Code Implementation
- All core business logic (`ecodispatch/core/models.py`, `grid.py`, `scheduler.py`, `accounting.py`, `cli.py`), frontend interface (`web/index.html`, `web/app.js`), and automated unit tests (`tests/test_*.py`) were authored and executed locally in Python 3.12+ and modern JavaScript.
- AI pair programming assistants (Antigravity) were used for boilerplate scaffolding, rapid iteration, syntax verification, and test case expansion.

### 3. Media & Assets
- **Video Narration**: Microsoft Azure Neural Text-to-Speech (`en-IN-PrabhatNeural`) was used to generate clear, high-fidelity audio narration.
- **Visual Assets**: Visual assets including the 3D logo shield and widescreen presentation banners were generated using generative imaging tools and processed with Pillow.
- **Demo Recording**: The web demo walkthrough was captured live in real time using automated Playwright browser interaction against the live deployed Vercel application.

### 4. Open Source & Third-Party Libraries
- Pydantic v2 (BSD 3-Clause)
- Rich (MIT)
- Pytest (MIT)
- Tailwind CSS (MIT)
- FFmpeg (LGPL/GPL)
- Playwright (Apache 2.0)
