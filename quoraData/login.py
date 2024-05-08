from selenium import webdriver

# 创建 Chrome WebDriver 对象
driver = webdriver.Chrome()

# 打开 Quora 登录页面
login_url = "https://www.quora.com/"
driver.get(login_url)

# 在此处手动输入用户名和密码进行登录

# 等待登录完成和页面加载
input("请登录完成后按 Enter 键继续...")

# 获取当前页面的所有 cookie
cookies = driver.get_cookies()

# 将 cookie 保存到文本文件中
with open('cookies.txt', 'w') as f:
    for cookie in cookies:
        f.write(f"{cookie['name']}={cookie['value']}\n")

# 关闭浏览器
driver.quit()
