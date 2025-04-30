#!/usr/bin/env python3
"""
Seekly Installation Helper

This script helps users install Seekly in various Python environments by:
1. Detecting the current environment type
2. Recommending the most appropriate installation method
3. Guiding users through the installation process
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def check_environment():
    """Detect the type of Python environment the user is running in."""
    env_info = {
        "is_venv": sys.prefix != sys.base_prefix,
        "is_linux": platform.system() == "Linux",
        "is_windows": platform.system() == "Windows",
        "is_macos": platform.system() == "Darwin",
        "pip_path": shutil.which("pip"),
        "pipx_path": shutil.which("pipx"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "can_write_to_site_packages": os.access(next(iter(sys.path), "."), os.W_OK),
    }
    
    # Check for Debian/Ubuntu specific environment
    if env_info["is_linux"]:
        env_info["is_debian_based"] = os.path.exists("/etc/debian_version")
        # Check for externally managed environment marker
        env_info["is_externally_managed"] = os.path.exists(
            os.path.join(sys.prefix, "share/python/debian_info.json")
        ) or os.path.exists(
            os.path.join(sys.prefix, "lib/python{}.{}/EXTERNALLY-MANAGED".format(
                sys.version_info.major, sys.version_info.minor
            ))
        )
    else:
        env_info["is_debian_based"] = False
        env_info["is_externally_managed"] = False
    
    return env_info


def run_command(cmd, check=False):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=check,
            text=True,
            capture_output=True
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "code": result.returncode
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "code": 1
        }


def create_venv(venv_path="seekly-env"):
    """Create a virtual environment at the specified path."""
    print(f"Creating virtual environment at {venv_path}...")
    cmd = f"{sys.executable} -m venv {venv_path}"
    result = run_command(cmd)
    
    if not result["success"]:
        print(f"Error creating virtual environment: {result['error']}")
        return False
    
    # Get activation command based on platform
    if platform.system() == "Windows":
        activate_cmd = f"{venv_path}\\Scripts\\activate"
        python_path = f"{venv_path}\\Scripts\\python"
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
        python_path = f"{venv_path}/bin/python"
    
    print("\nVirtual environment created successfully!")
    print(f"\nTo activate and use, run:\n{activate_cmd}")
    print(f"\nThen install Seekly with:\n{python_path} -m pip install seekly")
    
    return True


def setup_pipx():
    """Check for or install pipx."""
    if shutil.which("pipx"):
        print("pipx is already installed.")
        return True
    
    print("Installing pipx...")
    result = run_command(f"{sys.executable} -m pip install --user pipx")
    
    if not result["success"]:
        print(f"Error installing pipx: {result['error']}")
        return False
    
    # Ensure pipx is in PATH
    run_command("pipx ensurepath")
    
    print("\npipx installed successfully!")
    print("\nTo install Seekly with pipx, run:\npipx install seekly")
    
    return True


def main():
    """Main function to guide installation."""
    print("Seekly Installation Helper")
    print("-" * 50)
    print("Detecting your environment...")
    
    env = check_environment()
    
    print(f"\nEnvironment Details:")
    print(f"• Python Version: {env['python_version']}")
    print(f"• Operating System: {platform.system()}")
    print(f"• Virtual Environment: {'Yes' if env['is_venv'] else 'No'}")
    if env["is_linux"]:
        print(f"• Debian-based: {'Yes' if env['is_debian_based'] else 'No'}")
        print(f"• Externally Managed: {'Yes' if env['is_externally_managed'] else 'No'}")
    
    print("\nRecommended Installation Method:")
    
    # Determine the best installation method based on the environment
    if env["is_venv"]:
        print("You're already in a virtual environment. You can install directly with pip.")
        print("\nRun:\npip install seekly")
    elif env["is_externally_managed"]:
        print("Your Python environment is externally managed (PEP 668).")
        print("The best options are:")
        print("1. Use pipx (recommended)")
        print("2. Create a virtual environment")
        
        choice = input("\nSelect an option (1/2) or press Enter for pipx: ") or "1"
        
        if choice == "1":
            setup_pipx()
        else:
            create_venv()
    elif not env["can_write_to_site_packages"]:
        print("You don't have write permission to the Python site-packages directory.")
        print("The best options are:")
        print("1. Create a virtual environment (recommended)")
        print("2. Use pip with --user flag")
        
        choice = input("\nSelect an option (1/2) or press Enter for virtual environment: ") or "1"
        
        if choice == "1":
            create_venv()
        else:
            print("\nTo install for your user only, run:")
            print(f"{sys.executable} -m pip install --user seekly")
    else:
        print("You can install Seekly in multiple ways:")
        print("1. Create a virtual environment (recommended)")
        print("2. Install with pipx")
        print("3. Install directly with pip")
        
        choice = input("\nSelect an option (1/2/3) or press Enter for virtual environment: ") or "1"
        
        if choice == "1":
            create_venv()
        elif choice == "2":
            setup_pipx()
        else:
            print("\nTo install with pip, run:")
            print(f"{sys.executable} -m pip install seekly")
    
    print("\nFor more information, refer to the README.md or visit:")
    print("https://github.com/Dhodraj/seekly")


if __name__ == "__main__":
    main()