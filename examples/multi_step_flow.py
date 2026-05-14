"""
Example: Multi-Step Workflow with CodeGeeX2 + Page Agent

Demonstrates complex automation workflows combining multiple steps
with code generation and execution.
"""

import asyncio
import sys
sys.path.insert(0, '..')

from bridge import CodeGeeXPageAgentBridge, WorkflowBuilder


async def ecommerce_checkout_flow():
    """Complete e-commerce checkout workflow."""
    print("=" * 60)
    print("Example 1: E-Commerce Checkout Flow")
    print("=" * 60)
    
    bridge = CodeGeeXPageAgentBridge(model=None, page_agent_api_key="demo_key")
    
    workflow = WorkflowBuilder(bridge)
    
    # Build checkout workflow
    workflow \
        .add_step("Search for 'laptop' in search box", language="javascript") \
        .add_step("Click first product in results", language="javascript") \
        .add_step("Select 16GB RAM variant", language="javascript") \
        .add_step("Click 'Add to Cart' button", language="javascript") \
        .add_step("Click shopping cart icon", language="javascript") \
        .add_step("Update quantity to 2", language="javascript") \
        .add_step("Click 'Proceed to Checkout' button", language="javascript") \
        .add_step("Fill shipping address with provided data", language="javascript") \
        .add_step("Select 'Express Shipping' option", language="javascript") \
        .add_step("Enter payment details", language="javascript") \
        .add_step("Review order and click 'Place Order'", language="javascript") \
        .add_step("Extract order confirmation number", language="javascript")
    
    print("\n📋 Workflow: Complete Checkout Process")
    print(f"Total steps: {len(workflow.steps)}")
    
    for i, step in enumerate(workflow.steps, 1):
        print(f"  {i:2d}. {step['prompt']}")
    
    print("\n⏳ Executing checkout workflow...")
    results = await workflow.execute()
    
    print(f"\n✅ Checkout completed in {len(results)} steps")
    print("📊 Workflow Statistics:")
    print(f"  - Total steps: {len(results)}")
    print(f"  - Successful: {sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')}")
    
    return results


async def content_management_flow():
    """Content publishing workflow."""
    print("\n" + "=" * 60)
    print("Example 2: Content Publishing Workflow")
    print("=" * 60)
    
    bridge = CodeGeeXPageAgentBridge(model=None, page_agent_api_key="demo_key")
    
    content_data = {
        "title": "Getting Started with Python",
        "description": "A beginner's guide to Python programming",
        "tags": ["python", "programming", "tutorial"],
        "category": "Education"
    }
    
    workflow = WorkflowBuilder(bridge)
    
    # Build publishing workflow
    workflow \
        .add_step("Navigate to admin dashboard", language="javascript") \
        .add_step("Click 'Create New Post' button", language="javascript") \
        .add_step(f"Fill title field with '{content_data['title']}'", language="javascript") \
        .add_step(f"Fill description with '{content_data['description']}'", language="javascript") \
        .add_step(f"Select category '{content_data['category']}'", language="javascript") \
        .add_step(f"Add tags: {', '.join(content_data['tags'])}", language="javascript") \
        .add_step("Set featured image", language="javascript") \
        .add_step("Click 'Publish' button", language="javascript") \
        .add_step("Wait for confirmation message", language="javascript") \
        .add_step("Extract post URL from success message", language="javascript")
    
    print("\n📋 Workflow: Publishing New Content")
    print("Content:")
    for key, value in content_data.items():
        print(f"  - {key}: {value}")
    
    print(f"\nSteps: {len(workflow.steps)}")
    
    print("\n⏳ Executing publishing workflow...")
    results = await workflow.execute()
    
    print(f"\n✅ Content published successfully")
    print(f"  Total steps executed: {len(results)}")
    
    return results


async def data_migration_flow():
    """Data migration and transformation workflow."""
    print("\n" + "=" * 60)
    print("Example 3: Data Migration Workflow")
    print("=" * 60)
    
    bridge = CodeGeeXPageAgentBridge(model=None, page_agent_api_key="demo_key")
    
    workflow = WorkflowBuilder(bridge)
    
    # Build migration workflow
    workflow \
        .add_step("Connect to source database", language="javascript") \
        .add_step("Query all customer records", language="javascript") \
        .add_step("Transform data to new schema format", language="javascript") \
        .add_step("Validate transformed data integrity", language="javascript") \
        .add_step("Connect to destination database", language="javascript") \
        .add_step("Insert transformed data in batches", language="javascript") \
        .add_step("Generate migration report", language="javascript") \
        .add_step("Verify record counts match", language="javascript") \
        .add_step("Backup original data", language="javascript") \
        .add_step("Mark migration as complete", language="javascript")
    
    print("\n📋 Workflow: Data Migration Pipeline")
    print(f"Total steps: {len(workflow.steps)}\n")
    
    for i, step in enumerate(workflow.steps, 1):
        print(f"  {i:2d}. {step['prompt']}")
    
    print("\n⏳ Executing migration workflow...")
    results = await workflow.execute()
    
    print(f"\n✅ Data migration completed")
    print(f"  Processed {len(results)} workflow steps")
    
    return results


