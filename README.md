

# 🛡️ Autonomous Vulnerability Scanner (Local AI-Powered)

## 📌 Project Overview
This project is an automated, zero-trust network vulnerability scanner designed for enterprise-grade homelab environments. It performs weekly network sweeps and utilizes strictly local Large Language Models (LLMs) to analyze vulnerabilities and generate actionable security reports.

## 🏗️ Architecture & Technologies
* **Infrastructure:** Proxmox VE, K3s / Debian
* **Network Sweeping:** Nmap
* **AI Analysis:** Ollama (Hermes 3 / Qwen 2.5 Coder) - *100% Local Inference*
* **Automation:** Cron
* **Language:** Python

## 🔒 Security Posture & Vision
In alignment with **ISO 27001** standards and **Zero-Trust** architecture:
* **No Cloud Data Leakage:** Unlike tools that send network topology data to OpenAI or external APIs, this pipeline processes all Nmap outputs through local AI models. Sensitive internal IP structures never leave the local network.
* **Continuous Monitoring:** Simulates an automated Blue Team workflow by periodically scanning assets and highlighting outdated services (e.g., legacy SSH/SMB protocols).

## 🚀 How It Works
1. **Discovery:** `nmap` scans the target subnet for active hosts and open ports/services.
2. **Data Parsing:** Results are structured into a JSON payload.
3. **AI Evaluation:** The local Ollama API evaluates the payload using a custom cybersecurity-focused system prompt.
4. **Reporting:** A structured Markdown report is generated, highlighting risk levels and mitigation strategies (e.g., enforcing Public Key authentication over passwords).
