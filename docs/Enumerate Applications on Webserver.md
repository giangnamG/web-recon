Enumerate Applications on Webserver (Dò tìm các ứng dụng trên Webserver) là một công việc quan trọng trong quá trình kiểm tra bảo mật và đánh giá ứng dụng web. Nó nhằm mục đích thu thập thông tin về các ứng dụng đang chạy trên webserver, xác định các dịch vụ, ứng dụng, hoặc nền tảng mà webserver sử dụng. Dưới đây là các đầu mục công việc chính trong quá trình này:

1. Dò tìm cổng mở và dịch vụ (Port Scanning & Service Enumeration)
   Nmap: Sử dụng công cụ Nmap để quét cổng và tìm các dịch vụ đang chạy trên các cổng này.
   HTTP server: Xác định các dịch vụ web đang chạy, ví dụ như Apache, Nginx, IIS, hoặc các dịch vụ HTTP khác.
   Phiên bản dịch vụ: Tìm kiếm thông tin về phiên bản của các dịch vụ web và các ứng dụng để xác định các lỗi bảo mật tiềm ẩn.
2. Phân tích thông tin từ tiêu đề HTTP (HTTP Header Analysis)
   Kiểm tra tiêu đề HTTP để phát hiện thông tin về công nghệ sử dụng trên server.
   Các tiêu đề như Server, X-Powered-By, Set-Cookie có thể tiết lộ thông tin về hệ điều hành, nền tảng, hoặc công nghệ phát triển của ứng dụng (ví dụ: PHP, ASP.NET, Node.js).
   WhatWeb: Là công cụ hữu ích để phân tích công nghệ web từ tiêu đề HTTP và nội dung của trang web.
3. Dò tìm thư mục và endpoint (Directory and Endpoint Enumeration)
   Brute-force directories: Sử dụng các công cụ như Gobuster, Dirsearch, và FFUF để brute-force tìm các thư mục, endpoint tiềm năng của ứng dụng web, chẳng hạn như /admin, /login, /wp-admin, /cgi-bin, v.v.
   Các công cụ này sẽ thử với một danh sách từ điển (wordlist) các thư mục phổ biến để xem liệu có các ứng dụng hoặc tính năng nào ẩn chứa trong đó.
4. Thu thập thông tin WHOIS (WHOIS Lookup)
   Whois: Thực hiện tra cứu WHOIS để thu thập thông tin về domain của web server như chủ sở hữu, người quản lý, DNS, và các thông tin liên quan đến địa chỉ IP của server.
5. Kiểm tra thông tin DNS (DNS Enumeration)
   Dig: Sử dụng công cụ dig để thu thập thông tin DNS về domain, bao gồm các bản ghi A, MX, TXT, CNAME, và SOA. Điều này giúp bạn biết thêm về các dịch vụ DNS mà server đang sử dụng.
   Kiểm tra DNS giúp phát hiện các bản ghi không công khai hoặc các thông tin có thể cung cấp cái nhìn sâu sắc về cấu hình của webserver.
6. Truy vết đường đi của gói tin (Traceroute)
   Traceroute: Sử dụng lệnh traceroute để xem các bước đi của gói tin từ máy của bạn đến webserver. Điều này có thể giúp phát hiện các tầng của mạng và các thiết bị trung gian.
   Phân tích thông tin traceroute có thể giúp phát hiện cấu trúc mạng và xác định các điểm yếu trong hạ tầng mạng.
7. Phân tích các ứng dụng CMS (Content Management System)
   Nếu ứng dụng sử dụng CMS (chẳng hạn như WordPress, Joomla, Drupal), các công cụ như WhatWeb, Wappalyzer hoặc BuiltWith có thể giúp nhận diện các nền tảng CMS này dựa trên các dấu hiệu trong tiêu đề HTTP hoặc mã nguồn của trang web.
   Phát hiện và phân tích các CMS có thể giúp xác định các ứng dụng dễ bị tấn công với các lỗ hổng đã biết.
8. Phát hiện các ứng dụng JavaScript và các thư viện phía client (JavaScript Frameworks & Libraries)
   Các công cụ như Wappalyzer hoặc WhatWeb có thể phát hiện các thư viện hoặc framework JavaScript phía client (VD: React, Angular, Vue.js, v.v.).
   Việc phân tích các ứng dụng JavaScript có thể giúp xác định các điểm yếu trong ứng dụng web phía client.
9. Xác định ứng dụng và nền tảng (Application and Platform Identification)
   WhatWeb: Dùng để phát hiện công nghệ web (ví dụ: nền tảng, framework, phần mềm server).
   Các công cụ này sẽ phân tích các dấu hiệu trên HTTP response và mã nguồn trang web để xác định chính xác các công nghệ đang chạy trên webserver.
10. Kiểm tra và quét bảo mật (Security Scanning)
    Nikto: Công cụ quét bảo mật web để phát hiện các vấn đề bảo mật cơ bản, chẳng hạn như cấu hình sai, các tệp và thư mục nhạy cảm.
    Kiểm tra các bản vá và các vấn đề bảo mật như SQL injection, XSS, hoặc các lỗi phổ biến khác.
    Tổng hợp kết quả và tạo báo cáo (Reporting)
    Sau khi thu thập đủ thông tin từ các công cụ trên, việc tạo báo cáo chi tiết về các dịch vụ, ứng dụng, công nghệ và vấn đề bảo mật là rất quan trọng.
    Các kết quả có thể được trình bày dưới dạng bảng, văn bản, hoặc thông qua các công cụ như rich (để hiển thị báo cáo đẹp mắt trên terminal).
    Tóm tắt các công việc chính trong việc Enumerate Applications on Webserver:
    Quét cổng và dịch vụ (Port Scanning & Service Enumeration).
    Phân tích HTTP headers.
    Brute-force thư mục và endpoint.
    WHOIS Lookup.
    DNS Enumeration.
    Traceroute.
    Phân tích CMS và nền tảng.
    Phân tích JavaScript và các thư viện client.
    Quét bảo mật và phát hiện lỗ hổng.
    Tạo báo cáo kết quả chi tiết.
