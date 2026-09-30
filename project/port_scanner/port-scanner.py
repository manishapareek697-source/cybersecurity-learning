# import socket

# print("DEBUG: Script started!")
# target = "127.0.0.1"
# print(f"DEBUG: Target is {target}")

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("DEBUG: Socket created!")

# sock.settimeout(1)
# result = sock.connect_ex((target, 80))
# print(f"DEBUG: Connection result = {result}")

# if result == 0:
#     print("[+] Port 80 is OPEN")
# else:
#     print("[-] Port 80 is CLOSED")

# sock.close()
# print("DEBUG: Script ended!")

  


# import socket

# target = "127.0.0.1"

# print("=" * 50)
# print(f"Scanning target: {target}")
# print("=" * 50)

# # Check common ports
# common_ports = [21, 22, 80, 443, 3306, 5432, 8000, 8080, 8443, 9000]

# open_ports = []

# for port in common_ports:
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(1)
#     result = sock.connect_ex((target, port))
    
#     if result == 0:
#         print(f"[+] Port {port} is OPEN")
#         open_ports.append(port)
#     else:
#         print(f"[-] Port {port} is CLOSED")
    
#     sock.close()

# print("=" * 50)
# if open_ports:
#     print(f"Found {len(open_ports)} open port(s): {open_ports}")
# else:
#     print("No open ports found on common ports")
# print("=" * 50)


# import socket

# target = "127.0.0.1"

# # Service names for common ports
# services = {
#     21: "FTP",
#     22: "SSH",
#     80: "HTTP",
#     443: "HTTPS",
#     3306: "MySQL",
#     5432: "PostgreSQL",
#     8000: "Web Server",
#     8080: "Alt Web",
#     8443: "Alt HTTPS",
#     9000: "App Server"
# }

# print("=" * 60)
# print(f"🔍 Network Vulnerability Scanner")
# print(f"Target: {target}")
# print("=" * 60)

# common_ports = [21, 22, 80, 443, 3306, 5432, 8000, 8080, 8443, 9000]
# open_ports = []
# total = len(common_ports)

# for index, port in enumerate(common_ports):
#     # Progress bar
#     progress = (index + 1) / total * 100
#     bar_length = int(progress / 5)
#     bar = "█" * bar_length + "░" * (20 - bar_length)
#     print(f"[{bar}] {progress:.0f}% - Scanning port {port}...", end="\r")
    
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(1)
#     result = sock.connect_ex((target, port))
    
#     if result == 0:
#         service_name = services.get(port, "Unknown")
#         print(f"[+] Port {port:5d} is OPEN  | Service: {service_name:15s}")
#         open_ports.append((port, service_name))
    
#     sock.close()

# # Summary
# print("=" * 60)
# print(f"✅ Scan Complete!")
# print("=" * 60)

# if open_ports:
#     print(f"\n🎯 Found {len(open_ports)} Open Port(s):\n")
#     for port, service in open_ports:
#         print(f"   Port {port:5d} → {service}")
#     print()
# else:
#     print("\n⚠️ No open ports found on common ports\n")

# print("=" * 60)




import socket

target = "127.0.0.1"

# Service names for common ports
services = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8000: "Web Server",
    8080: "Alt Web",
    8443: "Alt HTTPS",
    9000: "App Server"
}

print("=" * 60)
print(f"🔍 Network Vulnerability Scanner")
print(f"Target: {target}")
print("=" * 60)

common_ports = [21, 22, 80, 443, 3306, 5432, 8000, 8080, 8443, 9000]
open_ports = []
total = len(common_ports)

for index, port in enumerate(common_ports):
    # Progress bar
    progress = (index + 1) / total * 100
    bar_length = int(progress / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    print(f"[{bar}] {progress:.0f}% - Scanning port {port}...", end="\r")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    
    if result == 0:
        service_name = services.get(port, "Unknown")
        print(f"[+] Port {port:5d} is OPEN  | Service: {service_name:15s}")
        open_ports.append((port, service_name))
    
    sock.close()

# Summary
print("=" * 60)
print(f"✅ Scan Complete!")
print("=" * 60)

if open_ports:
    print(f"\n🎯 Found {len(open_ports)} Open Port(s):\n")
    for port, service in open_ports:
        print(f"   Port {port:5d} → {service}")
    print()
else:
    print("\n⚠️ No open ports found on common ports\n")

print("=" * 60)