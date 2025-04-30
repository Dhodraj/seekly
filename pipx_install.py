#!/usr/bin/env python3
"""
Seekly CLI Pipx Installer

A lightweight script that helps users install Seekly CLI using pipx,
which is the recommended approach for CLI tools on systems with externally
managed environments (like modern Debian/Ubuntu systems).

This script follows Seekly's core principles:
- No hardcoding: Works across different platforms and system configurations
- Generic approach: Handles different installation paths adaptively
- Adaptability: Gracefully handles various environments without assumptions
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(cmd, capture=True):
    """
    Execute a shell command with flexible output handling.
    
    Args:
        cmd: Command to run
        capture: Whether to capture output (vs display it directly)
        
    Returns:
        Tuple of (success, output) where success is a boolean
    """
    try:
        if capture:
            result = subprocess.run(
                cmd, 
                shell=True,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode == 0, result.stdout + result.stderr
        else:
            # Run without capturing output (direct to terminal)
            result = subprocess.run(cmd, shell=True, check=False)
            return result.returncode == 0, ""
    except Exception as e:
        return False, str(e)


def check_command_exists(cmd):
    """
    Check if a command exists in the system PATH using a cross-platform approach.
    
    Args:
        cmd: Command name to check
    
    Returns:
        Boolean indicating if command exists
    """
    # Different checks based on platform for adaptability
    if platform.system() == "Windows":
        test_cmd = f"where {cmd}"
    else:
        test_cmd = f"command -v {cmd}"
    
    success, _ = run_command(test_cmd)
    return success


def get_package_source():
    """
    Determine the best package source based on environment.
    
    Returns:
        String containing the pip-compatible package reference
    """
    # If we're running from the Seekly repository, use local path
    if os.path.exists("setup.py") and os.path.isdir("seekly"):
        return "."
    # Otherwise use GitHub source
    return "git+https://github.com/Dhodraj/seekly.git"


def install_pipx():
    """
    Install pipx using the most appropriate method for the environment.
    
    Returns:
        Boolean indicating success
    """
    # Try multiple strategies to install pipx, in order of preference
    print("Installing pipx...")
    
    # Strategy 1: Use pip with --user to avoid system conflicts
    success, output = run_command(f"{sys.executable} -m pip install --user pipx")
    if success:
        # Ensure pipx is in PATH (platform agnostic)
        run_command(f"{sys.executable} -m pipx ensurepath", capture=False)
        return True
        
    # Strategy 2: For Debian-based systems, try apt
    if os.path.exists("/etc/debian_version"):
        print("Trying to install pipx via apt...")
        success, output = run_command("sudo apt install -y pipx")
        if success:
            return True
    
    # Strategy 3: For macOS, try Homebrew
    if platform.system() == "Darwin" and check_command_exists("brew"):
        print("Trying to install pipx via Homebrew...")
        success, output = run_command("brew install pipx")
        if success:
            run_command("pipx ensurepath", capture=False)
            return True
    
    print(f"Failed to install pipx. Error details:\n{output}")
    return False


def install_seekly():
    """
    Main function to install Seekly via pipx.
    """
    # Header display
    print("=" * 60)
    print("Seekly CLI Installer")
    print("=" * 60)
    
    # Check if pipx is already installed
    has_pipx = check_command_exists("pipx")
    
    if not has_pipx:
        print("pipx not found. It's needed to install Seekly as a CLI tool.")
        install_ok = install_pipx()
        
        if not install_ok:
            print("\nCould not install pipx automatically.")
            print("Please install pipx manually and try again:")
            print("  • pip install --user pipx")
            print("  • python -m pipx ensurepath")
            return False
    
    # Now install Seekly using pipx
    package_source = get_package_source()
    print(f"\nInstalling Seekly from {package_source}...")
    
    # Execute installation with output shown directly to user
    cmd = f"pipx install {package_source} --force"
    success, output = run_command(cmd, capture=False)
    
    if success:
        print("\n✓ Seekly CLI installed successfully!")
        print("\nYou can now use Seekly with commands like:")
        print("  seekly search \"find function that validates email\"")
        print("  seekly info")
        print("  seekly --help")
        return True
    else:
        print("\n✗ Installation failed.")
        print("Try installing manually with:")
        print(f"  pipx install {package_source}")
        return False


if __name__ == "__main__":
    install_seekly()