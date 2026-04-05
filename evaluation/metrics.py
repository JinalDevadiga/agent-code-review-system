from typing import Any, Dict, List
from dataclasses import dataclass
import json


@dataclass
class EvaluationScore:
    """Structure for evaluation scores"""
    metric_name: str
    score: float  # 0-100
    weight: float = 1.0
    description: str = ""
    details: Dict[str, Any] = None


class MetricsCalculator:
    """Calculate custom evaluation metrics"""
    
    @staticmethod
    def calculate_code_quality_score(analysis: Dict[str, Any]) -> float:
        """
        Calculate code quality score based on analysis
        
        Factors:
        - Complexity (0-100)
        - Readability (0-100)
        - Maintainability (0-100)
        - Issue severity
        """
        metrics = analysis.get('quality_metrics', {})
        
        complexity = metrics.get('complexity', 50)
        readability = metrics.get('readability', 50)
        maintainability = metrics.get('maintainability', 50)
        
        # Higher complexity is worse
        complexity_score = 100 - complexity
        
        # Average the metrics
        base_score = (complexity_score + readability + maintainability) / 3
        
        # Penalize for issues
        issues = analysis.get('issues', [])
        critical_issues = len([i for i in issues if i.get('severity') == 'critical'])
        high_issues = len([i for i in issues if i.get('severity') == 'high'])
        
        penalty = (critical_issues * 10) + (high_issues * 5)
        final_score = max(0, base_score - penalty)
        
        return min(100, final_score)
    
    @staticmethod
    def calculate_autonomy_score(
        execution_results: Dict[str, Any],
        required_interventions: int = 0
    ) -> float:
        """
        Calculate autonomy score
        
        Factors:
        - Successful completion without intervention
        - Error recovery
        - Decision making quality
        """
        base_score = 100.0
        
        # Penalize for each intervention needed
        intervention_penalty = required_interventions * 10
        base_score -= intervention_penalty
        
        # Check for errors
        if not execution_results.get('success', False):
            base_score -= 25
        
        # Check execution time stability
        execution_time = execution_results.get('execution_time', 0)
        if execution_time > 60:  # More than 60 seconds
            base_score -= 10
        
        return max(0, min(100, base_score))
    
    @staticmethod
    def calculate_optimization_impact(
        original_analysis: Dict[str, Any],
        optimized_analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate optimization impact percentage
        
        Factors:
        - Code quality improvement
        - Complexity reduction
        - Size reduction
        """
        original_quality = original_analysis.get('overall_quality_score', 50)
        optimized_quality = optimized_analysis.get('overall_quality_score', 50)
        
        quality_improvement = optimized_quality - original_quality
        
        # Code size reduction
        size_reduction = optimized_analysis.get('size_reduction_percent', 0)
        
        # Overall impact
        impact = (quality_improvement + size_reduction) / 2
        
        return min(100, max(0, 50 + impact))
    
    @staticmethod
    def calculate_consistency_score(
        results_list: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate consistency score across multiple runs
        
        Factors:
        - Agreement between results
        - Score variance
        - Decision consistency
        """
        if len(results_list) < 2:
            return 100.0
        
        scores = [r.get('score', 0) for r in results_list if 'score' in r]
        
        if not scores:
            return 100.0
        
        # Calculate variance
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Convert std dev to consistency score
        # Lower std dev = higher consistency
        consistency = 100 - min(100, std_dev * 10)
        
        return consistency
    
    @staticmethod
    def calculate_test_coverage_score(
        test_results: Dict[str, Any],
        code_analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate test coverage and effectiveness
        
        Factors:
        - Coverage percentage
        - Test count
        - Edge case coverage
        """
        coverage = test_results.get('coverage_estimate', 0)
        test_count = test_results.get('test_statistics', {}).get('total_test_cases', 0)
        edge_cases = len(test_results.get('edge_cases_covered', []))
        
        # Coverage is primary factor
        coverage_score = coverage
        
        # Bonus for adequate test count
        test_bonus = min(20, test_count * 2)
        
        # Bonus for edge case coverage
        edge_bonus = min(10, edge_cases * 2)
        
        final_score = coverage_score + test_bonus + edge_bonus
        
        return min(100, final_score)
    
    @staticmethod
    def calculate_model_comparison_score(
        results_dict: Dict[str, Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Compare scores across different models
        
        Returns:
        Dict of model -> overall_score
        """
        comparison = {}
        
        for model, result in results_dict.items():
            analysis = result.get('analysis', {}).get('result', {})
            
            # Get individual metrics
            quality = analysis.get('overall_quality_score', 0)
            issue_count = len(analysis.get('issues', []))
            suggestions = len(analysis.get('improvements_suggested', []))
            
            # Calculate composite score
            # Higher quality is better, fewer issues is better
            issue_penalty = min(30, issue_count * 2)
            suggestion_bonus = min(10, suggestions)
            
            overall = quality - issue_penalty + suggestion_bonus
            comparison[model] = min(100, max(0, overall))
        
        return comparison


class EvaluationFramework:
    """Complete evaluation framework for agentic workflows"""
    
    def __init__(self):
        self.metrics_calculator = MetricsCalculator()
        self.evaluation_history = []
    
    def evaluate_workflow_result(
        self,
        workflow_result: Dict[str, Any],
        config: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Comprehensively evaluate a workflow result
        
        Args:
            workflow_result: Complete workflow output
            config: Metric weights (from config.yaml)
            
        Returns:
            Detailed evaluation report
        """
        if config is None:
            config = {
                'correctness': 0.4,
                'clarity': 0.2,
                'completeness': 0.2,
                'practicality': 0.15,
                'innovation': 0.05
            }
        
        evaluation = {
            "workflow_id": workflow_result.get('workflow_id'),
            "timestamp": workflow_result.get('timestamp'),
            "metric_scores": {},
            "weighted_scores": {},
            "overall_score": 0.0
        }
        
        stages = workflow_result.get('stages', {})
        
        # 1. Code Quality Score
        analysis_stage = stages.get('analysis', {})
        if analysis_stage.get('success'):
            quality_score = self.metrics_calculator.calculate_code_quality_score(
                analysis_stage.get('result', {})
            )
            evaluation['metric_scores']['code_quality'] = quality_score
        
        # 2. Autonomy Score
        autonomy_score = self.metrics_calculator.calculate_autonomy_score(
            workflow_result,
            required_interventions=0
        )
        evaluation['metric_scores']['autonomy'] = autonomy_score
        
        # 3. Optimization Impact
        optimization_stage = stages.get('optimization', {})
        if optimization_stage.get('success') and analysis_stage.get('success'):
            impact_score = self.metrics_calculator.calculate_optimization_impact(
                analysis_stage.get('result', {}),
                optimization_stage.get('result', {})
            )
            evaluation['metric_scores']['optimization_impact'] = impact_score
        
        # 4. Test Coverage
        test_stage = stages.get('test_generation', {})
        if test_stage.get('success') and analysis_stage.get('success'):
            coverage_score = self.metrics_calculator.calculate_test_coverage_score(
                test_stage.get('result', {}),
                analysis_stage.get('result', {})
            )
            evaluation['metric_scores']['test_coverage'] = coverage_score
        
        # Calculate weighted overall score
        total_weight = sum(config.values())
        weighted_sum = 0
        
        for metric_name, score in evaluation['metric_scores'].items():
            # Map metric name to config key
            weight = config.get(metric_name, 0) / total_weight
            weighted_score = score * weight
            evaluation['weighted_scores'][metric_name] = weighted_score
            weighted_sum += weighted_score
        
        evaluation['overall_score'] = weighted_sum
        
        self.evaluation_history.append(evaluation)
        return evaluation
    
    def compare_models(
        self,
        comparative_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare evaluation results across models"""
        model_results = comparative_results.get('results', {})
        comparison = self.metrics_calculator.calculate_model_comparison_score(
            model_results
        )
        
        return {
            "workflow_id": comparative_results.get('workflow_id'),
            "model_comparison": comparison,
            "best_model": max(comparison, key=comparison.get) if comparison else None,
            "scores": comparison,
            "recommendations": self._generate_recommendations(comparison)
        }
    
    def _generate_recommendations(self, comparison: Dict[str, float]) -> List[str]:
        """Generate recommendations based on evaluation"""
        recommendations = []
        
        if not comparison:
            return recommendations
        
        best_model = max(comparison, key=comparison.get)
        worst_model = min(comparison, key=comparison.get)
        
        best_score = comparison[best_model]
        worst_score = comparison[worst_model]
        gap = best_score - worst_score
        
        if gap > 20:
            recommendations.append(
                f"Significant performance gap ({gap:.1f} points). "
                f"Consider using {best_model} for this task."
            )
        
        if best_score < 70:
            recommendations.append(
                "Overall scores are low. Consider improving prompts or agent design."
            )
        
        return recommendations
