from playwright.sync_api import sync_playwright
import threading


share_url = "https://www.icloud.com.cn/iclouddrive/0c4AUs7KM6e_1rIks61e_rGiw"


found_url = None
event = threading.Event()


with sync_playwright() as p:

    browser = p.chromium.launch(
    headless=True,
    args=[
        "--disable-blink-features=AutomationControlled"
    ]
)


    page = browser.new_page()



    # =========================
    # 捕获请求（最快）
    # =========================
    def handle_request(request):

        global found_url

        url = request.url


        if (
            "icloud-content" in url
            or "cvws" in url
        ):

            if found_url is None:

                found_url = url

                print("\n====================")
                print("找到直链(request):")
                print(url)
                print("====================\n")

                event.set()



        if "downloadFiles" in url:

            print("\n发现下载接口:")
            print(url)




    # =========================
    # 捕获响应（备用）
    # =========================
    def handle_response(response):

        global found_url

        url = response.url


        if (
            "icloud-content" in url
            or "cvws" in url
        ):

            if found_url is None:

                found_url = url

                print("\n====================")
                print("找到直链(response):")
                print(url)
                print("====================\n")

                event.set()



    page.on(
        "request",
        handle_request
    )


    page.on(
        "response",
        handle_response
    )



    print("打开 iCloud...")


    page.goto(
        share_url,
        wait_until="domcontentloaded",
        timeout=30000
    )



    print("等待下载按钮...")



    try:

        # 下载副本按钮
        download_btn = page.locator(
            "ui-button.icloud-mouse.secondary"
        ).first


        download_btn.wait_for(
            state="visible",
            timeout=10000
        )


        print("找到下载按钮")


        download_btn.click(
            force=True
        )


        print("点击下载成功")



    except Exception as e:

        print("点击失败:")
        print(e)

        browser.close()
        exit()



    print("等待直链...")



    # 等待直链出现
    if event.wait(timeout=15):

        print("解析完成")


    else:

        print("15秒内未获取直链")



    browser.close()


    print("程序结束")