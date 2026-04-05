import json
import time
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent, AgentResult


class CodeAnalyzerAgent(BaseAgent):
    """Analyzes code for issues, complexity, and improvements"""
    
    def __init__(self, model: str, system_prompt: str):
        super().__init__(model, system_prompt)
        self.analysis_cache = {}
        
    def execute(self, task: Dict[str, Any]) -> AgentResult:
        """
        Analyze provided code
        
        Expected task keys:
        - code: source code to analyze
        - language: programming language (optional)
        - focus: areas to focus on (optional)
        """
        start_time = time.time()
        
        try:
            code = task.get("code")
            if not code:
                return self._create_result(
                    success=False,
                    result={},
                    error="No code provided in task",
                    execution_time=time.time() - start_time
                )
            
            language = task.get("language", "python")
            focus = task.get("focus", "all")
            
            # Create analysis prompt
            analysis_prompt = self._build_analysis_prompt(code, language, focus)
            
            # Call LLM
            llm_response = self._call_llm(
                user_message=analysis_prompt,
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
            
            # Enrich analysis
            analysis = self._enrich_analysis(content, code)
            
            # Store in cache
            self.analysis_cache[hash(code)] = analysis
            
            result = self._create_result(
                success=True,
                result=analysis,
                execution_time=time.time() - start_time,
                tokens_used=llm_response.get("usage", {}).get("output_tokens", 0),
                metadata={
                    "language": language,
                    "focus": focus,
                    "code_length": len(code),
                    "llm_model": self.model
                }
            )
            
            self.execution_history.append(result)
            return result
            
        except Exception as e:
            return self._create_result(
                success=False,
                result={},
                error=f"Analysis failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _build_analysis_prompt(self, code: str, language: str, focus: str) -> str:
        """Build the analysis prompt"""
        prompt = f"""Analyze the following {language} code:

```{language}
{code}
```

Focus on: {focus}

Provide a comprehensive analysis in JSON format with these keys:
- issues: list of issues found (each with 'description', 'severity' [critical/high/medium/low], 'line_reference')
- quality_metrics: object with 'complexity' (0-100), 'readability' (0-100), 'maintainability' (0-100)
- overall_quality_score: 0-100
- strengths: list of code strengths
- weaknesses: list of weaknesses
- improvements_suggested: list of specific improvements with reasoning
- optimization_opportunities: list of optimization chances with estimated impact
- security_concerns: list of security issues if any

Respond ONLY with valid JSON, no markdown formatting."""
        return prompt
    
    def _enrich_analysis(self, analysis: Dict[str, Any], code: str) -> Dict[str, Any]:
        """Enrich analysis with computed metrics"""
        try:
            # Add code statistics
            lines = code.split('\n')
            analysis['code_statistics'] = {
                'total_lines': len(lines),
                'non_empty_lines': len([l for l in lines if l.strip()]),
                'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
                'characters': len(code)
            }
            
            # Compute quality grade
            quality_score = analysis.get('overall_quality_score', 0)
            if quality_score >= 90:
                grade = 'A'
            elif quality_score >= 80:
                grade = 'B'
            elif quality_score >= 70:
                grade = 'C'
            elif quality_score >= 60:
                grade = 'D'
            else:
                grade = 'F'
            
            analysis['quality_grade'] = grade
            
        except Exception as e:
            analysis['enrichment_error'] = str(e)
        
        return analysis
