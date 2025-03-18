import requests
import json
import signal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

class MetaFileReview:
    def __init__(self, url, wordlist_path="/usr/share/seclists/Discovery/Web-Content/common.txt"):
        self.url = url.rstrip("/")
        self.console = Console()
        self.sensitive_files = self.load_wordlist(wordlist_path)
        self.results = []
        self.stop_scan = False

        # Bắt tín hiệu Ctrl+C để dừng và lưu kết quả
        signal.signal(signal.SIGINT, self.handle_exit)

    def load_wordlist(self, path):
        """Đọc danh sách file từ SecLists"""
        try:
            with open(path, "r") as file:
                return [line.strip() for line in file if line.strip() and not line.startswith("#")]
        except FileNotFoundError:
            self.console.print(f"[bold red]❌ Không tìm thấy file wordlist: {path}[/bold red]")
            return []

    def check_file(self, file_path):
        """Kiểm tra xem file có tồn tại trên server không"""
        if self.stop_scan:
            return None  # Nếu bị dừng, không quét tiếp

        full_url = f"{self.url}/{file_path}"
        try:
            response = requests.get(full_url, timeout=5)
            status_code = response.status_code
            if status_code in [200, 403]:  # Chỉ quan tâm đến 200 (tồn tại) & 403 (bị chặn)
                return {"file": file_path, "status": status_code, "url": full_url}
        except requests.exceptions.RequestException:
            return None
        return None

    def handle_exit(self, signum, frame):
        """Xử lý khi nhấn Ctrl+C"""
        self.console.print("\n[bold red]⚠ Chương trình bị dừng! Đang lưu kết quả...[/bold red]")
        self.stop_scan = True  # Đánh dấu để dừng quét
        self.save_results()  # Lưu kết quả trước khi thoát
        exit(0)

    def save_results(self):
        """Lưu kết quả ra file JSON"""
        if self.results:
            with open("results.json", "w") as f:
                json.dump(self.results, f, indent=2)
            self.console.print(f"[bold green]✅ Đã lưu {len(self.results)} kết quả vào [cyan]results.json[/cyan]![/bold green]")
        else:
            self.console.print("[bold yellow]⚠ Không có dữ liệu để lưu![/bold yellow]")

    def scan(self):
        """Quét danh sách các tệp nhạy cảm từ SecLists và hiển thị tiến trình"""
        total_files = len(self.sensitive_files)
        self.console.print(f"[bold cyan]🔍 Đang quét Webserver Metafiles từ SecLists ({total_files} mục)...[/bold cyan]\n")
        try:
            found_files = 0
            with Progress() as progress:
                task = progress.add_task("[cyan]Đang quét...", total=total_files)

                for i, file in enumerate(self.sensitive_files, start=1):
                    if self.stop_scan:  # Nếu nhận tín hiệu dừng thì thoát khỏi vòng lặp
                        break

                    result = self.check_file(file)
                    if result:
                        self.results.append(result)
                        found_files += 1
                        self.print_found_file(result)  # In kết quả ngay khi tìm thấy

                    progress.update(task, advance=1, description=f"[cyan]{i}/{total_files} - Phát hiện: {found_files}[/cyan]")
            self.console.print(f"\n[bold green]✅ Quét hoàn tất! Đã kiểm tra {total_files} file, phát hiện {found_files} file nhạy cảm.[/bold green]\n")
            self.save_results()  # Lưu kết quả sau khi quét xong
        except KeyboardInterrupt as e:
            self.console.print("\n[bold red]⚠ Chương trình bị dừng! Đang lưu kết quả...[/bold red]")
            self.console.print(f"\n[bold green]✅ Đã kiểm tra {total_files} file, phát hiện {found_files} file nhạy cảm.[/bold green]\n")
            self.save_results()
    def print_found_file(self, result):
        """Hiển thị kết quả ngay khi tìm thấy file nhạy cảm"""
        status_text = "🟢 200 OK" if result["status"] == 200 else "🔴 403 Forbidden"
        self.console.print(f"[bold yellow]📂 Phát hiện:[/bold yellow] {result['file']} - {status_text} - [cyan]{result['url']}[/cyan]")

