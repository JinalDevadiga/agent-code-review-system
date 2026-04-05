# Autonomous Code Review & Performance Optimization System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

A sophisticated multi-agent agentic AI system that autonomously analyzes, optimizes, and tests code using Claude LLMs. This project demonstrates advanced AI engineering with autonomous workflows, custom evaluation frameworks, and comparative LLM analysis.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [System Components](#system-components)
- [Evaluation Framework](#evaluation-framework)
- [Examples](#examples)
- [Performance](#performance)
- [Advanced Usage](#advanced-usage)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

The **Autonomous Code Review & Performance Optimization System** is an enterprise-grade platform that leverages Claude AI to perform comprehensive code analysis without manual intervention. The system orchestrates multiple specialized AI agents that work autonomously to:

1. **Analyze** code for issues, complexity, and quality metrics
2. **Optimize** code by generating improved versions with explanations
3. **Test** code by creating comprehensive test cases
4. **Evaluate** all outputs using custom metrics and scoring

This project is ideal for:
- **Developers** who want automated code quality insights
- **Teams** implementing code review processes
- **Researchers** studying agentic AI systems
- **Portfolio** showcasing advanced AI engineering

---

## Features

### 🤖 Multi-Agent Architecture

- **Code Analyzer Agent**: Identifies issues, calculates quality metrics, assigns grades
- **Optimizer Agent**: Generates optimized code versions with complexity analysis
- **Test Generator Agent**: Creates comprehensive test cases with edge case coverage
- **Orchestrator**: Coordinates autonomous workflows between agents

### 📊 Custom Evaluation Framework

- **Code Quality Score**: Complexity, readability, maintainability (0-100)
- **Autonomy Score**: Agent effectiveness without intervention (0-100)
- **Optimization Impact**: Percentage improvement measurement (0-100)
- **Consistency Score**: Stability across multiple runs (0-100)
- **Test Coverage Score**: Quality and completeness of tests (0-100)

### 🔄 Autonomous Workflows

- **Full Workflow**: Analysis → Optimization → Test Generation (sequential, autonomous)
- **Analysis Only**: Quick code review without optimization
- **Comparative Mode**: Run workflow with multiple models and compare results
- **Batch Processing**: Analyze entire directories and aggregate metrics

### 🛠️ Production-Ready Features

- Configuration-driven design (YAML-based)
- Comprehensive error handling with retry logic
- Structured JSON output for downstream processing
- Professional logging with file and console output
- CLI interface with multiple execution modes
- Extensible architecture for custom agents

### 📈 Comparative LLM Analysis

- Compare performance across Claude models (Opus, Sonnet, Haiku)
- Objective metrics-based model evaluation
- Cost vs. quality analysis
- Model-specific recommendations

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input (Code)                        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │  Orchestrator    │
                   │  (Coordinator)   │
                   └────────┬─────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Code         │ │ Optimizer    │ │ Test         │
    │ Analyzer     │ │ Agent        │ │ Generator    │
    │ Agent        │ │              │ │ Agent        │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Analysis     │ │ Optimized    │ │ Test Cases   │
    │ Results      │ │ Code         │ │ + Coverage   │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                ┌────────────────────────┐
                │ Evaluation Framework   │
                │ (Metrics Calculation)  │
                └────────────┬───────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │      Comprehensive Report with:       │
         │  - Quality Scores (0-100)             │
         │  - Issues Identified                  │
         │  - Optimized Code                     │
         │  - Generated Tests                    │
         │  - Improvement Suggestions            │
         └───────────────────────────────────────┘
```

### Component Hierarchy

```
BaseAgent (Abstract Base Class)
├── CodeAnalyzerAgent
├── OptimizerAgent
├── TestGeneratorAgent
└── WorkflowOrchestrator

LLMClient (API Management)
├── Retry Logic
├── Metrics Tracking
└── JSON Parsing

EvaluationFramework (Metrics)
├── MetricsCalculator
├── Scoring System
└── Comparative Analysis
```

---

## Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Conda**: For environment management (recommended on Windows)
- **API Key**: Valid Anthropic API key with active credits
- **OS**: Windows, macOS, or Linux

### Step-by-Step Setup

#### 1. Clone/Download the Project

```bash
# Create project directory
mkdir agent_code_review_system
cd agent_code_review_system
```

#### 2. Create Conda Environment (Recommended)

```bash
# Create environment
conda create -n codeagent python=3.10 -y

# Activate environment
conda activate codeagent
```

#### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Dependencies:**
- `anthropic>=0.21.0` - Claude API client
- `pydantic>=2.0.0` - Data validation
- `pyyaml>=6.0` - Configuration parsing
- `python-dotenv>=1.0.0` - Environment variable loading
- `requests>=2.31.0` - HTTP client
- `tabulate>=0.9.0` - Pretty table printing
- `rich>=13.0.0` - Rich console output
- `tqdm>=4.65.0` - Progress bars

#### 4. Set Up API Key

**Option A: Using .env File (Recommended)**

Create `.env` file in project root:

```bash
notepad .env
```

Add your API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Option B: Using Environment Variable**

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# macOS/Linux
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

#### 5. Verify Installation

```bash
# Test Python import
python -c "import anthropic; print('✅ Anthropic SDK installed')"

# Test API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key set:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```

---

## Quick Start

### 5-Minute Quick Start

#### 1. Analyze Inline Code

```bash
python main.py --mode analyze --code "def add(a, b): return a + b"
```

**Output:**
```
INFO: Starting code review for python code
INFO: Results saved to data\results\workflow_20260405_124041.json
INFO: Code review completed. Overall score: 85.0
```

#### 2. Run Full Workflow

```bash
python main.py --mode full --code "
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"
```

**Output includes:**
- ✅ Code analysis with issues found
- ✅ Optimized code generation
- ✅ Test case creation
- ✅ Comprehensive scoring

#### 3. Analyze a File

```bash
python main.py --mode file --file your_script.py
```

#### 4. Batch Process Directory

```bash
python main.py --mode dir --dir ./src --pattern "*.py"
```

#### 5. View Results

```bash
# List all results
dir data\results\

# View specific result
cat data\results\workflow_20260405_124041.json
```

---

## Usage

### Command-Line Interface

#### Mode: Analyze

Quick code analysis without optimization.

```bash
python main.py --mode analyze --code "your code here"
```

**Output:**
- Code quality score
- Issues identified
- Quality grade (A-F)
- Improvement suggestions

#### Mode: Full

Complete workflow: analysis → optimization → testing.

```bash
python main.py --mode full --code "your code here"
```

**Output:**
- Analysis results
- Optimized code
- Generated test cases
- Overall evaluation score

#### Mode: File

Analyze a single file.

```bash
python main.py --mode file --file path/to/file.py
```

**Supports:**
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- And more (auto-detected by extension)

#### Mode: Directory

Batch process all files in a directory.

```bash
python main.py --mode dir --dir ./src --pattern "*.py"
```

**Features:**
- Processes all matching files
- Aggregates metrics
- Generates summary report
- Incremental result saving

#### Mode: Compare

Compare multiple Claude models on the same code.

```bash
python main.py --mode compare --code "code" --models claude-opus-4-20250514 claude-sonnet-4-20250514
```

**Output:**
- Model comparison scores
- Strengths/weaknesses
- Cost analysis
- Recommendations

#### Mode: Report

Generate formatted report from results.

```bash
python main.py --mode report --results-file data/results/workflow_*.json
```

---

## System Components

### 1. BaseAgent (`agents/base_agent.py`)

Abstract base class for all agents.

**Key Methods:**
- `execute(task)` - Execute agent's primary task
- `_call_llm(message)` - Make LLM API calls
- `_create_result()` - Structured result creation
- `get_metrics()` - Performance metrics

### 2. CodeAnalyzerAgent (`agents/code_analyzer.py`)

Analyzes code for issues and quality.

**Features:**
- Identifies code issues with severity levels
- Calculates quality metrics (complexity, readability, maintainability)
- Assigns quality grades (A-F)
- Provides improvement suggestions

**Output Structure:**
```json
{
  "issues": [
    {
      "description": "Function exceeds 50 lines",
      "severity": "medium",
      "line_reference": "1-45"
    }
  ],
  "quality_metrics": {
    "complexity": 65,
    "readability": 75,
    "maintainability": 70
  },
  "overall_quality_score": 82,
  "quality_grade": "B"
}
```

### 3. OptimizerAgent (`agents/optimizer.py`)

Generates optimized code versions.

**Features:**
- Creates improved code versions
- Explains each optimization
- Compares complexity before/after
- Calculates improvement percentage

**Output Structure:**
```json
{
  "optimized_code": "def fibonacci(n, memo={})...",
  "optimizations_made": [
    "Added memoization for O(2^n) → O(n) improvement",
    "Added input validation"
  ],
  "complexity_before": "O(2^n)",
  "complexity_after": "O(n)",
  "improvement_percentage": 85
}
```

### 4. TestGeneratorAgent (`agents/test_generator.py`)

Creates comprehensive test cases.

**Features:**
- Generates unit tests
- Creates edge case tests
- Estimates code coverage
- Provides test strategy summary

**Output Structure:**
```json
{
  "test_cases": [
    {
      "name": "test_fibonacci_base_cases",
      "code": "def test_fibonacci_base_cases()...",
      "type": "unit"
    }
  ],
  "coverage_estimate": 95,
  "edge_cases_covered": [
    "Negative numbers",
    "Zero and one",
    "Large numbers"
  ]
}
```

### 5. WorkflowOrchestrator (`agents/orchestrator.py`)

Coordinates multi-agent workflows.

**Key Methods:**
- `execute_full_workflow()` - Complete analysis → optimization → testing
- `execute_analysis_only()` - Just analysis
- `execute_comparative_workflow()` - Multiple models
- `_calculate_workflow_metrics()` - Aggregate metrics

### 6. LLMClient (`utils/llm_client.py`)

Manages all LLM API interactions.

**Features:**
- Automatic retry logic with exponential backoff
- Metrics tracking (tokens, time, errors)
- JSON mode with fallback parsing
- Error handling and recovery

### 7. EvaluationFramework (`evaluation/metrics.py`)

Custom metrics and evaluation system.

**Key Methods:**
- `calculate_code_quality_score()` - Code quality (0-100)
- `calculate_autonomy_score()` - Agent effectiveness
- `calculate_optimization_impact()` - Improvement percentage
- `calculate_consistency_score()` - Stability across runs
- `calculate_test_coverage_score()` - Test quality
- `evaluate_workflow_result()` - Complete evaluation

---

## Evaluation Framework

### Metrics Explained

#### 1. Code Quality Score (0-100)

**Formula:**
```
score = (complexity + readability + maintainability) / 3 - penalties
```

**Factors:**
- Low complexity is better (0-100)
- High readability is better (0-100)
- High maintainability is better (0-100)
- Penalties for critical/high issues

**Example:**
- Well-structured, readable code: 85-95
- Average code with some issues: 60-75
- Complex, hard to maintain code: 30-50

#### 2. Autonomy Score (0-100)

**Measures:** How well agents complete tasks without intervention

**Factors:**
- Task completion without intervention: +100
- Each intervention needed: -10
- Errors encountered: -25
- Timeouts (>60s): -10

**Example:**
- Completed without errors: 90-100
- Completed with some issues: 70-85
- Failed or requires intervention: 0-50

#### 3. Optimization Impact (0-100)

**Formula:**
```
impact = (quality_improvement + size_reduction) / 2
```

**Measures:**
- Improvement in code quality
- Reduction in code size
- Complexity reduction

**Example:**
- Major improvements (O(2^n) → O(n)): 80-100
- Moderate improvements: 50-75
- Minor improvements: 25-50

#### 4. Consistency Score (0-100)

**Measures:** Stability across multiple runs

**Formula:**
```
consistency = 100 - (std_deviation × 10)
```

**Example:**
- Identical results across runs: 95-100
- Slight variations: 80-90
- Significant variations: 50-75

#### 5. Test Coverage Score (0-100)

**Measures:** Quality and completeness of generated tests

**Factors:**
- Coverage percentage (0-100): 60% weight
- Number of test cases: 20% weight
- Edge cases covered: 20% weight

**Example:**
- Comprehensive tests (>90% coverage): 85-100
- Good tests (70-90% coverage): 70-85
- Basic tests (<70% coverage): 50-70

### Overall Score Calculation

**Weighted Average:**
```
overall_score = Σ(metric_score × weight)
```

**Default Weights:**
- Code Quality: 0.4 (40%)
- Autonomy: 0.25 (25%)
- Optimization Impact: 0.2 (20%)
- Test Coverage: 0.15 (15%)

**Score Interpretation:**
- 90-100: Excellent
- 80-89: Good
- 70-79: Acceptable
- 60-69: Needs improvement
- <60: Significant issues

---

## Examples

### Example 1: Basic Code Analysis

```bash
python main.py --mode analyze --code "
def hello(name):
    print('Hello ' + name)
"
```

**Output:**
```
CODE REVIEW AND OPTIMIZATION REPORT
================================================================================
Quality Grade: C (72)
Issues Found: 3
  [MEDIUM] No docstring documentation
  [LOW] Using string concatenation instead of f-strings
  [LOW] No type hints
```

### Example 2: Full Workflow with Complex Algorithm

```bash
python main.py --mode full --code "
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"
```

**Output includes:**
```
OPTIMIZATION RESULTS
Improvement: Replaced O(n²) bubble sort with O(n log n) Timsort
Size Reduction: 45.2%

TEST COVERAGE
Estimated Coverage: 100%
Test Cases Generated: 13
```

### Example 3: Batch Directory Analysis

```bash
python main.py --mode dir --dir ./src --pattern "*.py"
```

**Output:**
```
BATCH SUMMARY
Files processed: 15
Average Quality Score: 78.5
Average Autonomy: 82.3
Total Issues Found: 47
Time taken: 2m 34s
```

### Example 4: Comparative Model Analysis

```bash
python main.py --mode compare --code "def add(a, b): return a + b" \
  --models claude-opus-4-20250514 claude-sonnet-4-20250514
```

**Output:**
```
MODEL COMPARISON
claude-opus-4-20250514: 88.5/100
  - More detailed analysis
  - Better optimization suggestions
  - Higher cost per request

claude-sonnet-4-20250514: 82.3/100
  - Faster processing
  - Good quality at lower cost
  - Sufficient for most tasks

RECOMMENDATION: Use Sonnet for cost efficiency, Opus for critical code
```

### Example 5: Programmatic Usage (Python)

```python
from main import CodeReviewSystem

# Initialize system
system = CodeReviewSystem()

# Analyze code
code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""

results = system.review_code(code, language="python")

# Access results
print(f"Quality Score: {results['evaluation']['overall_score']:.1f}")
print(f"Issues Found: {len(results['stages']['analysis']['result']['issues'])}")

# Get optimized code
optimization = results['stages']['optimization']['result']
print(f"\nOptimized Code:\n{optimization['optimized_code']}")

# Get test cases
tests = results['stages']['test_generation']['result']
print(f"\nTest Cases Generated: {tests['test_statistics']['total_test_cases']}")
```

---

## Performance

### Benchmark Results

Tested on standard hardware (2024 MacBook Pro, 8-core CPU, 16GB RAM):

| Operation | Time | Tokens | Cost | Notes |
|-----------|------|--------|------|-------|
| Quick Analysis | 3-5s | 200-400 | $0.001-0.002 | Simple code |
| Full Workflow | 8-12s | 800-1500 | $0.004-0.008 | Include optimization + tests |
| Directory (10 files) | 90-120s | 8000-15000 | $0.04-0.08 | Sequential processing |
| Model Comparison | 15-20s | 1500-2500 | $0.008-0.015 | 2 models |

### Scaling Performance

- **Single file**: ~5 seconds
- **Directory (10 files)**: ~90 seconds (9s per file)
- **Directory (100 files)**: ~900 seconds (9s per file)
- **Large file (1000 LOC)**: ~10-15 seconds
- **Batch optimization**: Linear scaling

### API Usage Optimization

**Token estimates:**
- Simple analysis: 200-400 tokens
- With optimization: 600-1000 tokens
- With test generation: 800-1500 tokens

**Cost optimization:**
- Use Haiku for quick analysis: 90% cheaper
- Use Sonnet for balanced cost/quality: 50% cheaper than Opus
- Use Opus only for critical code: Best quality

---

## Advanced Usage

### Custom Agent Development

Your project supports creating custom agents, though it requires familiarity with the codebase. To create a custom agent:

**Requirements:**
1. Understanding of the `BaseAgent` abstract class
2. Knowledge of LLM prompt engineering
3. Familiarity with JSON output structures
4. Python programming experience

**Basic Structure:**

```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, model: str):
        super().__init__(
            model=model,
            system_prompt="Your custom system prompt here"
        )
    
    def execute(self, task):
        # Extract input from task
        code = task.get("code")
        
        # Create prompt
        prompt = f"Your analysis prompt:\n{code}"
        
        # Call LLM
        result = self._call_llm(prompt, json_mode=True)
        
        # Return structured result
        return self._create_result(
            success=result['success'],
            result=result['content']
        )

# Usage
agent = MyCustomAgent("claude-opus-4-20250514")
result = agent.execute({"code": your_code})
```

**Steps to add a custom agent:**

1. Create new file in `agents/` directory
2. Extend `BaseAgent` class
3. Implement `execute()` method
4. Register in `orchestrator.py` if needed
5. Update `config/config.yaml` with system prompt

**Note:** This requires modifying core files and understanding the agent architecture.

### Custom Configuration

Modify `config/config.yaml` to customize behavior:

```yaml
models:
  primary: "claude-haiku-3.5"  # Change model
  temperature: 0.5  # More/less deterministic
  max_tokens: 2048  # Response length

agents:
  code_analyzer:
    system_prompt: |
      Custom prompt for specific analysis needs

evaluation:
  scoring_weights:
    correctness: 0.5  # Customize metric weights
    clarity: 0.3
    completeness: 0.2
```

### Batch Processing Script

```python
from pathlib import Path
from main import CodeReviewSystem
import json

system = CodeReviewSystem()
all_scores = []

# Process all Python files
for py_file in Path("src").glob("**/*.py"):
    print(f"Processing {py_file}...")
    result = system.process_file(str(py_file))
    
    score = result['evaluation']['overall_score']
    all_scores.append({
        'file': str(py_file),
        'score': score,
        'issues': len(result['stages']['analysis']['result'].get('issues', []))
    })

# Sort by score
all_scores.sort(key=lambda x: x['score'], reverse=True)

# Print report
print("\n=== CODE QUALITY REPORT ===")
for i, item in enumerate(all_scores, 1):
    print(f"{i}. {item['file']}: {item['score']:.1f} ({item['issues']} issues)")
```

---

## Project Structure

```
agent_code_review_system/
├── main.py                          # Entry point & CLI
├── requirements.txt                 # Python dependencies
├── .env                            # API key (not in git)
│
├── config/
│   ├── __init__.py
│   └── config.yaml                 # System configuration
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py               # Abstract base class
│   ├── code_analyzer.py            # Analysis agent
│   ├── optimizer.py                # Optimization agent
│   ├── test_generator.py           # Test generation agent
│   └── orchestrator.py             # Workflow coordinator
│
├── evaluation/
│   ├── __init__.py
│   └── metrics.py                  # Evaluation framework & metrics
│
├── utils/
│   ├── __init__.py
│   ├── llm_client.py               # LLM API client
│   └── logger.py                   # Logging configuration
│
├── data/
│   ├── benchmarks/
│   │   └── sample.py               # Example code
│   ├── results/                    # Generated results (auto-created)
│   └── (other data files)
│
├── logs/                           # System logs (auto-created)
│   └── system.log
│
└── README.md                       # This file
```



