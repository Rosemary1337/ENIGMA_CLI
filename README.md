# ENIGMA CLI

**A comprehensive security reconnaissance tool for bug bounty hunters**

ENIGMA CLI is a command-line version of the ENIGMA security framework, designed to streamline your bug bounty workflow with a collection of powerful reconnaissance tools.

## 🚀 Features

- **Multi-tool Integration**: Combines several powerful security tools in one interface
- **Modular Architecture**: Organized into distinct modules for different reconnaissance tasks
- **Optimized Output**: Clean, structured output with loading animations
- **Cross-platform**: Works on Linux, macOS, and other Unix-like systems
- **Directory Visualization**: Beautiful tree-like output directory structure
- **Progress Indicators**: Loading animations for better UX

## 🛠️ Modules

ENIGMA CLI comes with several modules to handle different aspects of reconnaissance:

### Enumeration
- **Subdomain Discovery**: Uses Subfinder and Assetfinder to discover subdomains
- **Result Merging**: Combines results from multiple tools
- **Alive Hosts**: Checks which subdomains are responsive with HTTPX

### Information Gathering
- **WHOIS Lookup**: Retrieves domain registration and ownership information
- **Registrar Details**: Gets contact information, creation/expiration dates, name servers

### Crawling
- **Live Crawling**: Uses Katana to discover hidden paths in real-time
- **Archive Crawling**: Uses Waybackurls to find historical URLs from the Internet Archive

### Path Finder
- **Admin Finder**: Identifies sensitive files and directories (admin panels, backups, etc.)

### SSL/TLS Scanner
- **SSL Configuration**: Checks for weak ciphers, expired certificates, insecure protocols

### Vulnerability Scanning
- **Nuclei Scanning**: Automatic vulnerability detection using Nuclei templates

### Additional Tools
- **Subdomain Takeover**: Uses Subjack for takeover detection
- **HTTP Probing**: Uses Httpx for status code and title detection
- **URL Gathering**: Uses GAU to fetch URLs from multiple sources
- **Comprehensive Enumeration**: Uses Amass for extensive DNS enumeration
- **Technology Detection**: Uses WhatWeb to detect web technologies

## 📦 Installation

### Prerequisites
- Python 3.7+
- Go programming language
- Git

### Automatic Installation
Run the installation script to set up all required dependencies:

```bash
python install.py
```

The installer will:
- Detect your operating system and Linux distribution
- Install Python packages (openai, psutil)
- Install system tools using appropriate package managers (apt for Ubuntu/Debian, pacman for Arch/Manjaro with AUR support)
- Create necessary output directories
- Set up API key file

### Manual Installation (Alternative)
For manual installation, you'll need to install these tools:

**Go-based tools** (install with `go install`):
- subfinder
- assetfinder
- katana
- waybackurls
- httpx
- nuclei
- subjack
- gau
- amass

**System packages**:
- sslscan
- whois
- whatweb
- tree
- okadminfinder

## 🔧 Usage

### Basic Command Structure
```bash
python enigma_cli.py [module] [arguments]
```

### Examples

**Subdomain Enumeration**:
```bash
# Basic enumeration
python enigma_cli.py enum --target example.com

# Merge results from multiple tools
python enigma_cli.py enum --target example.com --merge-results

# Check which subdomains are alive
python enigma_cli.py enum --target example.com --check-alive
```

**Information Gathering**:
```bash
python enigma_cli.py info --target example.com
```

**Web Crawling**:
```bash
# Live crawling
python enigma_cli.py crawl --target example.com --live

# Archive crawling
python enigma_cli.py crawl --target example.com --archive
```

**SSL/TLS Scanning**:
```bash
python enigma_cli.py ssl --target example.com
```

**Vulnerability Scanning**:
```bash
python enigma_cli.py vuln --target example.com
```

**Subdomain Takeover Detection**:
```bash
python enigma_cli.py takeover --target example.com
```

**HTTP Probing**:
```bash
python enigma_cli.py httpx --target example.com
```

**URL Gathering**:
```bash
python enigma_cli.py gau --target example.com
```

**Comprehensive Enumeration**:
```bash
python enigma_cli.py amass --target example.com
```

**Technology Detection**:
```bash
python enigma_cli.py tech --target example.com
```

**View Output Files**:
```bash
# List all output files
python enigma_cli.py output --list

# View specific output file
python enigma_cli.py output --file output/enumeration/example.com/subfinder.txt
```

**AI Assistant** (requires OpenAI API key):
```bash
python enigma_cli.py ai --query "How to find subdomains?"
python enigma_cli.py ai --query "What is subdomain enumeration?" --api-key your-api-key
```

**System Settings**:
```bash
python enigma_cli.py settings
```

## 📁 Output Structure

All outputs are organized in a clean directory structure under the `output/` folder:

```
output/
├── enumeration/        # Subdomain enumeration results
├── information/        # WHOIS and domain information
├── crawling/           # Crawling results (live & archive)
├── pathfinder/         # Path finding results
├── sslscan/            # SSL/TLS scan results
├── vulnerability/      # Nuclei vulnerability scan results
├── takeover/           # Subdomain takeover results
├── httpx/              # HTTP probing results
├── gau/                # URL gathering results
├── amass/              # Amass enumeration results
└── technologies/       # Technology detection results
```

## 💡 Tips for Bug Bounty Hunters

1. **Start with enumeration**: Always begin with subdomain discovery to expand your attack surface
2. **Check alive subdomains**: Use the alive check to filter out non-responsive domains
3. **Combine techniques**: Use both live and archive crawling for comprehensive path discovery
4. **Monitor for subdomain takeovers**: Regularly check for potential takeover opportunities
5. **Use technology detection**: Knowing the underlying tech stack helps in finding specific vulnerabilities
6. **Regular vulnerability scanning**: Run Nuclei regularly to catch common vulnerabilities

## 🔐 API Key Setup

For AI functionality, add your OpenAI API key:
1. Add it directly to `openai_apikey.txt` file
2. Or use the `--api-key` parameter with each AI command

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for educational and authorized security testing purposes only. The developer is not responsible for any misuse or illegal activities. Always ensure you have proper authorization before testing on any systems you do not own.

## 🐛 Issues & Support

If you encounter any issues or have suggestions for improvements, please open an issue on the repository.

---

**Developed by @Rosemary1337**
**Telegram: @stupidp3rson**
**TikTok: @justan0therloser**
