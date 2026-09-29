import argparse
import sys
import json
from agent.orchestrator import AutonomousAgentOrchestrator

def main():
    parser = argparse.ArgumentParser(description="🤖 Autonomous Coding Agent — Inspired by Open-SWE")
    parser.add_argument("--prompt", "-p", type=str, help="Natural language project requirement prompt")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output directory path")
    args = parser.parse_args()

    prompt = args.prompt
    if not prompt:
        print("🤖 Autonomous Coding Agent (Interactive Mode)")
        prompt = input("Enter project requirement (e.g., 'Build a student management API using Python + SQLite'): ")

    if not prompt.strip():
        print("Error: Prompt cannot be empty.")
        sys.exit(1)

    print("\n🚀 Launching 10-Phase Autonomous Engineering Pipeline...")
    orchestrator = AutonomousAgentOrchestrator()
    results = orchestrator.run_pipeline(prompt, target_dir=args.output)

    print("\n" + "="*60)
    print("🎉 PIPELINE EXECUTION SUMMARY")
    print("="*60)
    for log in results["phase_logs"]:
        print(f"  {log}")

    print(f"\n📂 Project Location: {results['project_directory']}")
    print(f"📦 Release Archive: {results['delivery']['release_archive']}")
    print(f"⭐ Quality Score: {results['quality_score']}/100")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
