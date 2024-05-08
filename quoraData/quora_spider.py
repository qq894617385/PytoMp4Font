from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

import json


# 创建文件夹
directory = "result"
if not os.path.exists(directory):
    os.makedirs(directory)

# 创建 Chrome WebDriver 对象
driver = webdriver.Chrome()

# 打开目标页面
url = 'https://www.quora.com/topic/Food/top_questions'
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
driver.get(url)

# 等待登录完成和页面加载
input("请登录完成后按 Enter 键继续...")


# 等待页面加载完成
wait = WebDriverWait(driver, 10)  # 设置最长等待时间为10秒
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'qu-dynamicFontSize--regular_title')))


# 获取页面的 HTML 内容
html_content = driver.page_source

# 使用 BeautifulSoup 解析 HTML 内容
soup = BeautifulSoup(html_content, 'html.parser')

# 查找具有指定类的父元素
parent_elements = soup.find_all(class_='dom_annotate_multifeed_topic')

i = 0

targetArray = []

# 遍历每个父元素，查找其中包含指定类的子元素
for parent_element in parent_elements:
    # 查找包含指定类的子元素
    child_elements = parent_element.find_all(class_=['puppeteer_test_link', 'qu-display--block', 'qu-cursor--pointer', 'qu-hover--textDecoration--underline'])
    # 提取每个子元素的文本内容和链接
    for child_element in child_elements:
        text = child_element.get_text(strip=True)
        link = child_element['href'] if 'href' in child_element.attrs else None
        if 'answer' not in text.lower() and link is not None:
            print("Text:", text)
            print("Link:", link)
            targetArray.append({
                'text': text,
                'link': link
            })
            file_path = os.path.join(directory, f"{i}.txt")
            i = i + 1
            with open(file_path, "a") as file:
                file.writelines([f"{text}\n",f'{link}'])


# 将目标数组保存到JSON文件
with open('result.json', 'w') as json_file:
    json.dump(targetArray, json_file)

time.sleep(30)
# 关闭浏览器
driver.quit()
