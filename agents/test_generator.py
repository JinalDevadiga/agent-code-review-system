import json
import time
from typing import Any, Dict
from agents.base_agent import BaseAgent, AgentResult


class TestGeneratorAgent(BaseAgent):
    """Generates comprehensive test cases"""
    
    def __init__(self, model: str, system_prompt: str):
        super().__init__(model, system_prompt)
    
    def execute(self, task: Dict[str, Any]) -> AgentResult:
        """
        Generate test cases for code
        
        Expected task keys:
        - code: source code to test
        - language: programming language (optional)
        - test_framework: which framework to use (optional)
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
            framework = task.get("test_framework", "pytest")
            
            # Build test generation prompt
            test_prompt = self._build_test_prompt(code, language, framework)
            
            # Call LLM
            llm_response = self._call_llm(
                user_message=test_prompt,
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
            
            # Enrich test results
            tests = self._enrich_tests(content, code)
            
            result = self._create_result(
                success=True,
                result=tests,
                execution_time=time.time() - start_time,
                tokens_used=llm_response.get("usage", {}).get("output_tokens", 0),
                metadata={
                    "language": language,
                    "framework": framework,
                    "llm_model": self.model
                }
            )
            
            self.execution_history.append(result)
            return result
            
        except Exception as e:
            return self._create_result(
                success=False,
                result={},
                error=f"Test generation failed: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def _build_test_prompt(self, code: str, language: str, framework: str) -> str:
        """Build test generation prompt"""
        prompt = f"""Generate comprehensive test cases for the following {language} code using {framework}:

```{language}
{code}
```

Provide tests in JSON format with these keys:
- test_cases: list of test cases (each with 'name', 'code', 'description', 'type' [unit/edge/integration])
- coverage_estimate: estimated code coverage percentage
- edge_cases_covered: list of edge cases addressed
- test_categories: types of tests included
- test_summary: brief summary of test strategy
- potential_improvements: suggestions for additional tests

Respond ONLY with valid JSON, no markdown formatting."""
        return prompt
    
    def _enrich_tests(self, tests: Dict[str, Any], code: str) -> Dict[str, Any]:
        """Enrich test generation results"""
        try:
            test_cases = tests.get('test_cases', [])
            tests['test_statistics'] = {
                'total_test_cases': len(test_cases),
                'unit_tests': len([t for t in test_cases if t.get('type') == 'unit']),
                'edge_case_tests': len([t for t in test_cases if t.get('type') == 'edge']),
                'integration_tests': len([t for t in test_cases if t.get('type') == 'integration']),
                'total_test_code_length': sum(len(t.get('code', '')) for t in test_cases)
            }
            
            # Calculate quality metric
            coverage = tests.get('coverage_estimate', 0)
            test_quality = min(100, coverage + (len(test_cases) * 2))
            tests['test_quality_score'] = min(100, test_quality)
            
        except Exception as e:
            tests['enrichment_error'] = str(e)
        
        return tests
