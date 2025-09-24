import subprocess

# 创建Scrapy项目
# subprocess.run("scrapy startproject myproject", shell=True)

# 创建Spider
# subprocess.run("scrapy genspider MyTokenCapSpider xxx.com", shell=True)

# 运行Spider
subprocess.run("scrapy crawl MyTokenCapSpider", shell=True)
