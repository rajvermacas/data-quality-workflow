#!/usr/bin/env python3
"""
Test script for Data Quality Alert to GitLab Issue n8n workflow
Sends sample webhook payloads to test the workflow functionality
"""

import json
import requests
import time
import argparse
from typing import Dict, Any, List


def load_test_data(file_path: str = "test_data/sample_webhook_payloads.json") -> List[Dict[str, Any]]:
    """Load test data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Test data file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in test data file: {file_path}")
        return []


def send_webhook_request(webhook_url: str, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    """Send a webhook request and return the response details"""
    try:
        print(f"📤 Sending request to: {webhook_url}")
        print(f"📝 Payload: {json.dumps(payload, indent=2)}")
        
        start_time = time.time()
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        end_time = time.time()
        
        return {
            "success": True,
            "status_code": response.status_code,
            "response_time": round(end_time - start_time, 2),
            "response_text": response.text,
            "headers": dict(response.headers)
        }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout",
            "response_time": timeout
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Connection error - check webhook URL",
            "response_time": 0
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request error: {str(e)}",
            "response_time": 0
        }


def print_test_result(test_case: Dict[str, Any], result: Dict[str, Any]) -> None:
    """Print formatted test result"""
    print(f"\n{'='*60}")
    print(f"🧪 Test Case: {test_case['test_case']}")
    print(f"📋 Description: {test_case['description']}")
    print(f"⏱️  Response Time: {result['response_time']}s")
    
    if result['success']:
        if result['status_code'] == 200:
            print(f"✅ SUCCESS - Status Code: {result['status_code']}")
        else:
            print(f"⚠️  WARNING - Status Code: {result['status_code']}")
        
        if result['response_text']:
            print(f"📤 Response: {result['response_text'][:200]}...")
    else:
        print(f"❌ FAILED - {result['error']}")
    
    print(f"{'='*60}")


def run_single_test(webhook_url: str, test_case: Dict[str, Any], delay: int = 0) -> bool:
    """Run a single test case"""
    if delay > 0:
        print(f"⏳ Waiting {delay} seconds before next test...")
        time.sleep(delay)
    
    result = send_webhook_request(webhook_url, test_case['payload'])
    print_test_result(test_case, result)
    
    return result['success'] and result.get('status_code') == 200


def run_all_tests(webhook_url: str, test_data: List[Dict[str, Any]], delay: int = 5) -> None:
    """Run all test cases"""
    print(f"🚀 Starting webhook tests for: {webhook_url}")
    print(f"📊 Total test cases: {len(test_data)}")
    
    if delay > 0:
        print(f"⏳ Delay between tests: {delay} seconds")
    
    results = []
    
    for i, test_case in enumerate(test_data, 1):
        print(f"\n🔄 Running test {i}/{len(test_data)}")
        success = run_single_test(webhook_url, test_case, delay if i > 1 else 0)
        results.append(success)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")
    print(f"📈 Success Rate: {(sum(results) / len(results) * 100):.1f}%")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Test n8n webhook workflow")
    parser.add_argument("webhook_url", help="n8n webhook URL")
    parser.add_argument("--test-data", default="test_data/sample_webhook_payloads.json", 
                       help="Path to test data JSON file")
    parser.add_argument("--test-case", type=int, help="Run specific test case by index (1-based)")
    parser.add_argument("--delay", type=int, default=5, 
                       help="Delay between tests in seconds (default: 5)")
    parser.add_argument("--timeout", type=int, default=30, 
                       help="Request timeout in seconds (default: 30)")
    
    args = parser.parse_args()
    
    # Validate webhook URL
    if not args.webhook_url.startswith(('http://', 'https://')):
        print("❌ Invalid webhook URL. Must start with http:// or https://")
        return
    
    # Load test data
    test_data = load_test_data(args.test_data)
    if not test_data:
        return
    
    print(f"✅ Loaded {len(test_data)} test cases")
    
    # Run specific test case or all tests
    if args.test_case:
        if 1 <= args.test_case <= len(test_data):
            test_case = test_data[args.test_case - 1]
            print(f"🧪 Running single test case: {args.test_case}")
            run_single_test(args.webhook_url, test_case)
        else:
            print(f"❌ Invalid test case number. Must be between 1 and {len(test_data)}")
    else:
        run_all_tests(args.webhook_url, test_data, args.delay)


if __name__ == "__main__":
    main()