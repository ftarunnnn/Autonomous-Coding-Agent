import os
from typing import Dict, Any, Tuple
from agent.models.task_spec import TaskSpec
from agent.models.architecture_plan import ArchitecturePlan
from agent.models.execution_result import ExecutionResult
from agent.models.quality_report import QualityReport
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner
from agent.phase4_codegen.generator import CodeGenerator
from agent.phase5_execution.sandbox import SandboxExecutionEngine
from agent.phase6_testing.tester import AutomatedTester
from agent.phase7_self_fixing.repair_loop import ErrorRepairLoop
from agent.phase8_quality.quality_checker import QualityAndSecurityChecker
from agent.phase9_documentation.doc_builder import DocumentationBuilder
from agent.phase10_delivery.packager import FinalDeliveryPackager

class AutonomousAgentOrchestrator:
    """
    Master Core Autonomous Loop Engine (Phase 1 -> Phase 10).
    Requirement -> Plan -> Code -> Execute -> Test -> Error -> Fix -> Quality -> Docs -> Deliver
    """

    def __init__(self, workspace_root: str = "generated_projects"):
        self.workspace_root = workspace_root
        self.parser = RequirementInputParser()
        self.analyzer = RequirementAnalyzer()
        self.planner = ProjectPlanner()
        self.generator = CodeGenerator()
        self.sandbox = SandboxExecutionEngine()
        self.tester = AutomatedTester()
        self.repair_loop = ErrorRepairLoop()
        self.quality_checker = QualityAndSecurityChecker()
        self.doc_builder = DocumentationBuilder()
        self.packager = FinalDeliveryPackager()

    def run_pipeline(self, prompt: str, target_dir: str = None) -> Dict[str, Any]:
        """
        Executes all 10 project phases end-to-end.
        """
        results = {"status": "in_progress", "phase_logs": []}

        # Phase 1: Requirement Input
        spec: TaskSpec = self.parser.parse(prompt)
        results["phase_logs"].append("Phase 1 Complete: Requirement parsed into TaskSpec.")

        # Phase 2: Requirement Analysis
        spec, clarifications = self.analyzer.analyze(spec)
        results["phase_logs"].append(f"Phase 2 Complete: Features & Entity schemas extracted ({len(spec.metadata.get('entities', []))} entities).")

        # Set target directory
        if not target_dir:
            target_dir = os.path.join(self.workspace_root, spec.project_name)
        os.makedirs(target_dir, exist_ok=True)

        # Phase 3: Project Planning
        plan: ArchitecturePlan = self.planner.plan(spec, target_dir=target_dir)
        results["phase_logs"].append(f"Phase 3 Complete: Architecture blueprint generated ({len(plan.file_manifest)} files planned).")

        # Phase 4: Code Generation
        generated_files = self.generator.generate_project(spec, plan, output_dir=target_dir)
        results["phase_logs"].append(f"Phase 4 Complete: Code generated for {len(generated_files)} files.")

        # Phase 5: Code Execution & Sandbox
        self.sandbox.install_dependencies(target_dir)
        build_res = self.sandbox.verify_build(target_dir, primary_language=spec.primary_language)
        results["phase_logs"].append(f"Phase 5 Complete: Sandbox build verification (exit code {build_res.exit_code}).")

        # Phase 6: Automated Testing
        self.tester.generate_tests(spec, target_dir)
        test_res: ExecutionResult = self.tester.run_tests(target_dir, self.sandbox)
        results["phase_logs"].append(f"Phase 6 Complete: Tests executed ({test_res.passed_tests} passed, {test_res.failed_tests} failed).")

        # Phase 7: Error Analysis & Self-Fixing
        if not test_res.success:
            healed, diagnostics = self.repair_loop.diagnose_and_fix(
                target_dir, test_res, lambda p: self.tester.run_tests(p, self.sandbox)
            )
            results["phase_logs"].append(f"Phase 7 Complete: Self-repair loop finished (Healed: {healed}).")
        else:
            results["phase_logs"].append("Phase 7 Complete: No errors detected; repair loop bypassed.")

        # Phase 8: Code Quality & Security
        quality_report: QualityReport = self.quality_checker.audit_project(target_dir)
        results["phase_logs"].append(f"Phase 8 Complete: Quality audit score {quality_report.score}/100.")

        # Phase 9: Documentation
        docs = self.doc_builder.generate_documentation(spec, plan, target_dir)
        results["phase_logs"].append(f"Phase 9 Complete: Documentation generated ({len(docs)} files).")

        # Phase 10: Final Delivery
        delivery = self.packager.package_delivery(target_dir)
        results["phase_logs"].append("Phase 10 Complete: Project release packaged successfully!")

        results["status"] = "success"
        results["project_directory"] = target_dir
        results["task_spec"] = spec.to_dict()
        results["quality_score"] = quality_report.score
        results["delivery"] = delivery

        return results
