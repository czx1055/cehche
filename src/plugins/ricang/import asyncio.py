import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.jx3box.com/index/')
    await page.waitFor(1 * 1000) # 等待10秒看看验证码长什么样
    yazhengma = await page.waitForSelector('#app > div > div.m-primary > div.m-content > div > div.m-right > div.m-daily-activity.m-sideblock') # 通过css selector定位验证码元素
    await yazhengma.screenshot({'path': 'yazhengma.png'}) # 注意这里用的是ele.screenshot方法与教程1 page.screenshot是不同的
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())