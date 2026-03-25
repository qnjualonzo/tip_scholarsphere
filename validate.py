#!/usr/bin/env python3
"""Validation script for backend and frontend"""

import sys
import os
import shutil
import subprocess

def validate_backend():
    """Validate backend Python syntax and imports"""
    print("=" * 60)
    print("BACKEND VALIDATION")
    print("=" * 60)

    backend_python = os.path.join("backend", "venv", "Scripts", "python.exe")
    python_cmd = backend_python if os.path.exists(backend_python) else sys.executable

    # Step 1: Python syntax check
    print("\n1. Python syntax/import check (compileall)...")
    try:
        result = subprocess.run(
            [python_cmd, "-m", "compileall", "backend/app"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✓ PASS: Python syntax check successful")
        else:
            print("✗ FAIL: Python syntax check failed")
            if result.stderr:
                print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
            return False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    
    # Step 2: Runtime import check
    print("\n2. Runtime import check (app.main)...")
    try:
        result = subprocess.run(
            [python_cmd, "-c", "import app.main; print('import ok')"],
            cwd="backend",
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            stderr_text = result.stderr.strip() if result.stderr else ""
            stdout_text = result.stdout.strip() if result.stdout else ""
            detail = stderr_text or stdout_text or "unknown import error"
            print(f"✗ FAIL: Import failed - {detail}")
            return False
        print("✓ PASS: Successfully imported app.main")
        return True
    except Exception as e:
        print(f"✗ FAIL: Import failed - {e}")
        return False

def validate_frontend():
    """Validate frontend with npm install and build"""
    print("\n" + "=" * 60)
    print("FRONTEND VALIDATION")
    print("=" * 60)
    
    npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm_cmd:
        print("✗ FAIL: npm is not available in PATH")
        return False

    # Step 1: npm install check
    print("\n3. Checking npm dependencies...")
    try:
        os.chdir("frontend")
        # Check if node_modules exists and is complete
        if not os.path.exists("node_modules"):
            print("   node_modules not found, running npm install...")
            result = subprocess.run(
                [npm_cmd, "install"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode != 0:
                print("✗ FAIL: npm install failed")
                if result.stderr:
                    print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
                os.chdir("..")
                return False
            print("✓ PASS: npm install completed")
        else:
            print("   node_modules exists, skipping install")
            print("✓ PASS: npm dependencies ready")
    except Exception as e:
        print(f"✗ FAIL: npm install error - {e}")
        os.chdir("..")
        return False
    
    # Step 2: npm build
    print("\n4. Running npm build...")
    try:
        result = subprocess.run(
            [npm_cmd, "run", "build"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("✓ PASS: npm build successful")
            os.chdir("..")
            return True
        else:
            print("✗ FAIL: npm build failed")
            if result.stderr:
                print("STDERR:", result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)
            os.chdir("..")
            return False
    except Exception as e:
        print(f"✗ FAIL: npm build error - {e}")
        os.chdir("..")
        return False

if __name__ == "__main__":
    os.chdir("f:\\Users\\me\\tip_scholarsphere")
    
    backend_ok = validate_backend()
    frontend_ok = validate_frontend()
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Backend:  {'✓ PASS' if backend_ok else '✗ FAIL'}")
    print(f"Frontend: {'✓ PASS' if frontend_ok else '✗ FAIL'}")
    print("=" * 60)
    
    sys.exit(0 if (backend_ok and frontend_ok) else 1)
