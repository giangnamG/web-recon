import subprocess, time, os
from utils.FingerPrintServer import FingerPrintServer
from utils.ReviewWebserverMetafiles import MetaFileReview
from utils.EnumWebApp import EnumerateWebServer

try:
    # 🚀 Chạy quét Webserver Metafiles với SecLists
    meta_review = MetaFileReview("https://nic.gov.vn")
    meta_review.scan()
except KeyboardInterrupt as e:
    print("Đã dừng quét Webserver Metafiles!")
    pass

# Chạy quét trên domain cụ thể
scanner = FingerPrintServer("nic.gov.vn", silent=True)
scanner.run()

scanner = EnumerateWebServer("https://nic.gov.vn", silent=True)
scanner.run()