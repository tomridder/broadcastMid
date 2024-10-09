
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

import time
import asyncio
import random
import requests
import sys

TEST_ROOM_IDS = [
    1,0
]


def send_email_via_elasticemail(subject, body):
    api_key = 'BB10CA45CFDA85FA142B957CAAD1CC1B0CE45321EE33FF7F2B8919D08621A4C430C7310385B25BC5F0E8E49034C3161C'
    email_to = 'tomridder716@gmail.com'
    email_from = 'tomchat@tomchat.work'
    sender_name = 'tomchat'

    # API 的请求端点
    url = 'https://api.elasticemail.com/v2/email/send'

    # 构建请求数据
    data = {
        'apikey': api_key,
        'subject': subject,
        'to': email_to,
        'from': email_from,
        'fromName': sender_name,
        'bodyHtml': body,
    }

    # 发送 POST 请求
    response = requests.post(url, data=data)
    result = response.json()
    return result

def check_html_content(driver):
    # 我们会使用一个比较宽泛的 XPath，因为您给的 HTML 内容结构比较复杂
    xpath = "//div[contains(text(), '直播已结束')]"
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # 如果找到了这部分内容，调用 console.debug
        send_email_via_elasticemail('done','done');
        sys.exit(0)
        time.sleep(300000000000000000000000)
        print("特定HTML内容出现，已调用 console.debug(1)")
    except:
        # 如果没有找到这部分内容，代码将抛出异常并被捕捉到，可以什么都不做
        pass


async def switch_windows(driver):
    while True:
        driver.switch_to.window(driver.window_handles[TEST_ROOM_IDS[0]])
        await asyncio.sleep(0.5)
        driver.switch_to.window(driver.window_handles[TEST_ROOM_IDS[1]])
        await asyncio.sleep(20)

def extract_and_print_new_danmu(driver, previously_seen):
    # print('into exact')

    # 检查 HTML 内容
    # check_html_content(driver)

    # 等待直到弹幕元素能被定位，确保页面已经加载完成
    WebDriverWait(driver, 100000).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".danmu-line .msg-content"))
    )

    # 可能需根据实际的弹幕结构进行微调选择器
    danmu_elements = driver.find_elements(By.CSS_SELECTOR, ".danmu-line .msg-content")

    # 遍历所有弹幕元素，打印新出现的
    for danmu in danmu_elements:
        # for danmu in danmu_elements:
        try:
            danmu_text = danmu.text

            if danmu_text not in previously_seen:
                driver.switch_to.window(driver.window_handles[TEST_ROOM_IDS[0]])

                print('3');
                # 等待输入框加载完成
                input_element = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "home_chat-input__3tOh5"))
                )

                # 清空输入框
                input_element.clear()

                # 填入信息
                input_element.send_keys(danmu_text)

                time.sleep(0.5)

                button = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//div[text()="发送"]'))
                )

                button.click()
                print(danmu_text)
                previously_seen.add(danmu_text)


        except Exception as e:
            # 打印异常信息
            print(f"An error occurred while processing the danmu: {e}")
            #send_email_via_elasticemail("ok", "ok");
            # 根据需要进行其他异常处理操作
            continue  # 跳过当前弹幕，继续处理后续元素


def wait_for_new_danmu(driver):
    previous_danmu_set = set()
    while True:
        current_time = datetime.now()
        current_seconds = current_time.second
        # print('wait_for_new_danmu'  , current_seconds)

        current_minute = time.localtime().tm_min

        driver.switch_to.window(driver.window_handles[TEST_ROOM_IDS[1]])

        extract_and_print_new_danmu(driver, previous_danmu_set)

        # 等待一定时间后再次检查新弹幕
        #
        time.sleep(1)  # 例如，每2秒检查一次新弹幕


def send_message_every_minute(driver):
    print('send_message_every_minute')
    number = 0;

    str_list = ['写一段冒泡排序', '给耐克的鸭舌帽，写一篇营销文，100字', '给一段马斯克的名言，并且翻译成英文', '怎么才能充实的过好每一天，给2个建议', '什么是山楂',
                '2131+21312等于几']

    # 找到你的输入框元素
    try:
        # 找到你的输入框元素
        input_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.n-input__input-el'))
        )
        # 接下来的动作...

    except TimeoutException:
        # 处理超时异常
        subject = "Selenium Timeout Exception"
        body_html = "<p>An exception occurred: Selenium Timeout Exception.</p >"
        send_email_result = send_email_via_elasticemail(subject, body_html)
        #send_email_via_elasticemail("ok", "ok");
        print("Email sent! Response:", send_email_result)

    number = random.randint(0, 4)

    print('w15');

    # 填写你的输入框
    input_elem.send_keys(str_list[number])

    #time.sleep(0.1)

    # 找到并点击按钮
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button/span[contains(text(), "发送 ")]'))
    )
    button.click()


async def main(driver):
    print('1')

    # 在此添加异步的网页打开操作
    # await driver.get(url)

    print('2')

    # 切换到指定的窗口
    driver.switch_to.window(driver.window_handles[TEST_ROOM_IDS[1]])

    print('3' + driver.window_handles[0])

    print('5')

    asyncio.create_task(switch_windows(driver))

    # 检查新弹幕（需要确保内部的操作是异步的或是在executor中运行）
    await asyncio.to_thread(wait_for_new_danmu, driver)

    print('6')

    # 记得最后要关闭浏览器
    # driver.quit()


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8888")

print('1');

# 连接到已经打开的Chrome浏览器实例
driver = webdriver.Chrome(options=chrome_options)
asyncio.run(main(driver))