async def api_testing_flow():
    """API endpoint testing workflow."""
    print("\n" + "=" * 60)
    print("Example 4: API Testing Workflow")
    print("=" * 60)
    
    bridge = CodeGeeXPageAgentBridge(model=None, page_agent_api_key="demo_key")
    
    api_endpoints = [
        "/api/users",
        "/api/products",
        "/api/orders",
        "/api/auth/login",
        "/api/auth/logout"
    ]
    
    workflow = WorkflowBuilder(bridge)
    
    # Build API testing workflow
    for endpoint in api_endpoints:
        workflow.add_step(f"Test GET request to {endpoint}", language="javascript")
        workflow.add_step(f"Validate response status and schema for {endpoint}", language="javascript")
    
    workflow \
        .add_step("Generate test report", language="javascript") \
        .add_step("Upload report to dashboard", language="javascript")
    
    print("\n📋 Workflow: API Testing Pipeline")
    print(f"Endpoints to test: {len(api_endpoints)}")
    for endpoint in api_endpoints:
        print(f"  - {endpoint}")
    
    print(f"\nTotal test steps: {len(workflow.steps)}")
    
    print("\n⏳ Executing API testing workflow...")
    results = await workflow.execute()
    
    print(f"\n✅ API testing completed")
    print(f"  Executed {len(results)} test steps")
    
    return results


async def user_onboarding_flow():
    """User account setup and onboarding workflow."""
    print("\n" + "=" * 60)
    print("Example 5: User Onboarding Workflow")
    print("=" * 60)
    
    bridge = CodeGeeXPageAgentBridge(model=None, page_agent_api_key="demo_key")
    
    user_info = {
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe",
        "company": "Tech Startup",
        "industry": "Software Development"
    }
    
    workflow = WorkflowBuilder(bridge)
    
    # Build onboarding workflow
    workflow \
        .add_step("Navigate to sign up page", language="javascript") \
        .add_step(f"Fill email with {user_info['email']}", language="javascript") \
        .add_step(f"Fill password", language="javascript") \
        .add_step("Verify email address", language="javascript") \
        .add_step(f"Fill profile with {user_info['first_name']} {user_info['last_name']}", language="javascript") \
        .add_step(f"Select industry: {user_info['industry']}", language="javascript") \
        .add_step(f"Enter company: {user_info['company']}", language="javascript") \
        .add_step("Complete profile setup", language="javascript") \
        .add_step("Setup two-factor authentication", language="javascript") \
        .add_step("Take product tour", language="javascript") \
        .add_step("Accept terms and conditions", language="javascript") \
        .add_step("Complete onboarding", language="javascript")
    
    print("\n📋 Workflow: Complete User Onboarding")
    print("User Information:")
    for key, value in user_info.items():
        print(f"  - {key}: {value}")
    
    print(f"\nSteps: {len(workflow.steps)}")
    
    print("\n⏳ Executing onboarding workflow...")
    results = await workflow.execute()
    
    print(f"\n✅ User onboarding completed")
    print(f"  Completed {len(results)} onboarding steps")
    
    return results


async def error_recovery_flow():
    """Workflow with error handling and recovery."""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling & Recovery Workflow")
    print("=" * 60)
    
    bridge = CodeGeeXPageAgentBridge(model=None, page_agent_api_key="demo_key")
    
    workflow = WorkflowBuilder(bridge)
    
    # Build resilient workflow
    workflow \
        .add_step("Try to load page", language="javascript") \
        .add_step("If timeout, retry with exponential backoff", language="javascript") \
        .add_step("Validate page loaded correctly", language="javascript") \
        .add_step("If validation fails, clear cache and reload", language="javascript") \
        .add_step("Extract data with error boundaries", language="javascript") \
        .add_step("Log any errors encountered", language="javascript") \
        .add_step("Generate error report if needed", language="javascript") \
        .add_step("Determine if workflow should retry", language="javascript") \
        .add_step("If successful, continue to next stage", language="javascript")
    
    print("\n📋 Workflow: Resilient Error Handling Pipeline")
    print(f"Total steps: {len(workflow.steps)}")
    
    for i, step in enumerate(workflow.steps, 1):
        print(f"  {i}. {step['prompt']}")
    
    print("\n⏳ Executing error-resilient workflow...")
    results = await workflow.execute()
    
    print(f"\n✅ Workflow completed with error handling")
    print(f"  Executed {len(results)} steps with recovery")
    
    return results


async def main():
    """Run all workflow examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  CodeGeeX2 + Page Agent: Multi-Step Workflows         ║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        await ecommerce_checkout_flow()
        await content_management_flow()
        await data_migration_flow()
        await api_testing_flow()
        await user_onboarding_flow()
        await error_recovery_flow()
        
        print("\n" + "=" * 60)
        print("✨ All workflow examples completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
