# ClipSnatch 🎯

**ClipSnatch** is an educational Kali Linux tool to demonstrate how clipboard data can be accessed via browser-based social engineering. It provides a CLI-based GUI, customizable phishing templates, and automatic tunneling using Cloudflared.

> ⚠️ This tool is strictly for educational purposes. Do not use it without proper authorization.

---

## 🚀 Features

* 💅 **CLI-based GUI** for interaction and setup
* 🌭 **3 Social Engineering Templates**:

  * ✅ Amazon Gift Card (shows half code and copy button)
  * ✅ CAPTCHA Verification (fake human verification)
  * ✅ Google Docs Access Request (mimics Google Docs sharing)
* 📋 **Clipboard Capture** via JavaScript’s Clipboard API
* 🌐 **Cloudflared Tunnel Integration**:

  * Checks for `cloudflared` in system or downloads it automatically
  * Exposes Flask server to the internet using Cloudflare tunnel
* 🧠 **Link Display**:

  * Shows both **direct** and **DNS-masked (@)** links
* 🔒 **Clean Output**:

  * Suppresses Flask and Cloudflared banner logs
  * Displays clipboard content live in terminal after tunnel creation
* 🛠️ **Auto Dependency Handling**:

  * Installs Flask if not already present
  * Supports Linux (Debian/Kali tested)

---

## 📦 Folder Structure

```
ClipCLI/
├── main.py             # Main CLI tool
├── server.py           # Flask server for serving templates
├── templates/
│   ├── amazon.html     # Amazon Gift Card phishing template
│   ├── captcha.html    # CAPTCHA Verification phishing template
│   └── googledoc.html  # Google Docs phishing template
├── cloudflared         # Cloudflared binary (optional, auto-download if missing)
└── README.md
```

---

## 🛠️ Usage

```bash
git clone https://github.com/ritvijgaur/ClipSnatch
cd ClipSnatch
python3 main.py
```

### 🔧 Steps Inside the Tool

1. Select one of the three phishing templates.
2. Choose whether to generate a DNS-masked link (`victim.com@cloudflare-link`) or not.
3. Tool launches server and shows:

   * Direct link
   * DNS-masked link
4. When victim interacts, their clipboard data appears live in terminal.

---

## 🎨 Templates Overview

| Template    | Description                                | Trigger                     |
| ----------- | ------------------------------------------ | --------------------------- |
| Amazon Gift | Half-hidden gift code + “Copy Code” button | Clipboard permission prompt |
| CAPTCHA     | Fake "I am not a robot" button             | Clipboard prompt            |
| Google Docs | Simulated shared document                  | Clipboard prompt            |

All templates are customizable in the `/templates` folder using basic HTML/CSS/JS.

---

## 🧹 Customization

Want to build your own template?

1. Copy any existing HTML in `/templates`.
2. Modify visuals, wording, or behavior.
3. Update `server.py` to add a route.
4. Run `main.py` and select your new template.
