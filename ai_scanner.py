import argparse
import json
from datetime import datetime

import nmap
import requests


def scan_network(subnet):
    print(f"[*] Nmap taraması başlatılıyor: {subnet}")
    nm = nmap.PortScanner()
    # Hızlı ve versiyon tespiti yapan temel tarama
    nm.scan(hosts=subnet, arguments="-sV --top-ports 100 -T4")

    scan_results = {}
    for host in nm.all_hosts():
        if nm[host].state() != "up":
            continue
        scan_results[host] = {}
        for proto in nm[host].all_protocols():
            scan_results[host][proto] = {}
            for port, info in nm[host][proto].items():
                scan_results[host][proto][port] = f"{info['name']} {info['version']}".strip()

    return json.dumps(scan_results, indent=2)


def generate_report(scan_data, ollama_url, model, prompt_file):
    print(f"[*] Ollama ({model}) API'sine analiz isteği gönderiliyor...")

    with open(prompt_file, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    payload = {
        "model": model,
        "prompt": f"{system_prompt}\n\nTarama Sonuçları:\n{scan_data}",
        "stream": False,
    }

    try:
        response = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=300)
        response.raise_for_status()
        return response.json()["response"]
    except requests.RequestException as exc:
        return f"Hata: Yapay zeka sunucusuna ulaşılamadı: {exc}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lokal Yapay Zeka Destekli Zafiyet Raporu Üreticisi")
    parser.add_argument("--subnet", default="10.0.0.0/24", help="Taranacak hedef IP veya subnet (Örn: 192.168.1.0/24)")
    parser.add_argument("--ollama", default="http://localhost:11434", help="Ollama API adresi")
    parser.add_argument("--model", default="hermes3:8b", help="Kullanılacak Ollama modeli")

    args = parser.parse_args()

    print("[!] Yalnızca sahibi olduğunuz veya yazılı izin aldığınız ağları tarayın.")

    # 1. Ağı tara
    nmap_data = scan_network(args.subnet)

    # 2. Raporu üret
    ai_report = generate_report(nmap_data, args.ollama, args.model, "system_prompt.txt")

    # 3. Dosyaya kaydet
    filename = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ai_report)

    print(f"[+] Başarılı! Zafiyet raporu oluşturuldu: {filename}")
