from playwright.sync_api import sync_playwright
import os
from db_interface_v2 import get_db_connection

class ImageDownloader:
    def __init__(self, save_folder=r"C:\erp_images", cdp_url="http://localhost:9222"):
        self.save_folder = save_folder
        self.cdp_url = cdp_url
        self._ensure_save_folder_exists()

    def _ensure_save_folder_exists(self):
        os.makedirs(self.save_folder, exist_ok=True)

    def _connect_to_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.connect_over_cdp(self.cdp_url)
        self.context = self.browser.contexts[0]
        self.page = self.context.pages[0]

    def _disconnect_from_browser(self):
        if hasattr(self, "browser"):
            self.browser.close()
        if hasattr(self, "playwright"):
            self.playwright.stop()

    def navigate(self, url):
        self.page.goto(url)
        print(f"页面标题：{self.page.title()}")

    def get_download_links(self):
        links = self.page.get_by_role("link", name="下载").all()
        return links

    def insert_to_database(self, billid, tableid, billstate, filename):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "insert into image_backup (billid, tableid, billstate, image) values (?, ?, ?, ?)",
                (billid, tableid, billstate, filename)
            )
            conn.commit()

    def download_and_save_image(self, link, index, billid, tableid, billstate):
        print(f"正在处理第 {index+1} 个下载...")

        with self.page.expect_download() as download_info:
            link.click()

        download = download_info.value
        filename = download.suggested_filename

        self.insert_to_database(billid, tableid, billstate, filename)

        final_path = os.path.join(self.save_folder, filename)
        download.save_as(final_path)
        print(f"已保存：{final_path}")

    def download_all_images(self, url, billid, tableid, billstate):
        try:
            self._connect_to_browser()
            self.navigate(url)

            download_links = self.get_download_links()

            for idx, link in enumerate(download_links):
                self.download_and_save_image(link, idx, billid, tableid, billstate)

        finally:
            self._disconnect_from_browser()


if __name__ == "__main__":
    downloader = ImageDownloader()

    target_url = "http://dzerp:88/dzerp/aspx/filemanger.aspx?tableid=40&billstate=2&billid=78711"
    billid = 78711
    table_id = 40
    billstate = 2

    downloader.download_all_images(target_url, billid, table_id, billstate)

# 启动 playwright driver 进程
# with sync_playwright() as p:
#     with p.chromium.connect_over_cdp("http://localhost:9222") as browser:
#         context = browser.contexts[0]
#         page = context.pages[0]
#         page.goto("http://dzerp:88/dzerp/aspx/filemanger.aspx?tableid=40&billstate=2&billid=78711")
#         print(page.title())
#
#         download_links = page.get_by_role("link", name="下载").all()
#         print(f"找到 {len(download_links)} 个下载链接")
#
#         for idx, link in enumerate(download_links):
#             print(f"正在处理第 {idx+1} 个下载链接")
#
#             with page.expect_download() as download_info:
#                 link.click()
#
#             download = download_info.value
#             filename = download.suggested_filename
#
#             with get_db_connection() as conn:
#                 cursor = conn.cursor()
#                 cursor.execute("insert into image_backup (billid, tableid, billstate, image) values (?, ?, ?, ?)",
#                                (7971640, 11, 2, filename))
#                 cursor.commit()
#
#             final_path = os.path.join(save_folder, download.suggested_filename)
#
#             download.save_as(final_path)