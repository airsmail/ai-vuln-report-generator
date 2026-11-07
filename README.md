# 🛡️ AI-Assisted Vulnerability Report Generator (Nmap + Local LLM)

## 📌 Overview
A homelab tool that scans a subnet with Nmap and asks a locally hosted LLM (via Ollama) to turn the results into a structured Markdown security report with risk levels and hardening suggestions. All analysis runs locally, so network details never leave your environment.

> This is a learning and homelab project. The report is an AI-generated summary of Nmap output, not a validated vulnerability assessment. Review the findings manually.

## 🏗️ Architecture & Technologies
- **Host:** Debian VM on Proxmox VE
- **Network discovery:** Nmap (`-sV --top-ports 100`)
- **AI analysis:** Ollama with a local model (default `hermes3:8b`)
- **Language:** Python (`python-nmap`, `requests`)
- **Scheduling (optional):** cron

## 🚀 How It Works
1. **Discovery:** Nmap scans the target subnet for active hosts, open ports and service versions.
2. **Parsing:** The results are structured into a JSON payload.
3. **AI evaluation:** The payload and `system_prompt.txt` are sent to the local Ollama API.
4. **Reporting:** A Markdown report with risk levels and mitigation suggestions is saved as `security_report_<timestamp>.md`.

## ⚙️ Setup
Requires Python 3, Nmap and a running Ollama instance.

```bash
pip install -r requirements.txt
ollama pull hermes3:8b
```

## ▶️ Usage
```bash
python ai_scanner.py --subnet 192.168.1.0/24 --model hermes3:8b
```

Options: `--subnet`, `--ollama` (default `http://localhost:11434`), `--model`.

Optional weekly run with cron (Sundays at 03:00):

```
0 3 * * 0 cd /opt/ai-scanner && /usr/bin/python3 ai_scanner.py --subnet 192.168.1.0/24
```

## 🔒 Privacy
Nmap output is processed only by a local model, so internal IP ranges and service details are not sent to external AI APIs.

## ⚠️ Limitations
- Findings are based on service banners from `nmap -sV`. Versions can be spoofed, and distributions such as Debian and Ubuntu often patch packages without changing the version number.
- The LLM can produce false positives or invented CVE references. Verify findings before acting on them.
- This is not a replacement for dedicated scanners such as OpenVAS or Nessus.
- Banner text is untrusted input and could try to influence the model's output.

## ⚖️ Responsible Use
Only scan networks you own or have written permission to scan.
