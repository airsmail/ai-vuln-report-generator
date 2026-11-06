import nmap
import requests
import json
import argparse
from datetime import datetime

def scan_network(subnet):
    print(f"[*] Nmap taraması başlatılıyor: {subnet}")
    nm = nmap.PortScanner()
    # Hızlı ve versiyon tespiti yapan temel tarama
    nm.scan(hosts=subnet, arguments='-sV --top-ports 100 -T4')
    
    scan_results = {}
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            scan_results[host] = {'tcp': {}}
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    service = nm[host][proto][port]['name']
                    version = nm[host][proto][port]['version']
                    scan_results[host]['tcp'][port] = f"{service} {version}"
                    
    return json.dumps(scan_results, indent=2)

def generate_report(scan_data, ollama_url, model, prompt_file):
    print(f"[*] Ollama ({model}) API'sine analiz isteği gönderiliyor...")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    payload = {
        "model": model,
        "prompt": f"{system_prompt}\n\nTarama Sonuçları:\n{scan_data}",
        "stream": False
    }
    
    response = requests.post(f"{ollama_url}/api/generate", json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Hata: Yapay zeka sunucusuna ulaşılamadı. Kod: {response.status_code}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lokal Yapay Zeka Destekli Otonom Zafiyet Tarayıcı")
    parser.add_argument("--subnet", default="10.0.0.0/24", help="Taranacak hedef IP veya Subnet (Örn: 192.168.1.0/24)")
    parser.add_argument("--ollama", default="http://localhost:11434", help="Ollama API adresi")
    parser.add_argument("--model", default="hermes3:8b", help="Kullanılacak Ollama modeli")
    
    args = parser.parse_args()
    
    # 1. Ağı Tara
    nmap_data = scan_network(args.subnet)
    
    # 2. Raporu Üret
    ai_report = generate_report(nmap_data, args.ollama, args.model, "system_prompt.txt")
    
    # 3. Dosyaya Kaydet
    filename = f"security_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(ai_report)
        
    print(f"[+] Başarılı! Zafiyet raporu oluşturuldu: {filename}")