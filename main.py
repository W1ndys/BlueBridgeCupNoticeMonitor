import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import os
from datetime import datetime


class LanQiaoMonitor:
    def __init__(
        self, url, dingtalk_token, dingtalk_secret, data_file="lanqiao_data.json"
    ):
        """
        初始化监控器
        :param url: 要监控的API URL
        :param dingtalk_token: 钉钉机器人的令牌
        :param dingtalk_secret: 钉钉机器人的密钥
        :param data_file: 存储历史数据的文件
        """
        self.url = url
        self.dingtalk_token = dingtalk_token
        self.dingtalk_secret = dingtalk_secret

        # 获取脚本所在的目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 将数据文件路径设为脚本目录下的文件
        self.data_file = os.path.join(script_dir, data_file)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def print_welcome(self):
        print("--------------------------------")
        print("蓝桥杯通知监控系统")
        print("By W1ndys")
        print("开源地址：https://github.com/W1ndys/BlueBridgeCupNoticeMonitor")
        print("--------------------------------")

    def fetch_data(self):
        """获取API的JSON数据"""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取数据失败: {e}")
            return None

    def load_saved_data(self):
        """加载保存的历史数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载历史数据失败: {e}")
                return None
        return None

    def save_data(self, data):
        """保存数据到文件"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {self.data_file}")
        except Exception as e:
            print(f"保存数据失败: {e}")

    def find_new_content(self, old_data, new_data):
        """
        比较新旧数据，找出新内容
        :return: 新通知列表
        """
        if not old_data:
            # 如果没有旧数据，那么所有内容都是新的
            return new_data.get("datalist", [])

        old_nnids = {item["nnid"] for item in old_data.get("datalist", [])}
        new_items = [
            item
            for item in new_data.get("datalist", [])
            if item["nnid"] not in old_nnids
        ]

        return new_items

    def send_dingtalk_notification(self, new_items):
        """
        发送钉钉通知
        :param new_items: 新通知列表
        """
        if not new_items:
            print("没有新通知")
            return

        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.dingtalk_secret}"
        hmac_code = hmac.new(
            self.dingtalk_secret.encode(),
            string_to_sign.encode(),
            digestmod=hashlib.sha256,
        ).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code).decode())

        url = f"https://oapi.dingtalk.com/robot/send?access_token={self.dingtalk_token}&timestamp={timestamp}&sign={sign}"

        for item in new_items:
            title = item["title"]
            publish_time = item["publishTime"].split("T")[0]
            synopsis = item.get("synopsis", "无摘要")

            message = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "蓝桥杯通知更新",
                    "text": f"## 蓝桥杯大赛通知更新\n\n"
                    f"### {title}\n\n"
                    f"**发布时间**: {publish_time}\n\n"
                    f"**内容摘要**: {synopsis}\n\n"
                    f"[查看详情](https://dasai.lanqiao.cn/notices/{item['nnid']}/)",
                },
            }

            try:
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(message),
                )
                result = response.json()
                if result.get("errcode") == 0:
                    print(f"通知 '{title}' 发送成功")
                else:
                    print(f"通知发送失败: {result}")
            except Exception as e:
                print(f"发送通知时出错: {e}")

    def test_dingtalk_notification(self):
        """
        测试钉钉通知功能
        """
        print("开始测试钉钉通知...")

        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.dingtalk_secret}"
        hmac_code = hmac.new(
            self.dingtalk_secret.encode(),
            string_to_sign.encode(),
            digestmod=hashlib.sha256,
        ).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code).decode())

        url = f"https://oapi.dingtalk.com/robot/send?access_token={self.dingtalk_token}&timestamp={timestamp}&sign={sign}"

        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": "蓝桥杯监控测试",
                "text": f"## 蓝桥杯监控系统测试\n\n"
                f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"**测试内容**: 这是一条测试消息，用于验证钉钉通知功能是否正常工作。\n\n"
                f"[查看监控页面]({self.url})",
            },
        }

        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(message),
            )
            result = response.json()
            if result.get("errcode") == 0:
                print("测试通知发送成功")
            else:
                print(f"测试通知发送失败: {result}")
            return result.get("errcode") == 0
        except Exception as e:
            print(f"发送测试通知时出错: {e}")
            return False

    def run(self):
        """运行监控器"""
        print(f"蓝桥杯通知监控启动: {datetime.now()}")

        # 获取最新数据
        new_data = self.fetch_data()
        if not new_data:
            print("无法获取新数据，退出")
            return

        # 加载保存的历史数据
        old_data = self.load_saved_data()

        # 找出新内容
        new_items = self.find_new_content(old_data, new_data)

        # 如果有新内容，发送通知
        if new_items:
            print(f"发现 {len(new_items)} 条新通知")
            self.send_dingtalk_notification(new_items)
        else:
            print("没有发现新通知")

        # 保存最新数据
        self.save_data(new_data)

        print(f"蓝桥杯通知监控完成: {datetime.now()}")


if __name__ == "__main__":
    # 配置参数
    url = "https://www.guoxinlanqiao.com/api/news/find?status=1&project=dasai&progid=20&pageno=1&pagesize=10"
    dingtalk_token = "xxx"  # 替换为实际的钉钉机器人令牌
    dingtalk_secret = "xxx"  # 替换为实际的钉钉机器人密钥

    # 创建监控器实例
    monitor = LanQiaoMonitor(url, dingtalk_token, dingtalk_secret)
    # 打印欢迎信息
    monitor.print_welcome()
    # 运行监控器
    monitor.run()
