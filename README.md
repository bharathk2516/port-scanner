# 🌐 Network Port Scanner

A fast, multi-threaded command-line **port scanner** built in Python. Scan any IP address or hostname to discover open ports and running services — just like real security professionals do.

---

## 🛡️ How It Works

```
Target (IP/Hostname)
        │
        ▼
  DNS Resolution       ← Converts hostname to IP
        │
        ▼
  TCP Connect Scan     ← Tries to connect to each port
  (Multi-threaded)     ← 100 threads run simultaneously
        │
        ▼
  Open / Closed?       ← connect_ex() returns 0 if open
        │
        ▼
  Service Detection    ← Maps port to known service name
        │
        ▼
  Results Summary      ← Displays all open ports + services
```

### Key concepts used:
| Concept | What it does |
|---|---|
| **TCP Connect Scan** | Attempts a full TCP connection to detect open ports |
| **Multi-threading** | Scans 100 ports simultaneously for speed |
| **DNS Resolution** | Converts hostnames like google.com to IP addresses |
| **Socket Programming** | Low-level network connections using Python sockets |
| **Service Detection** | Maps port numbers to known services (HTTP, SSH, etc.) |

---

## 📦 Requirements

No external libraries needed! Uses only Python standard library.

```bash
python port_scanner.py  # That's it!
```

---

## 🚀 Usage

### Scan common ports (fastest)
```bash
python port_scanner.py <target> common
```
```bash
python port_scanner.py scanme.nmap.org common
```

### Scan a range of ports
```bash
python port_scanner.py <target> range <start> <end>
```
```bash
python port_scanner.py 192.168.1.1 range 1 1024
```

### Scan a single port
```bash
python port_scanner.py <target> single <port>
```
```bash
python port_scanner.py google.com single 443
```

---

## 🧪 Example Output

```
╔══════════════════════════════════════════════╗
║         Network Port Scanner v1.0            ║
║     Scan open ports on any IP/hostname       ║
╚══════════════════════════════════════════════╝

[*] Resolving host: scanme.nmap.org
[*] Target IP     : 45.33.32.156
[*] Scan started  : 2026-04-20 07:30:00
[*] Mode          : common

[*] Scanning 17 common ports...

  [OPEN]  Port 22     → SSH
  [OPEN]  Port 80     → HTTP

────────────────────────────────────────────────
  Target   : scanme.nmap.org (45.33.32.156)
  Open     : 2 port(s) found
  Duration : 2.14 seconds
────────────────────────────────────────────────

  PORT     SERVICE
  ──────────────────────
  22       SSH
  80       HTTP
```

---

## 🔍 Common Ports Scanned

| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 3389 | RDP |
| 8080 | HTTP-Alt |

---

## ⚠️ Legal Warning

> Only scan systems you **own** or have **explicit permission** to scan. Unauthorized port scanning may be illegal in your country. This tool is for **educational purposes only**.

---

## 💡 What I Learned

- How TCP connections work at the socket level
- The difference between open, closed, and filtered ports
- How to use Python threading for faster network scanning
- DNS resolution and hostname to IP conversion
- How real tools like Nmap work under the hood

---

## 📚 References

- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [TCP/IP Guide](http://www.tcpipguide.com/)
- [Nmap — The Network Mapper](https://nmap.org/)
