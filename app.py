from utils.FingerPrintServer import FingerPrintServer
from utils.ReviewWebserverMetafiles import MetaFileReview

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

