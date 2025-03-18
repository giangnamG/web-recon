import os
import subprocess
from rich.console import Console
from rich.panel import Panel
import re
from dotenv import load_dotenv

import requests
from rich.table import Table
from bs4 import BeautifulSoup
from rich import box


load_dotenv()
DNS_DUMPSTER_API_KEY = os.getenv("DNS_DUMPSTER_API_KEY")

REPORTS_DIR = "reports"

class ExternalTools:
    def __init__(self, silent=True):
        self.silent = silent  # Ẩn log nếu silent=True
        self.console = Console()

    def dnsdumpster(self, target):
        target = target.split("://")[-1]
        self.console.print(f"[bold cyan]🔍 Đang chạy trích xuất thông tin từ DNSDumpster cho URL: {target}...[/bold cyan]")
        host = f"https://api.dnsdumpster.com/domain/{target}"
        
        res = requests.get(
                url=host,
                headers={
                    'X-API-Key': DNS_DUMPSTER_API_KEY
                }
            )
        json_data = res.json()
        
        
        # Hiển thị tất cả các bản ghi A
        # Hiển thị tất cả các bản ghi A
        if "a" in json_data:
            self.console.print(f"\n[bold cyan]A Records (subdomains from dataset):[/bold cyan]")
            table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
            table.add_column("Host", style="dim")
            table.add_column("IP", style="dim")
            table.add_column("ASN", style="dim")
            table.add_column("ASN Name", style="dim")
            table.add_column("Open Services (from DB)", style="dim")
            table.add_column("HTTPS", style="dim")
            table.add_column("RevIP", style="dim")
            
            for record in json_data["a"]:
                for ip in record.get("ips", []):
                    # Highlight IP
                    ip_address = f"[bold red]{ip['ip']}[/bold red]"
                    
                    # Highlight các chuỗi khác (ví dụ: banner ssh, http, https)
                    ssh_banner = f"[bold green]{ip.get('banners', {}).get('ssh', {}).get('banner', 'N/A')}[/bold green]"
                    http_server = f"[bold yellow]{ip.get('banners', {}).get('http', {}).get('server', 'N/A')}[/bold yellow]"
                    https_server = f"[bold blue]{ip.get('banners', {}).get('https', {}).get('server', 'N/A')}[/bold blue]"
                    
                    # Highlight chuỗi title
                    title = f"[underline]{ip.get('banners', {}).get('https', {}).get('title', 'N/A')}[/underline]"

                    # Các giá trị khác
                    alt_n = ip.get('banners', {}).get('https', {}).get('alt_n', 'N/A')
                    apps = ", ".join(ip.get('banners', {}).get('https', {}).get('apps', []))
                    cn = ip.get('banners', {}).get('https', {}).get('cn', 'N/A')
                    redirect_location = ip.get('banners', {}).get('https', {}).get('redirect_location', 'N/A')
                    server = ip.get('banners', {}).get('https', {}).get('server', 'N/A')
                    
                    # Thêm các row vào bảng với các giá trị đã highlight
                    table.add_row(
                        record["host"],
                        ip_address,
                        f"ASN:{ip['asn']}",
                        ip["asn_name"],
                        f"ssh: {ssh_banner}\nhttp: {http_server}\n",
                        f"https: {https_server}\ntitle: {title}\nalt_n: {alt_n}\napps: {apps}\ncn: {cn}\n"
                        f"redirect_location: {redirect_location}\nserver: {server}\n",
                        ip.get("ptr", "N/A")
                    )
            self.console.print(table)

        # Hiển thị các bản ghi MX
        if "mx" in json_data:
            self.console.print(f"\n[bold cyan]MX Records:[/bold cyan]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Host", style="dim")
            table.add_column("IP", style="dim")
            table.add_column("ASN", style="dim")
            table.add_column("ASN Name", style="dim")
            table.add_column("PTR", style="dim")
            
            for record in json_data["mx"]:
                for ip in record.get("ips", []):
                    table.add_row(
                        record["host"],
                        ip["ip"],
                        f"ASN:{ip['asn']}",
                        ip["asn_name"],
                        ip.get("ptr", "N/A")
                    )
            self.console.print(table)

        # Hiển thị các bản ghi NS
        if "ns" in json_data:
            self.console.print(f"\n[bold cyan]NS Records:[/bold cyan]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Host", style="dim")
            table.add_column("IP", style="dim")
            table.add_column("ASN", style="dim")
            table.add_column("ASN Name", style="dim")
            table.add_column("PTR", style="dim")
            
            for record in json_data["ns"]:
                for ip in record.get("ips", []):
                    table.add_row(
                        record["host"],
                        ip["ip"],
                        f"ASN:{ip['asn']}",
                        ip["asn_name"],
                        ip.get("ptr", "N/A")
                    )
            self.console.print(table)

        # Hiển thị TXT Records
        if "txt" in json_data:
            self.console.print(f"\n[bold cyan]TXT Records:[/bold cyan]")
            for txt_record in json_data["txt"]:
                self.console.print(f"[bold yellow]{txt_record}[/bold yellow]")

                
