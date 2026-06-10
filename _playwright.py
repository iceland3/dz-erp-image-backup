from playwright.sync_api import sync_playwright
import os
from db_interface_v2 import get_db_connection

save_folder = r"C:\erp_images"

# 启动 playwright driver 进程
with sync_playwright() as p:
    with p.chromium.connect_over_cdp("http://localhost:9222") as browser:
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto("http://dzerp:88/dzerp/aspx/filemanger.aspx?tableid=40&billstate=2&billid=78711")
        print(page.title())

        with page.expect_download() as download_info:
            page.get_by_role("link", name="下载").click()

        download = download_info.value
        filename = download.suggested_filename

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("insert into image_backup (billid, tableid, billstate, image) values (?, ?, ?, ?)",
                           (7971640, 11, 2, filename))
            cursor.commit()

        final_path = os.path.join(save_folder, download.suggested_filename)

        download.save_as(final_path)