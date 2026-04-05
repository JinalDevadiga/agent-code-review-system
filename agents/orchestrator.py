import json
import time
from typing import Any, Dict, List, Optional
from agents.code_analyzer import CodeAnalyzerAgent
from agents.optimizer import OptimizerAgent
from agents.test_generator import TestGeneratorAgent
import yaml


class WorkflowOrchestrator:
    """Orchestrates multi-agent workflows"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize orchestrator with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.agents = {}
        self.workflow_history = []
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agents based on configuration"""
        config = self.config
        
        # Get prompts from config
        agent_config = config.get('agents', {})
        
        # Initialize agents
        self.agents['analyzer'] = CodeAnalyzerAgent(
            model=config['models']['primary'],
            system_prompt=agent_config['code_analyzer']['system_prompt']
        )
        
        self.agents['optimizer'] = OptimizerAgent(
            model=config['models']['primary'],
            system_prompt=agent_config['optimizer']['system_prompt']
        )
        
        self.agents['test_generator'] = TestGeneratorAgent(
            model=config['models']['primary'],
            system_prompt=agent_config['test_generator']['system_prompt']
        )
    
    def execute_full_workflow(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Execute complete workflow: analyze -> optimize -> test
        
        Args:
            code: Source code to process
            language: Programming language
            
        Returns:
            Complete workflow results
        """
        workflow_start = time.time()
        workflow_id = f"workflow_{int(workflow_start)}"
        
        results = {
            "workflow_id": workflow_id,
            "timestamp": workflow_start,
            "code": code,
            "language": language,
            "stages": {}
        }
        
        try:
            # Stage 1: Code Analysis
            print("[1/3] Analyzing code...")
            analysis_result = self.agents['analyzer'].execute({
                "code": code,
                "language": language,
                "focus": "all"
            })
            
            results['stages']['analysis'] = analysis_result.to_dict()
            
            if not analysis_result.success:
                results['error'] = "Analysis failed"
                return results
            
            # Stage 2: Code Optimization
            print("[2/3] Optimizing code...")
            optimization_result = self.agents['optimizer'].execute({
                "code": code,
                "language": language,
                "analysis": analysis_result.result,
                "optimization_focus": "performance"
            })
            
            results['stages']['optimization'] = optimization_result.to_dict()
            
            if not optimization_result.success:
                results['warning'] = "Optimization failed, continuing with original code"
            
            # Stage 3: Test Generation
            print("[3/3] Generating tests...")
            test_result = self.agents['test_generator'].execute({
                "code": code,
                "language": language,
                "test_framework": "pytest"
            })
            
            results['stages']['test_generation'] = test_result.to_dict()
            
            # Calculate workflow metrics
            results['metrics'] = self._calculate_workflow_metrics(results)
            results['total_execution_time'] = time.time() - workflow_start
            
            self.workflow_history.append(results)
            return results
            
        except Exception as e:
            results['error'] = str(e)
            return results
    
    def execute_analysis_only(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute just the analysis stage"""
        result = self.agents['analyzer'].execute({
            "code": code,
            "language": language,
            "focus": "all"
        })
        
        return {
            "workflow_id": f"analysis_{int(time.time())}",
            "stages": {"analysis": result.to_dict()},
            "timestamp": time.time()
        }
    
    def execute_comparative_workflow(
        self,
        code: str,
        models: Optional[List[str]] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Execute workflow with multiple models and compare results
        
        Args:
            code: Source code to process
            models: List of models to compare (default from config)
            language: Programming language
            
        Returns:
            Comparative results across models
        """
        if models is None:
            models = [
                self.config['models']['primary'],
                self.config['models']['secondary']
            ]
        
        workflow_id = f"comparative_{int(time.time())}"
        results = {
            "workflow_id": workflow_id,
            "timestamp": time.time(),
            "code": code,
            "models": models,
            "results": {}
        }
        
        # Run workflow for each model
        for model in models:
            print(f"\nRunning workflow for {model}...")
            
            # Create model-specific agents
            analyzer = CodeAnalyzerAgent(
                model=model,
                system_prompt=self.config['agents']['code_analyzer']['system_prompt']
            )
            
            # Run analysis
            analysis = analyzer.execute({
                "code": code,
                "language": language
            })
            
            results['results'][model] = {
                "analysis": analysis.to_dict(),
                "metrics": analyzer.get_metrics()
            }
        
        # Compare results
        results['comparison'] = self._compare_model_results(results['results'])
        
        return results
    
    def _calculate_workflow_metrics(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall workflow metrics"""
        metrics = {}
        stages = workflow_results.get('stages', {})
        
        # Aggregate execution time
        total_time = sum(
            stage.get('execution_time', 0)
            for stage in stages.values()
        )
        metrics['total_execution_time'] = total_time
        
        # Count stages completed
        metrics['stages_completed'] = sum(
            1 for stage in stages.values()
            if stage.get('success', False)
        )
        
        # Extract analysis quality score
        analysis = stages.get('analysis', {})
        if analysis.get('success'):
            quality_score = analysis.get('result', {}).get('overall_quality_score', 0)
            metrics['initial_code_quality'] = quality_score
        
        # Extract optimization impact
        optimization = stages.get('optimization', {})
        if optimization.get('success'):
            improvement = optimization.get('result', {}).get('improvement_summary', '')
            metrics['optimization_applied'] = bool(improvement)
        
        return metrics
    
    def _compare_model_results(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare results across different models"""
        comparison = {
            "models_compared": list(model_results.keys()),
            "analysis_comparison": {}
        }
        
        for model, result in model_results.items():
            analysis = result.get('analysis', {}).get('result', {})
            comparison['analysis_comparison'][model] = {
                "quality_score": analysis.get('overall_quality_score', 0),
                "issues_found": len(analysis.get('issues', [])),
                "optimization_opportunities": len(analysis.get('optimization_opportunities', []))
            }
        
        return comparison
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get all workflow execution history"""
        return self.workflow_history
    
    def get_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics for all agents"""
        return {
            agent_name: agent.get_metrics()
            for agent_name, agent in self.agents.items()
        }
    
    def reset_agents(self):
        """Reset all agent histories and metrics"""
        for agent in self.agents.values():
            agent.clear_history()
            agent.llm.reset_metrics()
        self.workflow_history = []
