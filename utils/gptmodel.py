from dotenv import load_dotenv
import openai
import json
import os

# Tải API Key từ biến môi trường
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Đặt API Key của bạn
openai.api_key = api_key

# Định nghĩa dữ liệu đầu vào (output từ công cụ)
output = {
    "tool_name": "Example Tool",
    "date": "2025-03-18",
    "results": [
        {"id": 1, "test": "Test A", "status": "Passed", "time": "12:30"},
        {"id": 2, "test": "Test B", "status": "Failed", "time": "12:45"},
        {"id": 3, "test": "Test C", "status": "Passed", "time": "13:00"}
    ]
}

# Yêu cầu API tạo báo cáo HTML từ dữ liệu đầu vào
prompt = f"""
Tạo báo cáo HTML cho công cụ {output['tool_name']} vào ngày {output['date']} với các kết quả sau:
{json.dumps(output)}
Báo cáo cần bao gồm một bảng với các cột: ID, Test, Status và Time. Màu sắc cho trạng thái Passed là xanh lá và cho trạng thái Failed là đỏ.
"""

# Gửi yêu cầu đến API ChatGPT
response = openai.Completion.create(
  model="gpt-3.5-turbo",
  prompt=prompt,
  temperature=0.5,
  max_tokens=1024,
  n=1
)

# Lấy kết quả trả về và in ra HTML
html_report = response['choices'][0]['text'].strip()

# Lưu báo cáo HTML vào file
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_report)

print("Báo cáo đã được tạo thành công và lưu vào 'report.html'.")
