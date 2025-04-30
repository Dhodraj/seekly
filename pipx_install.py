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
import shutil


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


def update_user_path(bin_dir):
    """
    Update user's PATH to include pipx binaries directory.
    
    Args:
        bin_dir: Directory to add to PATH
        
    Returns:
        Boolean indicating success
    """
    # Different approaches based on platform
    if platform.system() == "Windows":
        # For Windows, use the registry or setx
        os.system(f'setx PATH "%PATH%;{bin_dir}"')
        os.environ["PATH"] += f";{bin_dir}"
        return True
    else:
        # For Unix-like systems, modify shell startup files
        # Detect which shell is being used
        shell = os.environ.get("SHELL", "")
        
        # Default to ~/.profile if shell can't be determined
        shell_rc_file = os.path.expanduser("~/.profile")
        
        # Determine appropriate shell config file
        if "bash" in shell:
            shell_rc_file = os.path.expanduser("~/.bashrc")
        elif "zsh" in shell:
            shell_rc_file = os.path.expanduser("~/.zshrc")
        elif "fish" in shell:
            shell_rc_file = os.path.expanduser("~/.config/fish/config.fish")
            
        # Skip if already in PATH
        if bin_dir in os.environ.get("PATH", ""):
            return True
            
        # Backup the rc file
        backup_file = f"{shell_rc_file}.seekly_bak"
        try:
            if os.path.exists(shell_rc_file) and not os.path.exists(backup_file):
                shutil.copy(shell_rc_file, backup_file)
        except Exception:
            pass
            
        # Check if bin_dir already in file to avoid duplicates
        try:
            if os.path.exists(shell_rc_file):
                with open(shell_rc_file, 'r') as f:
                    content = f.read()
                    if bin_dir in content:
                        return True
        except Exception:
            pass
        
        # Append to shell config
        try:
            with open(shell_rc_file, 'a+') as f:
                if "fish" in shell:
                    f.write(f"\n# Added by Seekly installer\nset -x PATH {bin_dir} $PATH\n")
                else:
                    f.write(f"\n# Added by Seekly installer\nexport PATH=\"{bin_dir}:$PATH\"\n")
            return True
        except Exception as e:
            print(f"Error updating shell config: {str(e)}")
            return False


def get_pipx_bin_dir():
    """
    Get the directory where pipx installs binaries.
    
    Returns:
        Path to the pipx bin directory
    """
    # Try to get it from pipx
    success, output = run_command("pipx environment --value PIPX_BIN_DIR")
    if success and output.strip():
        return output.strip()
        
    # Default locations by OS
    if platform.system() == "Windows":
        return os.path.expanduser("~\\.local\\bin")
    else:
        return os.path.expanduser("~/.local/bin")


def ensure_seekly_runnable():
    """
    Ensure the seekly command can be run by updating PATH if needed.
    
    Returns:
        Tuple of (success, bin_path)
    """
    # First check if seekly is already runnable
    if check_command_exists("seekly"):
        return True, ""
        
    # If not, determine the pipx bin directory
    bin_dir = get_pipx_bin_dir()
    
    # Verify seekly exists in this directory
    seekly_path = os.path.join(bin_dir, "seekly")
    if platform.system() == "Windows":
        seekly_path += ".exe"
        
    if not os.path.exists(seekly_path):
        seekly_path = ""
        # Try to find seekly in common locations
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            test_path = os.path.join(path_dir, "seekly")
            if platform.system() == "Windows":
                test_path += ".exe"
            if os.path.exists(test_path):
                seekly_path = test_path
                bin_dir = path_dir
                break
                
    if not seekly_path:
        return False, bin_dir
        
    # Update PATH if needed and return the bin directory
    updated = update_user_path(bin_dir)
    return updated, bin_dir


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
        
        # Make sure seekly is runnable in the current shell
        path_updated, bin_dir = ensure_seekly_runnable()
        
        if path_updated:
            print("\n✓ Seekly command is now available!")
            print("\nYou can start using Seekly immediately with commands like:")
            
            # For Windows, suggest reopening terminal
            if platform.system() == "Windows":
                print("\nNOTE: You may need to open a new terminal window first.")
            # For Unix-like systems, suggest sourcing the shell config
            else:
                shell = os.environ.get("SHELL", "")
                if "bash" in shell:
                    print("\nTo use Seekly in this terminal session, run:")
                    print("  source ~/.bashrc")
                elif "zsh" in shell:
                    print("\nTo use Seekly in this terminal session, run:")
                    print("  source ~/.zshrc")
                elif "fish" in shell:
                    print("\nTo use Seekly in this terminal session, run:")
                    print("  source ~/.config/fish/config.fish")
                else:
                    print("\nTo use Seekly in this terminal session, run:")
                    print("  source ~/.profile")
            
            print("\nThen you can use commands like:")
            print("  seekly search \"find function that validates email\"")
            print("  seekly info")
            print("  seekly --help")
        else:
            print(f"\nNOTE: Seekly was installed successfully, but you may need to add")
            print(f"      {bin_dir} to your PATH to use it.")
            print("\nUntil then, you can use Seekly with:")
            seekly_path = os.path.join(bin_dir, "seekly")
            print(f"  {seekly_path} search \"your query here\"")
            
        return True
    else:
        print("\n✗ Installation failed.")
        print("Try installing manually with:")
        print(f"  pipx install {package_source}")
        return False


if __name__ == "__main__":
    install_seekly()