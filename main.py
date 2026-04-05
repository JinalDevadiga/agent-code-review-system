#!/usr/bin/env python3
"""
Autonomous Code Review & Performance Optimization System
Main entry point for the agentic workflow system
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agents.orchestrator import WorkflowOrchestrator
from evaluation.metrics import EvaluationFramework
from utils.logger import setup_logger


logger = setup_logger(__name__)


class CodeReviewSystem:
    """Main system for code review and optimization"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the system"""
        self.orchestrator = WorkflowOrchestrator(config_path)
        self.evaluator = EvaluationFramework()
        self.results_dir = Path("data/results")
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def review_code(
        self,
        code: str,
        language: str = "python",
        full_workflow: bool = True
    ) -> Dict[str, Any]:
        """
        Review code and generate recommendations
        
        Args:
            code: Source code to review
            language: Programming language
            full_workflow: Execute full analysis->optimize->test workflow
            
        Returns:
            Complete review results with evaluation
        """
        logger.info(f"Starting code review for {language} code")
        
        if full_workflow:
            workflow_results = self.orchestrator.execute_full_workflow(code, language)
        else:
            workflow_results = self.orchestrator.execute_analysis_only(code, language)
        
        # Evaluate results
        evaluation = self.evaluator.evaluate_workflow_result(workflow_results)
        workflow_results['evaluation'] = evaluation
        
        # Save results
        self._save_results(workflow_results)
        
        logger.info(f"Code review completed. Overall score: {evaluation['overall_score']:.1f}")
        return workflow_results
    
    def compare_models(
        self,
        code: str,
        models: Optional[list] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Compare models on the same code
        
        Args:
            code: Source code to analyze
            models: List of models to compare
            language: Programming language
            
        Returns:
            Comparative analysis results
        """
        logger.info("Starting comparative model analysis")
        
        workflow_results = self.orchestrator.execute_comparative_workflow(
            code,
            models=models,
            language=language
        )
        
        # Evaluate and compare
        comparison = self.evaluator.compare_models(workflow_results)
        workflow_results['comparison'] = comparison
        
        # Save results
        self._save_results(workflow_results)
        
        logger.info("Model comparison completed")
        return workflow_results
    
    def process_file(self, file_path: str, full_workflow: bool = True) -> Dict[str, Any]:
        """
        Process a code file
        
        Args:
            file_path: Path to code file
            full_workflow: Execute full workflow
            
        Returns:
            Review results
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return {"error": "File not found"}
        
        # Detect language from extension
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust'
        }
        
        language = language_map.get(path.suffix, 'python')
        
        # Read file
        with open(path, 'r') as f:
            code = f.read()
        
        logger.info(f"Processing {file_path} ({language})")
        
        return self.review_code(code, language, full_workflow)
    
    def process_directory(
        self,
        directory: str,
        pattern: str = "*.py",
        full_workflow: bool = True
    ) -> Dict[str, Any]:
        """
        Process all files in a directory
        
        Args:
            directory: Directory path
            pattern: File pattern to match
            full_workflow: Execute full workflow
            
        Returns:
            Batch results
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"Directory not found: {directory}")
            return {"error": "Directory not found"}
        
        files = list(dir_path.glob(pattern))
        logger.info(f"Found {len(files)} files matching {pattern}")
        
        results = {
            "batch_id": f"batch_{int(datetime.now().timestamp())}",
            "directory": str(directory),
            "pattern": pattern,
            "total_files": len(files),
            "processed_files": [],
            "summary": {
                "avg_quality_score": 0.0,
                "avg_autonomy_score": 0.0,
                "total_issues": 0
            }
        }
        
        quality_scores = []
        autonomy_scores = []
        total_issues = 0
        
        for file_path in files:
            try:
                logger.info(f"Processing {file_path.name}...")
                result = self.process_file(str(file_path), full_workflow)
                
                results['processed_files'].append({
                    "file": str(file_path),
                    "success": True,
                    "evaluation": result.get('evaluation', {})
                })
                
                # Collect metrics
                evaluation = result.get('evaluation', {})
                if 'code_quality' in evaluation['metric_scores']:
                    quality_scores.append(evaluation['metric_scores']['code_quality'])
                if 'autonomy' in evaluation['metric_scores']:
                    autonomy_scores.append(evaluation['metric_scores']['autonomy'])
                
                analysis = result.get('stages', {}).get('analysis', {}).get('result', {})
                total_issues += len(analysis.get('issues', []))
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results['processed_files'].append({
                    "file": str(file_path),
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate summary
        if quality_scores:
            results['summary']['avg_quality_score'] = sum(quality_scores) / len(quality_scores)
        if autonomy_scores:
            results['summary']['avg_autonomy_score'] = sum(autonomy_scores) / len(autonomy_scores)
        results['summary']['total_issues'] = total_issues
        
        self._save_results(results)
        
        return results
    
    def _save_results(self, results: Dict[str, Any]):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determine filename
        if 'batch_id' in results:
            filename = f"batch_{timestamp}.json"
        elif 'workflow_id' in results:
            filename = f"workflow_{timestamp}.json"
        else:
            filename = f"result_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {filepath}")
    
    def generate_report(self, results_file: Optional[str] = None) -> str:
        """
        Generate a formatted report from results
        
        Args:
            results_file: Path to results JSON file
            
        Returns:
            Formatted report string
        """
        if results_file:
            with open(results_file, 'r') as f:
                results = json.load(f)
        else:
            # Use latest results
            latest = max(self.results_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
            with open(latest, 'r') as f:
                results = json.load(f)
        
        report = self._format_report(results)
        return report
    
    def _format_report(self, results: Dict[str, Any]) -> str:
        """Format results as a readable report"""
        report = []
        report.append("=" * 80)
        report.append("CODE REVIEW AND OPTIMIZATION REPORT")
        report.append("=" * 80)
        
        # Workflow info
        if 'workflow_id' in results:
            report.append(f"\nWorkflow ID: {results['workflow_id']}")
        if 'code' in results:
            code_lines = results['code'].count('\n') + 1
            report.append(f"Code Lines: {code_lines}")
        
        # Evaluation scores
        evaluation = results.get('evaluation', {})
        if evaluation:
            report.append("\n" + "=" * 40)
            report.append("EVALUATION SCORES")
            report.append("=" * 40)
            
            overall = evaluation.get('overall_score', 0)
            report.append(f"Overall Score: {overall:.1f}/100")
            
            for metric, score in evaluation.get('metric_scores', {}).items():
                report.append(f"  {metric.replace('_', ' ').title()}: {score:.1f}")
        
        # Analysis details
        analysis = results.get('stages', {}).get('analysis', {}).get('result', {})
        if analysis:
            report.append("\n" + "=" * 40)
            report.append("CODE ANALYSIS")
            report.append("=" * 40)
            
            quality_grade = analysis.get('quality_grade', 'N/A')
            quality_score = analysis.get('overall_quality_score', 'N/A')
            report.append(f"Quality Grade: {quality_grade} ({quality_score})")
            
            issues = analysis.get('issues', [])
            report.append(f"\nIssues Found: {len(issues)}")
            for issue in issues[:5]:  # Top 5 issues
                severity = issue.get('severity', 'unknown').upper()
                desc = issue.get('description', 'Unknown')
                report.append(f"  [{severity}] {desc}")
        
        # Optimization details
        optimization = results.get('stages', {}).get('optimization', {}).get('result', {})
        if optimization:
            report.append("\n" + "=" * 40)
            report.append("OPTIMIZATION RESULTS")
            report.append("=" * 40)
            
            improvement = optimization.get('improvement_summary', '')
            report.append(f"Improvement: {improvement}")
            
            size_reduction = optimization.get('size_reduction_percent', 0)
            report.append(f"Size Reduction: {size_reduction:.1f}%")
        
        # Test coverage
        tests = results.get('stages', {}).get('test_generation', {}).get('result', {})
        if tests:
            report.append("\n" + "=" * 40)
            report.append("TEST COVERAGE")
            report.append("=" * 40)
            
            coverage = tests.get('coverage_estimate', 0)
            test_count = tests.get('test_statistics', {}).get('total_test_cases', 0)
            report.append(f"Estimated Coverage: {coverage}%")
            report.append(f"Test Cases Generated: {test_count}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Autonomous Code Review & Performance Optimization System"
    )
    
    parser.add_argument(
        "--mode",
        choices=["analyze", "full", "compare", "file", "dir", "report"],
        default="full",
        help="Execution mode"
    )
    
    parser.add_argument(
        "--code",
        help="Code snippet to analyze (for inline code)"
    )
    
    parser.add_argument(
        "--file",
        help="Code file to analyze"
    )
    
    parser.add_argument(
        "--dir",
        help="Directory to analyze"
    )
    
    parser.add_argument(
        "--pattern",
        default="*.py",
        help="File pattern for directory mode"
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        help="Models to compare"
    )
    
    parser.add_argument(
        "--results-file",
        help="Results file to generate report from"
    )
    
    parser.add_argument(
        "--language",
        default="python",
        help="Programming language"
    )
    
    args = parser.parse_args()
    
    system = CodeReviewSystem()
    
    try:
        if args.mode == "full":
            if args.code:
                results = system.review_code(args.code, args.language)
                print(system._format_report(results))
            elif args.file:
                results = system.process_file(args.file)
                print(system._format_report(results))
            else:
                print("Error: Provide --code or --file for full mode")
                sys.exit(1)
        
        elif args.mode == "analyze":
            if args.code:
                results = system.review_code(args.code, args.language, full_workflow=False)
                print(system._format_report(results))
            else:
                print("Error: Provide --code for analyze mode")
                sys.exit(1)
        
        elif args.mode == "compare":
            if args.code:
                results = system.compare_models(args.code, args.models, args.language)
                print(json.dumps(results['comparison'], indent=2))
            else:
                print("Error: Provide --code for compare mode")
                sys.exit(1)
        
        elif args.mode == "file":
            if args.file:
                results = system.process_file(args.file)
                print(system._format_report(results))
            else:
                print("Error: Provide --file for file mode")
                sys.exit(1)
        
        elif args.mode == "dir":
            if args.dir:
                results = system.process_directory(args.dir, args.pattern)
                print(json.dumps(results['summary'], indent=2))
            else:
                print("Error: Provide --dir for dir mode")
                sys.exit(1)
        
        elif args.mode == "report":
            report = system.generate_report(args.results_file)
            print(report)
    
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()