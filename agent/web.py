import os
import sys
import json
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from agent.orchestrator import AutonomousAgentOrchestrator

app = FastAPI(title="🤖 Autonomous Coding Agent Dashboard", version="1.0.0")

class PipelineRequest(BaseModel):
    prompt: str
    target_dir: Optional[str] = None

orchestrator = AutonomousAgentOrchestrator()

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Autonomous Coding Agent</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-color: #38bdf8;
            --text-color: #f8fafc;
            --subtext: #94a3b8;
            --success: #4ade80;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 40px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.5rem;
            color: var(--accent-color);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .card {
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            margin-bottom: 24px;
            border: 1px solid #334155;
        }
        textarea {
            width: 100%;
            height: 100px;
            background: #0f172a;
            border: 1px solid #334155;
            color: #fff;
            padding: 14px;
            border-radius: 8px;
            font-size: 1rem;
            box-sizing: border-box;
        }
        button {
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            color: #000;
            font-weight: 700;
            border: none;
            padding: 14px 28px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 12px;
            transition: all 0.2s ease;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(56, 189, 248, 0.4);
        }
        .log-box {
            background: #090d16;
            padding: 16px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.9rem;
            color: #38bdf8;
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #1e293b;
        }
        .phase-item {
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .phase-item::before {
            content: "➔";
            color: var(--success);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Autonomous Coding Agent</h1>
        <p style="color: var(--subtext);">Input your project requirement and let the agent autonomously plan, code, test, fix, and deliver your project.</p>
        
        <div class="card">
            <h3>Project Requirement Prompt</h3>
            <textarea id="promptInput" placeholder="e.g. Build a student management API using Python + SQLite"></textarea>
            <button onclick="runAgent()">🚀 Run Autonomous Pipeline</button>
        </div>

        <div class="card">
            <h3>Pipeline Progress Logs</h3>
            <div id="logBox" class="log-box">Ready to launch...</div>
        </div>
    </div>

    <script>
        async function runAgent() {
            const prompt = document.getElementById('promptInput').value;
            const logBox = document.getElementById('logBox');
            if(!prompt.trim()) return alert("Please enter a prompt!");

            logBox.innerHTML = "<div class='phase-item'>⏳ Initializing 10-Phase Pipeline...</div>";
            try {
                const res = await fetch('/api/run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: prompt})
                });
                const data = await res.json();

                let html = "";
                data.phase_logs.forEach(log => {
                    html += `<div class='phase-item'>${log}</div>`;
                });
                html += `<br><div style='color: var(--success); font-weight: bold;'>🎉 Delivery Complete! Location: ${data.project_directory}</div>`;
                html += `<div style='color: #fbbf24;'>⭐ Quality Score: ${data.quality_score}/100</div>`;
                logBox.innerHTML = html;
            } catch(e) {
                logBox.innerHTML = `<div style='color: #ef4444;'>❌ Error: ${e.message}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_DASHBOARD

@app.post("/api/run")
def run_pipeline_api(req: PipelineRequest):
    try:
        results = orchestrator.run_pipeline(req.prompt, target_dir=req.target_dir)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🌐 Starting Autonomous Coding Agent Web Dashboard at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
