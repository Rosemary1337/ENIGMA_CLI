#!/usr/bin/env python3
"""
███████╗███╗   ██╗██╗ ██████╗ ███╗   ███╗ █████╗          ██████╗██╗     ██╗
██╔════╝████╗  ██║██║██╔════╝ ████╗ ████║██╔══██╗        ██╔════╝██║     ██║
█████╗  ██╔██╗ ██║██║██║  ███╗██╔████╔██║███████║        ██║     ██║     ██║
██╔══╝  ██║╚██╗██║██║██║   ██║██║╚██╔╝██║██╔══██║        ██║     ██║     ██║
███████╗██║ ╚████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║███████╗╚██████╗███████╗██║
╚══════╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("="*60)
    print("ENIGMA CLI Installation Script")
    print("Installing required dependencies for ENIGMA CLI")
    print("="*60)
    print()

def install_python_packages():
    """Install required Python packages"""
    print("[INSTALLING PYTHON PACKAGES]")
    
    # Required packages for ENIGMA CLI (without PyQt5)
    packages = [
        "openai",
        "psutil"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    
    print("\n✓ All Python packages installed successfully")
    return True

def detect_linux_distro():
    """Detect the Linux distribution"""
    try:
        # Try to read /etc/os-release to determine the distribution
        with open('/etc/os-release', 'r') as f:
            os_release = f.read().lower()
        
        if 'arch' in os_release or 'manjaro' in os_release or 'artix' in os_release:
            return 'arch'
        elif 'ubuntu' in os_release or 'debian' in os_release:
            return 'ubuntu'
        elif 'centos' in os_release or 'rhel' in os_release or 'fedora' in os_release:
            return 'redhat'
        else:
            # Default to checking for package managers if distribution not recognized
            for pkg_mgr in ['pacman', 'apt', 'yum', 'dnf']:
                try:
                    subprocess.check_output(['which', pkg_mgr])
                    if pkg_mgr == 'pacman':
                        return 'arch'
                    elif pkg_mgr == 'apt':
                        return 'ubuntu'
                    else:
                        return 'redhat'
                except subprocess.CalledProcessError:
                    continue
            return 'unknown'
    except FileNotFoundError:
        # Fallback method: check for package managers directly
        for pkg_mgr in ['pacman', 'apt', 'yum', 'dnf']:
            try:
                subprocess.check_output(['which', pkg_mgr])
                if pkg_mgr == 'pacman':
                    return 'arch'
                elif pkg_mgr == 'apt':
                    return 'ubuntu'
                else:
                    return 'redhat'
            except subprocess.CalledProcessError:
                continue
        return 'unknown'

def check_aur_tool(tool_name):
    """Check and install AUR tools using pacman or AUR helpers"""
    # Check if the tool is available in official repos first
    try:
        subprocess.check_output(['pacman', '-Si', tool_name], stderr=subprocess.STDOUT)
        # Tool is in official repos
        return f"sudo pacman -S {tool_name} --noconfirm"
    except subprocess.CalledProcessError:
        # Tool is not in official repos, check AUR
        # Try to find an AUR helper
        aur_helpers = ['paru', 'yay', 'pikaur', 'trizen', 'yaourt']
        aur_helper = None
        
        for helper in aur_helpers:
            try:
                subprocess.check_output(['which', helper])
                aur_helper = helper
                break
            except subprocess.CalledProcessError:
                continue
        
        if aur_helper:
            return f"{aur_helper} -S {tool_name} --noconfirm"
        else:
            print(f"Warning: {tool_name} is not in official repos and no AUR helper found.")
            print("You may need to install it manually or install an AUR helper like paru or yay.")
            return f"manual_install_{tool_name}"

def install_system_tools():
    """Install required system tools"""
    print("\n[INSTALLING SYSTEM TOOLS]")
    
    system = platform.system().lower()
    
    # Define tools to install based on the operating system
    if system == "linux":
        print("Detected Linux system")
        
        # Detect the specific Linux distribution
        distro = detect_linux_distro()
        print(f"Detected Linux distribution: {distro}")
        
        # Define tools based on the package manager
        if distro in ["arch", "manjaro", "artix"]:
            # Arch-based distributions
            base_tools = {
                "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                "assetfinder": "go install github.com/tomnomnom/assetfinder@latest",
                "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
                "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
                "okadminfinder": "git clone https://github.com/stefanoj3/okadminfinder.git /tmp/okadminfinder && cd /tmp/okadminfinder && go build -o /usr/local/bin/okadminfinder .",
                "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
                "nuclei": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                "subjack": "go install -v github.com/haccer/subjack@latest",
                "gau": "go install -v github.com/lc/gau/v2/cmd/gau@latest",
                "amass": "go install -v github.com/owasp-amass/amass/v4/commands/amass@latest",
                "whatweb": "check_aur_tool whatweb",
                "tree": "sudo pacman -S tree --noconfirm"
            }
            
            # Handle sslscan specifically for Arch
            sslscan_cmd = check_aur_tool("sslscan")
            base_tools["sslscan"] = sslscan_cmd
            
            # Handle whois for Arch
            whois_cmd = check_aur_tool("whois")
            base_tools["whois"] = whois_cmd
            
            tools = base_tools
        else:
            # Default to apt-based systems (Ubuntu, Debian, etc.)
            tools = {
                "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                "assetfinder": "go install github.com/tomnomnom/assetfinder@latest",
                "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
                "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
                "okadminfinder": "git clone https://github.com/stefanoj3/okadminfinder.git /tmp/okadminfinder && cd /tmp/okadminfinder && go build -o /usr/local/bin/okadminfinder .",
                "sslscan": "sudo apt-get install sslscan",
                "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
                "whois": "sudo apt-get install whois",
                "nuclei": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                "subjack": "go install -v github.com/haccer/subjack@latest",
                "gau": "go install -v github.com/lc/gau/v2/cmd/gau@latest",
                "amass": "go install -v github.com/owasp-amass/amass/v4/commands/amass@latest",
                "whatweb": "sudo apt-get install whatweb",
                "tree": "sudo apt-get install tree"
            }
    elif system == "darwin":  # macOS
        print("Detected macOS system")
        tools = {
            "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "assetfinder": "go install github.com/tomnomnom/assetfinder@latest",
            "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
            "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
            "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "whois": "brew install whois"
        }
    else:
        print(f"Unsupported system: {system}")
        print("Please install the required tools manually")
        return False
    
    print("\nInstalling security tools...")
    
    # Check if Go is installed
    try:
        subprocess.check_output(["go", "version"])
        go_available = True
        print("✓ Go is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Go is not installed. Please install Go first.")
        go_available = False
    
    # Install each tool
    successful_installs = []
    failed_installs = []
    
    for tool, install_cmd in tools.items():
        print(f"\nInstalling {tool}...")
        
        # Special handling for AUR tools
        if install_cmd.startswith("manual_install_"):
            print(f"⚠ Skipping {tool} - requires manual installation")
            print(f"   You can install {tool} manually using an AUR helper like 'paru -S {tool}' or 'yay -S {tool}'")
            failed_installs.append(tool)
            continue
        
        # For tools that require Go, check if Go is available
        if "go install" in install_cmd and not go_available:
            print(f"⚠ Skipping {tool} (requires Go)")
            failed_installs.append(tool)
            continue
            
        # For tools that require sudo, ask for confirmation
        if install_cmd.startswith("sudo"):
            response = input(f"Do you want to install {tool} with sudo? (y/N): ")
            if response.lower() != 'y':
                print(f"Skipping {tool}")
                failed_installs.append(tool)
                continue
        
        try:
            # Handle shell commands properly
            if " " in install_cmd and ("sudo" in install_cmd or "paru" in install_cmd or "yay" in install_cmd):
                subprocess.check_call(install_cmd, shell=True)
            else:
                subprocess.check_call(install_cmd.split(), shell=("sudo" in install_cmd or "paru" in install_cmd or "yay" in install_cmd))
            print(f"✓ {tool} installed successfully")
            successful_installs.append(tool)
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {tool}")
            failed_installs.append(tool)
    
    print(f"\n✓ Successfully installed: {', '.join(successful_installs)}")
    if failed_installs:
        print(f"✗ Failed to install: {', '.join(failed_installs)}")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n[CREATING DIRECTORIES]")
    
    dirs_to_create = [
        "output",
        "output/enumeration",
        "output/information", 
        "output/crawling",
        "output/pathfinder",
        "output/sslscan",
        "output/vulnerability",
        "output/takeover",
        "output/httpx",
        "output/gau",
        "output/amass",
        "output/technologies",
        "output/daily_hunt"
    ]
    
    for directory in dirs_to_create:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")
    
    print("\n✓ All required directories created")

def setup_api_key_file():
    """Create an empty API key file for AI functionality"""
    print("\n[SETTING UP API KEY FILE]")
    
    api_key_file = "openai_apikey.txt"
    if not os.path.exists(api_key_file):
        with open(api_key_file, 'w') as f:
            f.write("")
        print(f"✓ Created {api_key_file}")
        print("Tip: Add your OpenAI API key to this file to enable AI features")
    else:
        print(f"- {api_key_file} already exists")

def verify_installation():
    """Verify that tools are installed"""
    print("\n[VERIFYING INSTALLATION]")
    
    tools_to_check = [
        "whois",
        "subfinder",
        "assetfinder", 
        "katana",
        "waybackurls",
        "httpx",
        "nuclei",
        "subjack",
        "gau",
        "amass",
        "whatweb",
        "tree"
    ]
    
    available_tools = []
    missing_tools = []
    
    for tool in tools_to_check:
        try:
            subprocess.check_output(["which", tool])
            available_tools.append(tool)
        except subprocess.CalledProcessError:
            missing_tools.append(tool)
    
    if available_tools:
        print(f"✓ Available tools: {', '.join(available_tools)}")
    if missing_tools:
        print(f"⚠ Missing tools: {', '.join(missing_tools)}")
        print("These tools were not installed. You may need to install them manually.")
    
    # Check Python modules
    python_modules = ["openai", "psutil"]
    available_modules = []
    missing_modules = []
    
    for module in python_modules:
        try:
            __import__(module)
            available_modules.append(module)
        except ImportError:
            missing_modules.append(module)
    
    if available_modules:
        print(f"✓ Available Python modules: {', '.join(available_modules)}")
    if missing_modules:
        print(f"✗ Missing Python modules: {', '.join(missing_modules)}")
    
    return len(missing_modules) == 0

def main():
    print_header()
    
    print("This script will install all required dependencies for ENIGMA CLI.")
    print("ENIGMA CLI is a security reconnaissance tool without GUI dependencies.\n")
    
    response = input("Do you want to proceed with installation? (Y/n): ")
    if response.lower() == 'n':
        print("Installation cancelled.")
        return
    
    print("\nStarting installation...")
    
    # Install Python packages first
    python_success = install_python_packages()
    
    # Install system tools
    tools_success = install_system_tools()
    
    # Create necessary directories
    create_directories()
    
    # Setup API key file
    setup_api_key_file()
    
    # Verify installation
    verify_success = verify_installation()
    
    print("\n" + "="*60)
    print("INSTALLATION SUMMARY")
    print("="*60)
    
    if python_success:
        print("✓ Python packages installed successfully")
    else:
        print("✗ Python packages installation failed")
    
    if tools_success:
        print("✓ System tools installation completed (with possible skipped items)")
    else:
        print("✗ System tools installation failed")
    
    # Create a simple test command
    print("\nTo test ENIGMA CLI, run:")
    print("  python enigma_cli.py settings")
    
    print("\nFor AI functionality, set your OpenAI API key:")
    print("  Add your API key to openai_apikey.txt or use --api-key parameter")
    
    print("\n✓ Installation process completed!")

if __name__ == "__main__":
    main()
