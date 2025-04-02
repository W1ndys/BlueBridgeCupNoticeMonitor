# 蓝桥杯通知监控系统

## 项目简介

这是一个用于监控蓝桥杯大赛通知的自动化工具。该工具会定期检查蓝桥杯官方网站的通知，当发现新通知时，会通过钉钉机器人发送提醒消息。

## 功能特点

- 自动获取蓝桥杯大赛最新通知
- 本地存储历史数据，避免重复通知
- 使用钉钉机器人推送新通知（支持加签验证）
- 提供通知测试功能，确保钉钉配置正确
- 面向对象设计，代码结构清晰

## 环境要求

- Python 3.8+
- 需要安装的依赖包：requests

## 安装方法

1. 克隆或下载本项目
2. 安装依赖包：
   ```bash
   pip install requests
   ```

## 配置说明

在使用前，需要在 `main.py` 中修改以下配置：

```python
url = "https://www.guoxinlanqiao.com/api/news/find?status=1&project=dasai&progid=20&pageno=1&pagesize=10"
dingtalk_token = "xxx"  # 替换为实际的钉钉机器人令牌
dingtalk_secret = "xxx"  # 替换为实际的钉钉机器人密钥
```

## 使用方法

使用 linux 的 crontab 定时任务，定时执行即可
