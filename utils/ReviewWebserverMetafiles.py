import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

class MetaFileReview:
    def __init__(self, url, wordlist_path="/usr/share/seclists/Discovery/Web-Content/common.txt"):
        self.url = url.rstrip("/")
        self.console = Console()
        self.sensitive_files = self.load_wordlist(wordlist_path)[:20]
        self.results = []

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
        full_url = f"{self.url}/{file_path}"
        try:
            response = requests.get(full_url, timeout=5)
            status_code = response.status_code
            if status_code in [200, 403]:  # Chỉ quan tâm đến 200 (tồn tại) & 403 (bị chặn)
                return {"file": file_path, "status": status_code, "url": full_url}
        except requests.exceptions.RequestException:
            return None
        return None

    def scan(self):
        """Quét danh sách các tệp nhạy cảm từ SecLists và hiển thị tiến trình"""
        total_files = len(self.sensitive_files)
        self.console.print(f"[bold cyan]🔍 Đang quét Webserver Metafiles từ SecLists ({total_files} mục)...[/bold cyan]\n")

        found_files = 0
        with Progress() as progress:
            task = progress.add_task("[cyan]Đang quét...", total=total_files)

            for i, file in enumerate(self.sensitive_files, start=1):
                result = self.check_file(file)
                if result:
                    self.results.append(result)
                    found_files += 1

                progress.update(task, advance=1, description=f"[cyan]Đã quét: {i}/{total_files} - Phát hiện: {found_files}[/cyan]")

        self.console.print(f"\n[bold green]✅ Quét hoàn tất! Đã kiểm tra {total_files} file, phát hiện {found_files} file nhạy cảm.[/bold green]\n")
        self.display_results()

    def display_results(self):
        """Hiển thị kết quả quét"""
        if not self.results:
            self.console.print("[bold green]✔ Không phát hiện file rò rỉ thông tin![/bold green]")
            return

        table = Table(title="📄 Kết quả quét Webserver Metafiles", show_lines=True)
        table.add_column("Tệp", style="bold yellow", justify="left")
        table.add_column("Trạng thái", style="bold cyan", justify="center")
        table.add_column("URL", style="bold green")

        for result in self.results:
            status_text = "🟢 200 OK" if result["status"] == 200 else "🔴 403 Forbidden"
            table.add_row(result["file"], status_text, result["url"])

        self.console.print(table)


