from playwright.sync_api import sync_playwright
import os
from db_interface_v2 import get_db_connection

save_folder = r"C:\erp_images"

# 启动 playwright driver 进程
p = sync_playwright().start()

# 启动浏览器，返回 Browser 类型对象
browser = p.chromium.connect_over_cdp("http://localhost:9222")

# 创建新页面，返回 Page 类型对象
default_context = browser.contexts[0]
page = default_context.pages[0]
page.goto("http://dzerp:88/dzerp/aspx/filemanger.aspx?tableid=40&billstate=1&billid=78716")
print(page.title()) # 打印网页标题栏

with page.expect_download() as download_info:
    page.get_by_role("link", name="下载").click()

download = download_info.value

filename = download.suggested_filename
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        "insert into image_backup (billid, tableid, billstate, image) values (?, ?, ?, ?)",
        (78716, 40, 1, filename)
    )
    cursor.commit()

final_path = os.path.join(save_folder, download.suggested_filename)

download.save_as(final_path)

# 关闭浏览器
browser.close()
# 关闭 playwright driver 进程
p.stop()