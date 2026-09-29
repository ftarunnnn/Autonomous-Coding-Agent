# 🤖 Autonomous Coding Agent

An open-source, asynchronous autonomous software engineering agent inspired by **LangChain Open-SWE**.
The agent autonomously understands software requirements, plans architectures, generates full-stack code, executes code in isolated environments, runs automated tests, self-analyzes & fixes errors, inspects code quality & security vulnerabilities, generates complete documentation, and delivers production-ready project packages.

---

## 🎯 10-Phase Autonomous Engineering Pipeline

```
  ┌───────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
  │ Phase 1: Input    │ ──> │ Phase 2: Analysis    │ ──> │ Phase 3: Planning │
  └───────────────────┘     └──────────────────────┘     └───────────────────┘
                                                                   │
                                                                   ▼
  ┌───────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
  │ Phase 6: Testing  │ <── │ Phase 5: Execution   │ <── │ Phase 4: Code Gen │
  └───────────────────┘     └──────────────────────┘     └───────────────────┘
            │
            ▼
  ┌───────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
  │ Phase 7: Repair   │ ──> │ Phase 8: Quality     │ ──> │ Phase 9: Docs     │
  └───────────────────┘     └──────────────────────┘     └───────────────────┘
                                                                   │
                                                                   ▼
                                                         ┌───────────────────┐
                                                         │ Phase 10: Delivery│
                                                         └───────────────────┘
```

### 🔄 Core Autonomous Loop
`Requirement → Analysis → Architecture Plan → Code Generation → Environment Execution → Automated Testing → Error Diagnosis → Self-Fixing → Quality Check → Final Delivery`

---

## 🛠 Features Across 10 Phases

1. **Phase 1 — Requirement Input**: Parses natural language requests, CLI arguments, or JSON specs into structured `TaskSpec` instances.
2. **Phase 2 — Requirement Analysis**: Identifies features, tech stacks, database models, and generates interactive clarification questions for missing information.
3. **Phase 3 — Project Planning**: Architectures directory structures, dependency DAGs, modules, and database schemas.
4. **Phase 4 — Code Generation**: Multi-agent code writer capable of creating and editing frontend, backend, database scripts, and configurations.
5. **Phase 5 — Code Execution**: Isolated subprocess sandbox environment manager for dynamic dependency resolution and process monitoring.
6. **Phase 6 — Automated Testing**: Dynamic test suite generation (pytest/unittest/jest) and coverage execution.
7. **Phase 7 — Error Analysis & Self-Fixing**: Autonomous AST/log diagnostics repair loop with failure root-cause analysis.
8. **Phase 8 — Code Quality & Security**: Static linting, anti-pattern detection, secret scanning, and security vulnerability patching.
9. **Phase 9 — Documentation**: Automated README, OpenAPI/Swagger specifications, and setup instructions.
10. **Phase 10 — Final Delivery**: Git branch & release packager, web dashboard UI, and executable CLI runner.

---

## ⚙️ Quick Start

```bash
# Clone repository
git clone https://github.com/ftarunnnn/Autonomous-Coding-Agent.git
cd Autonomous-Coding-Agent

# Install dependencies
pip install -r requirements.txt

# Run CLI Agent
python -m agent.cli --prompt "Build a Student Management REST API with FastAPI and SQLite"

# Launch Web Dashboard
python -m agent.web
```

---

## 📜 References & Acknowledgments
- Inspired by **[langchain-ai/open-swe](https://github.com/langchain-ai/open-swe)** - Open-Source Asynchronous Coding Agent architecture.