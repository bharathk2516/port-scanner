"""
Network Port Scanner
--------------------
Scans a target IP/hostname for open ports.
Supports single port, port range, and common ports scan.
Author: [Your Name]
"""

import socket
import sys
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Common ports and their services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}

open_ports = []
lock = threading.Lock()


def banner():
    print("""
╔══════════════════════════════════════════════╗
║         Network Port Scanner v1.0            ║
║     Scan open ports on any IP/hostname       ║
╚══════════════════════════════════════════════╝
    """)


def resolve_host(target: str) -> str:
    """Resolve hostname to IP address."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"[✗] Cannot resolve host: {target}")
        sys.exit(1)


def scan_port(ip: str, port: int, timeout: float = 1.0) -> bool:
    """
    Try to connect to a port.
    Returns True if open, False if closed/filtered.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def get_service(port: int) -> str:
    """Get service name for a port."""
    if port in COMMON_PORTS:
        return COMMON_PORTS[port]
    try:
        return socket.getservbyport(port)
    except Exception:
        return "Unknown"


def scan_ports(ip: str, ports: list, max_threads: int = 100) -> list:
    """Scan multiple ports using threading for speed."""
    results = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {
            executor.submit(scan_port, ip, port): port for port in ports
        }

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                is_open = future.result()
                if is_open:
                    service = get_service(port)
                    results.append((port, service))
                    print(f"  [OPEN]  Port {port:<6} → {service}")
            except Exception:
                pass

    return sorted(results)


def print_summary(target: str, ip: str, results: list, start_time: datetime):
    """Print scan summary."""
    duration = (datetime.now() - start_time).total_seconds()
    print("\n" + "─" * 48)
    print(f"  Target   : {target} ({ip})")
    print(f"  Open     : {len(results)} port(s) found")
    print(f"  Duration : {duration:.2f} seconds")
    print("─" * 48)

    if results:
        print("\n  PORT     SERVICE")
        print("  ──────────────────────")
        for port, service in results:
            print(f"  {port:<8} {service}")
    else:
        print("\n  No open ports found.")
    print()


def print_usage():
    print("""
Usage:
  python port_scanner.py <target> <mode> [options]

Modes:
  common              Scan most common 17 ports
  range <start> <end> Scan a range of ports
  single <port>       Scan a single port

Examples:
  python port_scanner.py scanme.nmap.org common
  python port_scanner.py 192.168.1.1 range 1 1024
  python port_scanner.py google.com single 443

⚠️  Only scan systems you own or have permission to scan.
""")


def main():
    banner()

    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    target = sys.argv[1]
    mode = sys.argv[2].lower()

    # Resolve host
    print(f"[*] Resolving host: {target}")
    ip = resolve_host(target)
    print(f"[*] Target IP     : {ip}")
    print(f"[*] Scan started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Mode          : {mode}\n")

    start_time = datetime.now()

    if mode == "common":
        ports = list(COMMON_PORTS.keys())
        print(f"[*] Scanning {len(ports)} common ports...\n")
        results = scan_ports(ip, ports)

    elif mode == "range":
        if len(sys.argv) < 5:
            print("[✗] Range mode needs start and end ports.")
            print("    Example: python port_scanner.py 192.168.1.1 range 1 1024")
            sys.exit(1)
        start_port = int(sys.argv[3])
        end_port = int(sys.argv[4])
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print("[✗] Invalid port range. Use 1-65535.")
            sys.exit(1)
        ports = list(range(start_port, end_port + 1))
        print(f"[*] Scanning ports {start_port}-{end_port} ({len(ports)} ports)...\n")
        results = scan_ports(ip, ports)

    elif mode == "single":
        if len(sys.argv) < 4:
            print("[✗] Single mode needs a port number.")
            print("    Example: python port_scanner.py google.com single 443")
            sys.exit(1)
        port = int(sys.argv[3])
        print(f"[*] Scanning port {port}...\n")
        is_open = scan_port(ip, port)
        service = get_service(port)
        if is_open:
            print(f"  [OPEN]  Port {port} → {service}")
            results = [(port, service)]
        else:
            print(f"  [CLOSED] Port {port} → {service}")
            results = []

    else:
        print(f"[✗] Unknown mode: '{mode}'")
        print_usage()
        sys.exit(1)

    print_summary(target, ip, results, start_time)


if __name__ == "__main__":
    main()
