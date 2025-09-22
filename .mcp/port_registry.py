#!/usr/bin/env python3
"""
Port Registry System for Claude Life Project
Tracks active ports and prevents conflicts during development
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import socket
import psutil

class PortRegistry:
    def __init__(self, registry_file: str = None):
        if registry_file is None:
            self.registry_file = os.path.join(os.path.dirname(__file__), "ports.json")
        else:
            self.registry_file = registry_file

        # Known service ports for this project
        self.known_services = {
            8000: "FastAPI Development Server",
            8001: "Claude Life Business API",
            3000: "Next.js Development Server",
            3001: "React Development Server",
            5432: "PostgreSQL Database",
            6379: "Redis Server",
            7687: "Neo4j Bolt",
            7474: "Neo4j HTTP",
            9090: "Prometheus",
            3306: "MySQL",
            27017: "MongoDB",
            5000: "Flask Development",
            4000: "Express.js Development",
            8080: "Alternative HTTP",
            8443: "HTTPS Alternative",
            9000: "Various Development Tools"
        }

    def scan_active_ports(self) -> List[Dict]:
        """Scan for currently active ports and their processes"""
        active_ports = []

        try:
            # Try psutil first
            connections = psutil.net_connections(kind='inet')

            for conn in connections:
                if conn.status == 'LISTEN' and conn.laddr:
                    port_info = {
                        'port': conn.laddr.port,
                        'address': conn.laddr.ip,
                        'protocol': 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP',
                        'process': None,
                        'command': None,
                        'service': self.known_services.get(conn.laddr.port, "Unknown"),
                        'timestamp': datetime.now().isoformat()
                    }

                    # Get process information
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            port_info['process'] = {
                                'pid': conn.pid,
                                'name': process.name(),
                                'cmdline': ' '.join(process.cmdline()) if process.cmdline() else None,
                                'user': process.username() if hasattr(process, 'username') else None
                            }
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            pass

                    active_ports.append(port_info)

        except Exception as e:
            print(f"Error with psutil, falling back to lsof: {e}")
            # Fallback to lsof command
            active_ports = self._scan_with_lsof()

        return sorted(active_ports, key=lambda x: x['port'])

    def _scan_with_lsof(self) -> List[Dict]:
        """Fallback method using lsof command"""
        active_ports = []
        try:
            # Use lsof to find listening ports
            result = subprocess.run(['lsof', '-i', '-P', '-n'],
                                  capture_output=True, text=True, timeout=10)

            for line in result.stdout.split('\n')[1:]:  # Skip header
                if 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) >= 9:
                        command = parts[0]
                        pid = parts[1]
                        user = parts[2]
                        address_port = parts[8]

                        # Extract port from address:port format
                        if ':' in address_port:
                            try:
                                port = int(address_port.split(':')[-1])
                                address = address_port.split(':')[0] if address_port.split(':')[0] else '*'

                                port_info = {
                                    'port': port,
                                    'address': address,
                                    'protocol': 'TCP',
                                    'process': {
                                        'pid': int(pid),
                                        'name': command,
                                        'cmdline': command,
                                        'user': user
                                    },
                                    'service': self.known_services.get(port, "Unknown"),
                                    'timestamp': datetime.now().isoformat()
                                }
                                active_ports.append(port_info)
                            except ValueError:
                                continue

        except Exception as e:
            print(f"Error with lsof fallback: {e}")

        return active_ports

    def is_port_available(self, port: int, host: str = 'localhost') -> bool:
        """Check if a specific port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                return result != 0
        except Exception:
            return False

    def find_available_port(self, start_port: int = 8000, end_port: int = 9000) -> Optional[int]:
        """Find the next available port in a range"""
        for port in range(start_port, end_port + 1):
            if self.is_port_available(port):
                return port
        return None

    def save_registry(self, active_ports: List[Dict]):
        """Save current port registry to file"""
        registry_data = {
            'last_updated': datetime.now().isoformat(),
            'active_ports': active_ports,
            'known_services': self.known_services,
            'project_ports': {
                'development': list(range(8000, 8010)),
                'testing': list(range(8010, 8020)),
                'staging': list(range(8020, 8030)),
                'databases': [5432, 6379, 7687, 7474, 3306, 27017],
                'reserved': [80, 443, 22, 21, 25, 53, 110, 143, 993, 995]
            }
        }

        try:
            with open(self.registry_file, 'w') as f:
                json.dump(registry_data, f, indent=2)
        except Exception as e:
            print(f"Error saving registry: {e}")

    def load_registry(self) -> Dict:
        """Load existing port registry"""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading registry: {e}")
        return {}

    def print_port_status(self):
        """Print human-readable port status"""
        active_ports = self.scan_active_ports()

        print("🔌 ACTIVE PORTS REGISTRY")
        print("=" * 50)
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        if not active_ports:
            print("No active ports detected.")
            return

        # Group by port ranges
        development_ports = [p for p in active_ports if 8000 <= p['port'] <= 8999]
        database_ports = [p for p in active_ports if p['port'] in [5432, 6379, 7687, 7474, 3306, 27017]]
        system_ports = [p for p in active_ports if p['port'] < 1024]
        other_ports = [p for p in active_ports if p not in development_ports + database_ports + system_ports]

        sections = [
            ("🚀 Development Ports (8000-8999)", development_ports),
            ("🗄️  Database Ports", database_ports),
            ("⚙️  System Ports (<1024)", system_ports),
            ("📡 Other Ports", other_ports)
        ]

        for section_name, ports in sections:
            if ports:
                print(f"{section_name}")
                print("-" * 30)
                for port in ports:
                    status = "🟢 AVAILABLE" if self.is_port_available(port['port']) else "🔴 IN USE"
                    print(f"  Port {port['port']:5} | {status} | {port['service']}")
                    if port['process']:
                        print(f"         └─ Process: {port['process']['name']} (PID: {port['process']['pid']})")
                        if port['process']['cmdline']:
                            cmd = port['process']['cmdline'][:80] + "..." if len(port['process']['cmdline']) > 80 else port['process']['cmdline']
                            print(f"         └─ Command: {cmd}")
                print()

    def suggest_port(self, service_name: str = "development") -> Tuple[int, str]:
        """Suggest an available port for a new service"""
        # Default port ranges by service type
        ranges = {
            'development': (8000, 8009),
            'api': (8010, 8019),
            'frontend': (3000, 3009),
            'testing': (8020, 8029),
            'database': (5430, 5439),
            'cache': (6380, 6389)
        }

        start, end = ranges.get(service_name, (8000, 8999))
        suggested_port = self.find_available_port(start, end)

        if suggested_port:
            return suggested_port, f"✅ Port {suggested_port} is available for {service_name}"
        else:
            # Fallback to wider range
            fallback_port = self.find_available_port(8000, 9000)
            if fallback_port:
                return fallback_port, f"⚠️  Preferred range full. Port {fallback_port} available as fallback"
            else:
                return None, f"❌ No ports available in development range (8000-9000)"

def main():
    registry = PortRegistry()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "scan":
            registry.print_port_status()
            active_ports = registry.scan_active_ports()
            registry.save_registry(active_ports)

        elif command == "suggest":
            service = sys.argv[2] if len(sys.argv) > 2 else "development"
            port, message = registry.suggest_port(service)
            print(message)

        elif command == "check":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else None
            if port:
                available = registry.is_port_available(port)
                status = "🟢 AVAILABLE" if available else "🔴 IN USE"
                print(f"Port {port}: {status}")
            else:
                print("Usage: port_registry.py check <port_number>")

        elif command == "save":
            active_ports = registry.scan_active_ports()
            registry.save_registry(active_ports)
            print(f"Registry saved to {registry.registry_file}")

        else:
            print("Usage: port_registry.py [scan|suggest|check|save] [args]")
    else:
        # Default: show status
        registry.print_port_status()

if __name__ == "__main__":
    main()