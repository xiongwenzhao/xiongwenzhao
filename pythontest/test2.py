import time
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError

def connect_to_wechat():
    try:
        app = Application(backend="uia").connect(path="WeChat.exe")
        return app
    except Exception as e:
        print(f"连接微信应用时出错: {e}")
        return None

def find_window(app, title):
    try:
        window = app.window(title=title)
        window.wait('visible', timeout=10)
        window.set_focus()
        return window
    except TimeoutError:
        print(f"未找到标题为 {title} 的窗口")
        return None

def click_button(window, title):
    try:
        button = window.child_window(title=title, control_type="Button")
        button.wait('enabled', timeout=5)
        button.click()
        return True
    except TimeoutError:
        print(f"未找到标题为 {title} 的按钮")
        return False

def add_friend_from_group(main_window):
    if not click_button(main_window, "聊天信息"):
        return

    time.sleep(2)

    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            member_list = main_window.child_window(control_type="List", found_index=0) # 假设群成员列表是第一个 List 控件
            member_list.wait('visible', timeout=5)
            items = member_list.children(control_type="ListItem")
            break  # 如果找到列表，跳出重试循环
        except TimeoutError:
            retry_count += 1
            if retry_count == max_retries:
                print("多次尝试后仍未找到群成员列表")
                return
            print(f"第 {retry_count} 次尝试未找到群成员列表，重试中...")
            time.sleep(1)  # 等待1秒后重试

    for item in items:
        item.click_input()
        time.sleep(1)
        if click_button(main_window, "添加到通讯录"):
            time.sleep(1)
            send_keys("你好，想加个好友")
            time.sleep(1)
            click_button(main_window, "发送")
            time.sleep(2)

def add_friends_from_group():
    app = connect_to_wechat()
    if app is None:
        return

    main_window = find_window(app, "微信")
    if main_window is None:
        return

    print("请手动打开某个微信群聊窗口，等待 5 秒...")
    time.sleep(5)

    add_friend_from_group(main_window)

if __name__ == "__main__":
    add_friends_from_group()
    