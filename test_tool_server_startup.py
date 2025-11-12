#!/usr/bin/env python3
"""
Test script to verify tool_server.py starts correctly with command-line arguments.
"""
import subprocess
import sys
import time
import requests
import os


def test_server_startup():
    """Test that tool_server starts and responds to health checks"""
    print("Testing tool_server startup with arguments...")
    print(f"{'='*60}")
    
    # Set environment variable for sandbox mode
    env = os.environ.copy()
    env['STRIX_SANDBOX_MODE'] = 'true'
    
    # Start the server
    port = 9999
    token = "test-token-12345"
    
    print(f"Starting tool_server on port {port}...")
    process = subprocess.Popen(
        [
            sys.executable,
            '-m', 'strix.runtime.tool_server',
            '--token', token,
            '--host', '127.0.0.1',
            '--port', str(port)
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Check if process is still running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print(f"❌ Server exited prematurely!")
        print(f"Exit code: {process.returncode}")
        print(f"STDOUT: {stdout.decode()}")
        print(f"STDERR: {stderr.decode()}")
        return False
    
    print(f"✅ Server started (PID: {process.pid})")
    
    # Test health endpoint
    try:
        print("\nTesting /health endpoint...")
        response = requests.get(f'http://127.0.0.1:{port}/health', timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful!")
            print(f"   Response: {data}")
            
            # Verify expected fields
            assert data.get('status') == 'healthy', "Status should be 'healthy'"
            assert data.get('sandbox_mode') == 'True', "Sandbox mode should be True"
            assert data.get('active_agents') == 0, "Should have 0 active agents initially"
            print(f"✅ All health check fields correct")
            success = True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            success = False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to server: {e}")
        success = False
    except AssertionError as e:
        print(f"❌ Health check validation failed: {e}")
        success = False
    finally:
        # Stop the server
        print(f"\nStopping server (PID: {process.pid})...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print(f"✅ Server stopped cleanly")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"⚠️  Server had to be killed")
    
    print(f"{'='*60}\n")
    return success


def test_missing_sandbox_mode():
    """Test that server fails gracefully without STRIX_SANDBOX_MODE"""
    print("Testing tool_server without STRIX_SANDBOX_MODE (should fail)...")
    print(f"{'='*60}")
    
    # Explicitly unset the environment variable
    env = os.environ.copy()
    env.pop('STRIX_SANDBOX_MODE', None)
    
    process = subprocess.Popen(
        [
            sys.executable,
            '-m', 'strix.runtime.tool_server',
            '--token', 'test-token',
            '--host', '127.0.0.1',
            '--port', '9998'
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for it to exit
    try:
        stdout, stderr = process.communicate(timeout=3)
        exit_code = process.returncode
        
        stderr_text = stderr.decode()
        
        if exit_code != 0 and 'sandbox mode' in stderr_text.lower():
            print(f"✅ Server correctly rejected startup without STRIX_SANDBOX_MODE")
            print(f"   Exit code: {exit_code}")
            return True
        else:
            print(f"❌ Unexpected behavior:")
            print(f"   Exit code: {exit_code}")
            print(f"   STDERR: {stderr_text}")
            return False
            
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"❌ Server didn't exit as expected")
        return False
    finally:
        print(f"{'='*60}\n")


def main():
    print(f"\n{'#'*60}")
    print(f"# Tool Server Startup Test")
    print(f"{'#'*60}\n")
    
    # Test 1: Normal startup with sandbox mode
    test1_passed = test_server_startup()
    
    # Test 2: Startup without sandbox mode (should fail)
    test2_passed = test_missing_sandbox_mode()
    
    # Summary
    print(f"{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Server Startup (with sandbox mode): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Server Rejection (without sandbox): {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"{'='*60}\n")
    
    if test1_passed and test2_passed:
        print("🎉 All startup tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
