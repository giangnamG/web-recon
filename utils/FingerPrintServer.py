import os
import xml.etree.ElementTree as ET
import socket
import re
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

REPORTS_DIR = "reports/"

class FingerPrintServer:
    def __init__(self, url, silent=True):
        self.url = url
        self.ip_address = self.get_ip()
        self.silent = silent  # Ẩn log nếu silent=True
        self.console = Console()

    def get_ip(self):
        """Lấy địa chỉ IP của domain"""
        try:
            return socket.gethostbyname(self.url)
        except socket.gaierror:
            return "Không thể lấy IP"

    def run_command(self, cmd, description):
        """Chạy lệnh shell và hiển thị tiến trình"""
        with self.console.status(f"[bold cyan]{description}...[/bold cyan]"):
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = result.stdout.strip()
                self.console.print(f"[green]✔ Hoàn thành:[/green] {description}")  # In ra sau khi chạy xong
                return output
            except Exception as e:
                return f"Lỗi: {e}"

    def NMapScan(self):
        """Chạy nmap để lấy thông tin cổng & tiêu đề HTTP"""
        output_file = f"{REPORTS_DIR}/output.xml"
        nmap_cmd = f"nmap --script=http-title,http-server-header {self.url} -F -oX {output_file}"

        with self.console.status("[bold yellow]🔍 Đang chạy Nmap scan...[/bold yellow]"):
            if self.silent:
                with open(os.devnull, 'w') as devnull:
                    subprocess.run(nmap_cmd, shell=True, stdout=devnull, stderr=devnull)
            else:
                subprocess.run(nmap_cmd, shell=True)

        if not os.path.exists(output_file):
            self.console.print("[bold red]❌ Không tìm thấy file output.xml! Có thể Nmap gặp lỗi.[/bold red]")
            return None

        self.console.print("[green]✔ Hoàn thành: Nmap scan[/green]")

        try:
            tree = ET.parse(output_file)
            root = tree.getroot()
            results = {"target": self.url, "ip": self.ip_address, "ports": []}

            for host in root.findall("host"):
                for port in host.findall("ports/port"):
                    port_id = port.get("portid")
                    service = port.find("service")
                    script_results = {}

                    for script in port.findall("script"):
                        script_id = script.get("id")
                        script_output = script.get("output")
                        script_results[script_id] = script_output

                    results["ports"].append({
                        "port": port_id,
                        "service": service.get("name") if service is not None else "unknown",
                        "scripts": script_results
                    })

            return results
        except Exception as e:
            self.console.print(f"[bold red]⚠️ Lỗi xử lý XML: {e}[/bold red]")
            return None

    def WhatWebScan(self):
        """Dùng WhatWeb để phát hiện công nghệ web"""
        return self.run_command(f"whatweb -a 3 {self.url}", "🛠 Đang phân tích công nghệ web (WhatWeb)")

    def WhoIsScan(self):
        """Lấy thông tin WHOIS"""
        return self.run_command(f"whois {self.url}", "📄 Đang lấy thông tin WHOIS")

    def display_report(self, nmap_results, whois_data, whatweb_data):
        """Hiển thị báo cáo chi tiết trên terminal"""
        self.console.print(Panel(f"📌 [bold cyan]Báo cáo Fingerprint Server: {self.url} ({self.ip_address})[/bold cyan]", expand=False))

        # Hiển thị kết quả Nmap
        table = Table(title="Thông tin cổng mở", show_lines=True)
        table.add_column("Cổng", style="bold yellow", justify="center")
        table.add_column("Dịch vụ", style="bold green", justify="left")
        table.add_column("Scripts", style="bold blue", justify="left")

        if not nmap_results["ports"]:
            self.console.print("[bold red]❌ Không tìm thấy cổng mở nào.[/bold red]\n")
        else:
            for port in nmap_results["ports"]:
                script_output = "\n".join([f"[{k}] {v}" for k, v in port["scripts"].items()])
                table.add_row(port["port"], port["service"], script_output if script_output else "[gray]Không có dữ liệu[/gray]")
            self.console.print(table)

        # Hiển thị dữ liệu khác
        self.console.print(Panel(f"[bold yellow]🌍 WHOIS Information:[/bold yellow]\n{whois_data}", expand=False))
        self.console.print(Panel(f"[bold magenta]🛠 WhatWeb Scan:[/bold magenta]\n{whatweb_data}", expand=False))

    def run(self):
        """Chạy tất cả các công cụ và hiển thị báo cáo"""
        self.console.print("[bold cyan]🔍 Đang thực hiện Fingerprint Server...[/bold cyan]\n")

        # Chạy quét fingerprint với thông báo tiến trình
        nmap_results = self.NMapScan()
        whois_data = self.WhoIsScan()
        whatweb_data = self.WhatWebScan()

        # Hiển thị báo cáo
        if nmap_results:
            self.display_report(nmap_results, whois_data, whatweb_data)
        else:
            self.console.print("[bold red]⚠️ Không thể thu thập dữ liệu Nmap.[/bold red]")
