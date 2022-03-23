import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest
from PIL import Image
import pytesseract

def ocr_img(): # 验证码识别
    pic = Image.open("img/code_img.png")
    pic_str = pytesseract.image_to_string(pic)

    # 处理字符串
    resp_str = pic_str.split()
    resp_str = "".join(resp_str)

    return resp_str

def isCorrect(): # 判断验证码是否正确
    true = web.find_element_by_id('r_code')
    if true.is_displayed() == True:
        return True
    else:
        return False

def FillCaptcha(): # 填入验证码
    web.find_element_by_id('w_code').clear()
    web.find_element_by_id('w_code').send_keys(ocr_img())

def CompleteInformation(): # 填入基本信息

    web.maximize_window()  # 将浏览器最大化

    #打开浏览器时执行规避检测的js代码
    with open('./stealth.min.js') as f:
            js = f.read()
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": js
            })

    web.get("http://gov.12321.cn/web")

    web.find_element_by_name('url').send_keys('http://cloud.hacosky.com/cart?fid=1')

    web.find_element_by_class_name('bllxCon').click()

    web.find_element_by_id('sms_content').send_keys('打开之后自动跳转到了黄色网站，严重影响了我的心智，不能忘怀，请国家严惩！！！\n 图片链接：https://s6.jpg.cm/2022/03/22/L3MX85.jpg')

def getcode_img(): # 获得验证码图片

    web.save_screenshot("img/scr_img.png") # 截图

    code = web.find_element_by_id('code')

    x0 = code.location["x"]  # 获得位置
    y0 = code.location["y"]
    x1 = code.size["width"] + x0
    y1 = code.size["height"] + y0

    img = Image.open("img/scr_img.png")

    image = img.crop((x0,y0,x1,y1))  # 左、上、右、下

    image.save("img/code_img.png")  # 将验证码图片保存为code_img.png

def pull():
    if isCorrect():
        web.find_element_by_id('sub_jb') # 点击提交按钮
    else:
        web.find_element_by_id('code').click() # 点击图片 更换验证码
        getcode_img()
        ocr_img()
        FillCaptcha()
        pull()

if __name__ == '__main__':
    web = webdriver.Chrome()    # Chrome浏览器

    CompleteInformation()

    time.sleep(1)

    getcode_img()

    time.sleep(1)

    ocr_img()

    time.sleep(1)

    FillCaptcha()

    time.sleep(1)

    pull()

    print("已提交")