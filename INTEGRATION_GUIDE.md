# CodeGeeX2 + Page Agent Integration Guide

Complete documentation for integrating CodeGeeX2 code generation with Page Agent web automation.

## Table of Contents

1. [Architecture](#architecture)
2. [Integration Patterns](#integration-patterns)
3. [Implementation Guide](#implementation-guide)
4. [API Examples](#api-examples)
5. [Advanced Workflows](#advanced-workflows)
6. [Troubleshooting](#troubleshooting)

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│              Integration Layer                           │
│  (CodeGeeXPageAgentBridge + WorkflowBuilder)            │
└────────────────┬──────────────────────┬─────────────────┘
                 │                      │
        ┌────────▼────────┐    ┌────────▼────────┐
        │   CodeGeeX2     │    │   Page Agent    │
        │                 │    │                 │
        │ • Generate      │    │ • Execute       │
        │ • Tokenize      │    │ • Monitor       │
        │ • Optimize      │    │ • Handle DOM    │
        └────────┬────────┘    └────────┬────────┘
                 │                      │
        ┌────────▼────────────────────▼────────┐
        │     Execution Engines                │
        │                                      │
        │ • Local (Python)                     │
        │ • Browser (JavaScript)               │
        │ • File (Saved Code)                  │
        └──────────────────────────────────────┘
```

### Data Flow

```
User Request
    ↓
Request Validation
    ↓
Type Detection (generate|execute|combined)
    ↓
┌─ Generate ─────────────────────┐
│ • Format prompt with lang tag  │
│ • Call CodeGeeX2               │
│ • Return generated code        │
└────────────────────────────────┘
    ↓
┌─ Execute ──────────────────────┐
│ • Select target environment    │
│ • Deploy code                  │
│ • Capture results/errors       │
└────────────────────────────────┘
    ↓
Record in History
    ↓
Return Result
```

## Integration Patterns

### Pattern 1: Sequential Generate → Execute

**Use Case**: User asks for a task, get code, execute it automatically

```python
async def sequential_workflow():
    bridge = CodeGeeXPageAgentBridge(model, api_key)
    
    # Step 1: Generate
    request = {
        "type": "combined",
        "prompt": "Click login and enter credentials",
        "language": "javascript",
        "target": "browser"
    }
    
    result = await bridge.process_request(request)
    return result
```

**Flow**: User Input → CodeGeeX2 → Page Agent → Result

### Pattern 2: Parallel Processing

**Use Case**: Generate multiple code variants and execute best one

```python
async def parallel_variants():
    bridge = CodeGeeXPageAgentBridge(model, api_key)
    
    prompts = [
        "Fill form using CSS selectors",
        "Fill form using XPath",
        "Fill form using text matching"
    ]
    
    requests = [
        {"type": "generate", "prompt": p, "language": "javascript"}
        for p in prompts
    ]
    
    results = await bridge.batch_process(requests)
    
    # Execute best variant
    best_code = results[0]  # In real scenario, rank by confidence
    return await bridge.process_request({
        "type": "execute",
        "code": best_code,
        "target": "browser"
    })
```

### Pattern 3: Conditional Routing

**Use Case**: Decide execution target based on code complexity

```python
async def conditional_routing():
    bridge = CodeGeeXPageAgentBridge(model, api_key)
    
    request = {
        "type": "generate",
        "prompt": "Parse CSV and extract data",
        "language": "python"
    }
    
    code = await bridge._handle_generate(request)
    
    # Route based on complexity
    if len(code) < 500:
        target = "console"
    elif "document." in code:
        target = "browser"
    else:
        target = "file"
    
    return await bridge.process_request({
        "type": "execute",
        "code": code,
        "target": target
    })
```

### Pattern 4: Iterative Refinement

**Use Case**: Generate → Execute → Get feedback → Regenerate

```python
async def iterative_refinement():
    bridge = CodeGeeXPageAgentBridge(model, api_key)
    
    prompt = "Create a script to test API endpoints"
    max_iterations = 3
    
    for i in range(max_iterations):
        code = await bridge.process_request({
            "type": "generate",
            "prompt": prompt,
            "language": "javascript"
        })
        
        result = await bridge.process_request({
            "type": "execute",
            "code": code,
            "target": "browser"
        })
        
        if result.get("status") == "success":
            return result
        
        # Refine prompt based on error
        prompt += f"\nPrevious error: {result.get('error')}"
```

## Implementation Guide

### 1. Setup CodeGeeX2

```python
from transformers import AutoTokenizer, AutoModel

# Load model
tokenizer = AutoTokenizer.from_pretrained(
    "THUDM/codegeex2-6b",
    trust_remote_code=True
)

model = AutoModel.from_pretrained(
    "THUDM/codegeex2-6b",
    trust_remote_code=True,
    device='cuda'
)

model = model.eval()
```

### 2. Initialize Bridge

```python
from bridge import CodeGeeXPageAgentBridge

bridge = CodeGeeXPageAgentBridge(
    codegeex_model=model,
    page_agent_api_key="your_api_key"
)
```

### 3. Create Workflows

```python
from bridge import WorkflowBuilder

workflow = WorkflowBuilder(bridge)

workflow \
    .add_step("Navigate to form page") \
    .add_step("Fill username field") \
    .add_step("Fill password field") \
    .add_step("Click submit button") \
    .add_step("Wait for success message")

results = await workflow.execute()
```

### 4. Monitor Execution

```python
# Get history
history = bridge.get_execution_history()

for entry in history:
    print(f"Prompt: {entry['prompt']}")
    print(f"Language: {entry['language']}")
    print(f"Time: {entry['execution_time_seconds']}s")
    print(f"Status: {entry.get('result', {}).get('status')}")
    print()
```

## API Examples

### Example 1: Form Filling

```python
async def fill_form():
    request = {
        "type": "combined",
        "prompt": "Fill registration form: username=john, email=john@example.com, password=SecurePass123",
        "language": "javascript",
        "target": "browser"
    }
    
    result = await bridge.process_request(request)
    return result
```

**Generated Code** (approximate):
```javascript
// CodeGeeX2 generates something like:
document.querySelector('input[name="username"]').value = 'john';
document.querySelector('input[name="email"]').value = 'john@example.com';
document.querySelector('input[name="password"]').value = 'SecurePass123';
document.querySelector('button[type="submit"]').click();
```

### Example 2: Web Scraping

```python
async def scrape_data():
    request = {
        "type": "generate",
        "prompt": "Extract product name, price, and rating from each product card on page",
        "language": "javascript"
    }
    
    code = await bridge._handle_generate(request)
    
    # Execute and collect data
    result = await bridge.process_request({
        "type": "execute",
        "code": code,
        "target": "browser"
    })
    
    return result
```

### Example 3: Multi-step Workflow

```python
async def multi_step_flow():
    workflow = WorkflowBuilder(bridge)
    
    workflow \
        .add_step(
            "Search for 'Python tutorials' on Google",
            language="javascript"
        ) \
        .add_step(
            "Click on first search result",
            language="javascript"
        ) \
        .add_step(
            "Extract article title and publish date",
            language="javascript"
        ) \
        .add_step(
            "Scroll down to find comments section",
            language="javascript"
        )
    
    results = await workflow.execute()
    return results
```

## Advanced Workflows

### Workflow 1: Test Generation and Execution

```python
async def generate_and_test():
    # Generate API test
    test_code = await bridge.process_request({
        "type": "generate",
        "prompt": "Write JavaScript test for user login endpoint",
        "language": "javascript"
    })
    
    # Execute test
    test_result = await bridge.process_request({
        "type": "execute",
        "code": test_code,
        "target": "browser"
    })
    
    # Parse results
    if test_result.get("status") == "success":
        print("✅ All tests passed")
    else:
        print("❌ Tests failed")
    
    return test_result
```

### Workflow 2: Error Handling and Retry

```python
async def robust_execution():
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            result = await bridge.process_request({
                "type": "combined",
                "prompt": "Click logout button and wait for redirect",
                "language": "javascript"
            })
            
            if result.get("status") == "success":
                return result
            
        except Exception as e:
            retry_count += 1
            print(f"Attempt {retry_count} failed: {str(e)}")
            
            if retry_count < max_retries:
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
    
    raise Exception("Max retries exceeded")
```

### Workflow 3: Performance Monitoring

```python
async def monitored_workflow():
    start_time = time.time()
    
    result = await bridge.process_request({
        "type": "combined",
        "prompt": "Fill and submit form",
        "language": "javascript"
    })
    
    total_time = time.time() - start_time
    
    # Analyze performance
    history = bridge.get_execution_history(limit=1)
    entry = history[0]
    
    print(f"Generation time: {entry.get('generation_time', 0):.2f}s")
    print(f"Execution time: {entry.get('execution_time_seconds', 0):.2f}s")
    print(f"Total time: {total_time:.2f}s")
    
    return result
```

## Troubleshooting

### Issue: Out of Memory

**Symptom**: `RuntimeError: CUDA out of memory`

**Solution**:
```python
# Use quantization
model = AutoModel.from_pretrained(
    "THUDM/codegeex2-6b",
    trust_remote_code=True,
    device='cuda'
).half()  # Use FP16

# Or use INT4 quantization
# See CodeGeeX2 docs for full setup
```

### Issue: Page Agent Connection Failed

**Symptom**: `ConnectionError: Unable to connect to Page Agent`

**Solution**:
```python
# Verify API key
bridge = CodeGeeXPageAgentBridge(
    model,
    page_agent_api_key="YOUR_VALID_KEY"  # Check key is correct
)

# Check network connectivity
import requests
response = requests.get("https://dashscope.aliyuncs.com/compatible-mode/v1/models")
print(response.status_code)
```

### Issue: Generated Code Errors

**Symptom**: `JavaScript execution failed: Cannot read property of undefined`

**Solution**:
```python
# Add better error handling in generated code
request = {
    "type": "generate",
    "prompt": "Generate code with error handling. Try to find element, if not found log error",
    "language": "javascript"
}

code = await bridge._handle_generate(request)
```

---

For more info, see [bridge.py](../bridge.py) implementation.
