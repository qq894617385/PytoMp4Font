from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import json

jsonData = []

# 从JSON文件中读取数据
with open('result.json', 'r') as json_file:
    data = json.load(json_file)

# 使用读取的数据
print(data)

# 创建文件夹
directory = "result"
if not os.path.exists(directory):
    os.makedirs(directory)

# 创建 Chrome WebDriver 对象
driver = webdriver.Chrome()

# 打开目标页面
url = 'https://www.quora.com/topic/Health/top_questions'
driver.get(url)

# 从文件中读取保存的 cookie
with open('cookies.txt', 'r') as f:
    cookies = f.read().splitlines()

# 将 cookie 添加到 WebDriver 中
for cookie in cookies:
    name, value = cookie.split('=', 1)
    driver.add_cookie({'name': name, 'value': value})

# 刷新页面以应用 cookie
driver.refresh()


# 等待登录完成和页面加载
# input("请登录完成后按 Enter 键继续...")

# 这里循环完成信息采集


# for index, element in enumerate(jsonData):
#     print(f"Index: {index}, Element: {element}")
#     if index == 0:
#         print(element['text'])
#         driver.get(element['link'])

driver.get('https://www.quora.com/Is-spinach-better-for-you-cooked-or-raw')

# 定义一个变量来存储上一次滚动条的位置
last_height = driver.execute_script("return document.body.scrollHeight")

# 循环滚动页面直到页面底部加载完毕
while True:
    # 滚动到页面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 等待一段时间以确保页面加载完成
    driver.implicitly_wait(5)

    # 获取当前滚动条位置
    new_height = driver.execute_script("return document.body.scrollHeight")

    # 如果滚动条位置没有变化，说明页面已经到达底部
    if new_height == last_height:
        break

    # 更新滚动条位置
    last_height = new_height

elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//span[contains(text(), "(more)")]'))
)

# 对每个元素执行点击操作
for element in elements:
    driver.execute_script("arguments[0].click();", element)

time.sleep(30)



# 关闭浏览器
driver.quit()