class EnumerateWebServer:
    def __init__(self, url, silent=True, wordlist_path="/usr/share/seclists/Discovery/Web-Content/common.txt"):
        self.url = url
        self.silent = silent  # Ẩn log nếu silent=True
        self.console = Console()
        self.wordlist_path = wordlist_path
        self.externalTools = ExternalTools()
        
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

    def DigScan(self):
        """Lấy thông tin DNS bằng dig với DNS server khác và nhiều loại bản ghi"""
        dns_server = "8.8.8.8"  # Google DNS để tránh lỗi từ DNS cục bộ
        dig_cmd = (
            f"dig @{dns_server} {self.url} A AAAA MX NS TXT CNAME SOA +trace +multiline +nocmd +nocomments"
        )
        return self.run_command(dig_cmd, "📡 Đang thu thập thông tin DNS chi tiết")

    def TraceRouteScan(self):
        """Chạy traceroute để xem đường đi của gói tin"""
        host = self.url.split("://")[-1]
        raw_output = self.run_command(f"traceroute -n {host}", "🛤 Đang kiểm tra đường đi của gói tin (Traceroute)")
        return self.parse_traceroute_output(raw_output)

    def parse_traceroute_output(self, output):
        """Xử lý output của Traceroute để loại bỏ dòng `* * *` nhưng giữ nguyên format"""
        lines = output.split("\n")
        parsed_data = []

        for line in lines:
            # Bỏ qua các dòng chỉ có dấu `* * *` (timeout)
            if re.match(r"^\s*\d+\s+\*\s+\*\s+\*$", line):
                continue
            
            # Giữ nguyên các dòng hợp lệ
            parsed_data.append(line)

        return "\n".join(parsed_data) if parsed_data else "[red]Không thể thu thập thông tin traceroute[/red]"


    def display_report(self, dig_data, traceroute_data):
        """Hiển thị báo cáo chi tiết trên terminal"""
        # Hiển thị dữ liệu khác
        self.console.print(Panel(f"[bold blue]📡 DNS Info (Dig):[/bold blue]\n{dig_data}", expand=False))
        self.console.print(Panel(f"[bold green]🛤 Traceroute Info:[/bold green]\n{traceroute_data}", expand=False))

    def run(self):
        """Chạy tất cả các công cụ và hiển thị báo cáo"""
        self.console.print("[bold cyan]🔍 Đang thực hiện Enumerate Applications on Webserver...[/bold cyan]\n")

        # Chạy quét fingerprint với thông báo tiến trình
        dig_data = self.DigScan()
        traceroute_data = self.TraceRouteScan()
        # Hiển thị báo cáo
        self.display_report(dig_data, traceroute_data)
        
        
        """Chạy toàn bộ các công cụ để trích xuất dữ liệu và hiển thị kết quả"""
        self.externalTools.dnsdumpster(self.url)