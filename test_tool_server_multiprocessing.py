#!/usr/bin/env python3
"""
Test script to verify tool_server.py multiprocessing fix.
This simulates the worker process creation that was causing issues on Windows.
"""
import multiprocessing
import sys
import time


def worker_function(queue, worker_id):
    """Simulates agent_worker in tool_server.py"""
    try:
        # This import should NOT trigger argument parsing or RuntimeError
        from strix.runtime import tool_server
        
        queue.put({
            'worker_id': worker_id,
            'status': 'success',
            'message': f'Worker {worker_id}: tool_server imported successfully',
            'expected_token_is_none': tool_server.EXPECTED_TOKEN is None
        })
    except Exception as e:
        queue.put({
            'worker_id': worker_id,
            'status': 'error',
            'message': f'Worker {worker_id}: Failed - {str(e)}'
        })


def test_multiprocessing_spawn():
    """Test with spawn method (used on Windows)"""
    print("Testing multiprocessing with 'spawn' method (Windows behavior)...")
    
    # Force spawn method (Windows default)
    ctx = multiprocessing.get_context('spawn')
    
    queue = ctx.Queue()
    workers = []
    
    # Create multiple worker processes
    for i in range(3):
        p = ctx.Process(target=worker_function, args=(queue, i))
        p.start()
        workers.append(p)
    
    # Wait for all workers
    for p in workers:
        p.join(timeout=5)
        if p.is_alive():
            p.terminate()
            print(f"⚠️  Worker had to be terminated (timeout)")
    
    # Collect results
    results = []
    while not queue.empty():
        results.append(queue.get())
    
    # Display results
    print(f"\n{'='*60}")
    print(f"Results from {len(results)} workers:")
    print(f"{'='*60}")
    
    all_success = True
    for result in results:
        status_symbol = "✅" if result['status'] == 'success' else "❌"
        print(f"{status_symbol} {result['message']}")
        if result['status'] == 'success':
            print(f"   - EXPECTED_TOKEN is None: {result['expected_token_is_none']}")
        else:
            all_success = False
    
    print(f"{'='*60}\n")
    
    return all_success


def test_direct_import():
    """Test direct import"""
    print("Testing direct import of tool_server...")
    try:
        from strix.runtime import tool_server
        print(f"✅ Direct import successful")
        print(f"   - EXPECTED_TOKEN is None: {tool_server.EXPECTED_TOKEN is None}")
        print(f"   - SANDBOX_MODE: {tool_server.SANDBOX_MODE}")
        return True
    except Exception as e:
        print(f"❌ Direct import failed: {e}")
        return False


def main():
    print(f"\n{'#'*60}")
    print(f"# Tool Server Multiprocessing Fix Test")
    print(f"{'#'*60}\n")
    
    # Test 1: Direct import
    test1_passed = test_direct_import()
    print()
    
    # Test 2: Multiprocessing with spawn
    test2_passed = test_multiprocessing_spawn()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Direct Import: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Multiprocessing (spawn): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"{'='*60}\n")
    
    if test1_passed and test2_passed:
        print("🎉 All tests passed! The fix is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
