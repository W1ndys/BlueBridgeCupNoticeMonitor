# 🏆 蓝桥杯通知监控系统

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/lanqiao-notifier?style=for-the-badge)](https://github.com/yourusername/lanqiao-notifier/stargazers)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)

> 实时监控蓝桥杯大赛官方通知的自动化解决方案

![Demo Screenshot](https://github.com/user-attachments/assets/8a0ee746-146b-44b5-9616-f26528b50675)

## ✨ 核心功能

- 🕵️‍♂️ **智能监控** - 定时扫描蓝桥杯官网最新通知
- 🔔 **即时推送** - 通过钉钉机器人实时提醒
- 💾 **状态记忆** - 本地存储已通知记录，避免重复提醒
- 🧪 **测试模式** - 支持消息推送测试验证
- 🏗 **优雅架构** - 采用面向对象设计，模块化清晰

## 🛠 快速开始

### 环境准备

```bash
# 克隆仓库
git clone https://github.com/yourusername/lanqiao-notifier.git

# 安装依赖
pip install -r requirements.txt
```

### 配置指南

在 `config.py` 中配置以下参数：

```python
# 蓝桥杯API接口
MONITOR_URL = "https://www.guoxinlanqiao.com/api/news/find?status=1&project=dasai&progid=20&pageno=1&pagesize=10"

# 钉钉机器人配置
DINGTALK_TOKEN = "your_webhook_token"  # 替换为实际token
DINGTALK_SECRET = "your_secret_key"   # 替换为加签密钥
```

## 🚀 部署运行

推荐使用 Linux crontab 设置定时任务：

```bash
# 编辑crontab
crontab -e

# 添加以下内容（示例：每30分钟检查一次）
*/30 * * * * /usr/bin/python3 /path/to/main.py >> /var/log/lanqiao_monitor.log 2>&1
```

## 📌 注意事项

1. 确保服务器可以访问蓝桥杯官网
2. 钉钉机器人需开启加签验证功能
3. 首次运行会发送所有历史通知（可通过清空本地存储文件重置）

## 🤝 参与贡献

欢迎提交 Issue 或 PR！请遵循以下流程：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

## 📄 开源协议

本项目采用 [GPL-3.0](LICENSE)

---

⭐ **如果这个项目对你有帮助，请点个 Star 支持一下！**
