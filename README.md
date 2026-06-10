# 东振公司：从旧ERP系统导出图纸

使用 Playwright 从已启动的 chrome 实例自动化下载图纸。图纸保存到本地目录，图纸索引保存到本地 SQL Server

## 依赖：
- dotenv
- mssql-python
- playwright

## 文件说明：
- _playwright.py 运行备份
- loop_preparation.py 循环函数
- test_db_interface.py  测试数据库连接
- db_interface_v2.py  数据库连接函数
