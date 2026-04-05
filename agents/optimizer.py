import json
import time
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentResult


class OptimizerAgent(BaseAgent):
    """Generates optimized code versions"""
    
    def __init__(self, model: str, system_prompt: str):
        super().__init__(model, system_prompt)
        self.optimization_cache = {}
    
    def execute(self, task: Dict[str, Any]) -> AgentResult:
        """
        Generate optimized code
        
        Expected task keys:
        - code: source code to optimize
        - analysis: code analysis (optional, provides context)
        - optimization_focus: what to optimize for (optional)
        - language: programming language (optional)
        """
        start_time = time.time()
        
        try:
            code = task.get("code")
            if not code:
                return self._create_result(
                    success=False,
                    result={},
                    error="No code provided",
                    execution_time=time.time() - start_time
                )
            
            language = task.get("language", "python")
            analysis = task.get("analysis", {})
            focus = task.get("optimization_focus", "performance")
            
            # Create optimization prompt
            opt_prompt = self._build_optimization_prompt(code, language, analysis, focus)
            
            # Call LLM
            llm_response = self._call_llm(
                user_message=opt_prompt,
                json_mode=True,
                max_tokens=4096
            )
            
            if not llm_response.get("success"):
                return self._create_result(
                    success=False,
                    result={},
                    error=llm_response.get("error"),
                    execution_time=time.time() - start_time
                )
            
            content = llm_response.get("content")
            if isinstance(content, str):
                content = json.loads(content)
            
            # Enrich optimization result
            optimization = self._enrich_optimization(content, code)
            
            result = self._create_result(
                success=True,
                result=optimization,
                execution_time=time.time() - start_time,
                tokens_used=llm_response.get("usage", {}).get("output_tokens", 0),
                metadata={
                    "language": language,
                    "optimization_focus": focus,
                    "original_code_length": len(code),
                    "llm_model": self.model
                }
            )
            
            self.execution_history.append(result)
            return result
            
        except Exception as e:
            return self._create_result(
                success=False,
                result={},
                error=f"Optimization failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _build_optimization_prompt(
        self,
        code: str,
        language: str,
        analysis: Dict[str, Any],
        focus: str
    ) -> str:
        """Build the optimization prompt"""
        context = ""
        if analysis:
            issues = analysis.get('issues', [])
            if issues:
                context += f"\nIdentified issues:\n"
                for issue in issues[:5]:  # Top 5 issues
                    context += f"- {issue.get('description', 'Unknown')}\n"
        
        prompt = f"""Optimize the following {language} code focusing on {focus}:

```{language}
{code}
```
{context}

Provide optimization in JSON format with these keys:
- optimized_code: the improved code in a code block
- optimizations_made: list of optimizations with explanations
- complexity_analysis: object with 'original' and 'optimized' complexity descriptions
- improvement_summary: brief summary of improvements
- trade_offs: any trade-offs made in optimization
- code_quality_impact: how optimization affects code quality
- performance_metrics: estimated performance improvements as percentages

Respond ONLY with valid JSON, no markdown formatting."""
        return prompt
    
    def _enrich_optimization(self, optimization: Dict[str, Any], original_code: str) -> Dict[str, Any]:
        """Enrich optimization results"""
        try:
            optimization['code_statistics'] = {
                'original_lines': len(original_code.split('\n')),
                'optimized_lines': len(optimization.get('optimized_code', '').split('\n')),
                'original_length': len(original_code),
                'optimized_length': len(optimization.get('optimized_code', ''))
            }
            
            # Calculate size reduction
            size_reduction = (
                (len(original_code) - len(optimization.get('optimized_code', original_code)))
                / len(original_code) * 100
            ) if original_code else 0
            optimization['size_reduction_percent'] = round(size_reduction, 2)
            
        except Exception as e:
            optimization['enrichment_error'] = str(e)
        
        return optimization
