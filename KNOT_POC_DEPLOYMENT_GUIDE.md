# 元来如此公司 MCP Server - Knot 平台 POC 部署指南

## 📋 概述

本文档提供在 Knot 平台上部署"元来如此公司智能 Agent 集群"的完整步骤和所需填写的内容。

---

## 🚀 部署流程

### **第一步：在 DevCloud 部署 MCP Server**

#### 1.1 登录 DevCloud
访问：http://devcloud.woa.com

#### 1.2 创建虚拟机（如果还没有）
- 选择 Linux 系统（推荐 Ubuntu 20.04）
- 配置：2核4G 即可
- 确保可以访问外网

#### 1.3 上传代码
```bash
# 方式 A：从 GitHub 克隆
git clone https://github.com/XiaoyuanNO1/yuanlai-mcp-server.git
cd yuanlai-mcp-server

# 方式 B：手动上传文件
# 上传以下文件到服务器：
# - yuanlai_mcp_server_knot.py
# - requirements.txt
# - start_server.sh
```

#### 1.4 启动服务
```bash
# 方式 A：使用启动脚本（推荐）
bash start_server.sh

# 方式 B：手动启动
pip3 install -r requirements.txt
python3 yuanlai_mcp_server_knot.py 8080
```

#### 1.5 验证服务
```bash
# 健康检查
curl http://localhost:8080/health

# 应该返回：
# {"status": "healthy", "service": "yuanlai-company-agent", "timestamp": "..."}
```

#### 1.6 获取服务器 IP
```bash
# 查看内网 IP
hostname -I
```

**记录这个 IP 地址！**（例如：`10.x.x.x`）

---

### **第二步：在 Knot 平台创建 MCP**

#### 2.1 访问 Knot 平台
访问：https://knot.woa.com

#### 2.2 进入 MCP 管理
点击左侧菜单 "MCP 管理" → "新建 MCP"

#### 2.3 填写 MCP 基本信息

**需要填写的内容：**

| 字段 | 填写内容 |
|------|---------|
| **MCP 名称** | `元来如此公司智能Agent集群` |
| **Server Name** | `yuanlai-company-agent` |
| **描述** | `支持财务、人力资源、研发三个子 Agent 的智能调度` |
| **MCP 类型** | 选择 `Streamable HTTP` |
| **URL 地址** | `http://你的DevCloud服务器IP:8080/mcp` <br>（例如：`http://10.123.45.67:8080/mcp`） |
| **超时时间** | `60` 秒 |
| **安全区域** | 选择 `开发网络 (devnet)` |

#### 2.4 填写 MCP 配置 JSON

**复制以下 JSON 并粘贴到"MCP 配置"框中：**

```json
{
  "mcpServers": {
    "yuanlai-company-agent": {
      "security_zone": "devnet",
      "url": "http://你的DevCloud服务器IP:8080/mcp",
      "timeout": 60,
      "transportType": "streamable-http"
    }
  }
}
```

**⚠️ 注意：**
- 将 `你的DevCloud服务器IP` 替换为第一步中获取的实际 IP 地址
- 例如：`http://10.123.45.67:8080/mcp`

#### 2.5 填写工具定义 JSON

**复制以下 JSON 并粘贴到"工具定义"框中：**

```json
{
  "tools": [
    {
      "name": "query_finance",
      "description": "查询公司财务数据（收入、利润、负债、资产等）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（可选，默认查询整体财务情况）"
          }
        }
      }
    },
    {
      "name": "query_hr",
      "description": "查询人力资源数据（员工信息、职级、薪资等）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（可选，默认查询整体人力情况）"
          }
        }
      }
    },
    {
      "name": "query_rd",
      "description": "查询研发项目数据（项目进度、团队规模等）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（可选，默认查询整体项目情况）"
          }
        }
      }
    },
    {
      "name": "query_company",
      "description": "智能综合查询，自动识别意图并调用相应的子 Agent（推荐使用）",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "查询问题（必填）"
          }
        },
        "required": ["query"]
      }
    }
  ]
}
```

#### 2.6 测试连接
- 点击"检测"按钮
- 应该显示"连接成功"
- 如果失败，检查：
  - DevCloud 服务器是否正在运行
  - IP 地址是否正确
  - 端口 8080 是否开放

#### 2.7 保存 MCP
点击"确认"按钮保存配置

---

### **第三步：在 Knot 创建或配置 Agent**

#### 3.1 创建新 Agent（或编辑现有 Agent）

**如果创建新 Agent：**
1. 点击"创建 Agent"
2. 填写基本信息：

| 字段 | 填写内容 |
|------|---------|
| **Agent 名称** | `元来如此公司助手` |
| **描述** | `公司智能助手，可查询财务、人力、研发信息` |
| **类型** | 选择 `智能体` |

3. 在"系统提示词"中填写：

```
你是"元来如此"公司的智能助手，名字叫"小小元"。

你可以帮助用户查询公司的以下信息：
1. 财务数据：收入、利润、负债、资产等
2. 人力资源：员工信息、职级、薪资等
3. 研发项目：项目进度、团队规模等

当用户提问时，你应该：
1. 识别用户的问题类型
2. 调用相应的工具获取信息
3. 以友好、清晰的方式回答用户

对话风格：轻松、友好，可以使用表情😊
```

#### 3.2 启用 MCP 工具

1. 在 Agent 配置页面找到"工具配置"或"MCP 配置"
2. 勾选启用 `yuanlai-company-agent`
3. 确认 4 个工具都已加载：
   - ✅ query_finance
   - ✅ query_hr
   - ✅ query_rd
   - ✅ query_company

#### 3.3 保存并发布
点击"保存"或"发布"按钮

---

### **第四步：在企微中测试**

#### 4.1 发起对话
- 在企微中找到刚创建的 Agent
- 或在群聊中 @这个 Agent

#### 4.2 测试查询

**测试用例 1：单领域查询**
```
你：老李的职级是多少？
```
预期：Agent 调用 `query_hr` 工具，返回老李的职级和薪资信息

**测试用例 2：跨领域查询**
```
你：公司经营情况怎么样？另外在做什么项目呢？
```
预期：Agent 调用 `query_finance` 和 `query_rd` 工具，返回财务和研发信息

**测试用例 3：综合查询**
```
你：公司整体情况如何？
```
预期：Agent 调用 `query_company` 工具，自动识别并调用所有相关子 Agent

**测试用例 4：超出范围**
```
你：今天天气怎么样？
```
预期：Agent 友好地提示超出服务范围

---

## 📊 **填写内容速查表**

### **Knot MCP 配置**

```
MCP 名称：元来如此公司智能Agent集群
Server Name：yuanlai-company-agent
描述：支持财务、人力资源、研发三个子 Agent 的智能调度
MCP 类型：Streamable HTTP
URL 地址：http://你的DevCloud服务器IP:8080/mcp
超时时间：60
安全区域：开发网络 (devnet)
```

### **MCP 配置 JSON**

```json
{
  "mcpServers": {
    "yuanlai-company-agent": {
      "security_zone": "devnet",
      "url": "http://你的DevCloud服务器IP:8080/mcp",
      "timeout": 60,
      "transportType": "streamable-http"
    }
  }
}
```

### **工具定义 JSON**

见上文"2.5 填写工具定义 JSON"部分

### **Agent 系统提示词**

见上文"3.1 创建新 Agent"部分

---

## 🔧 **故障排查**

### **问题 1：Knot 连接 MCP 失败**

**可能原因：**
- DevCloud 服务器未启动
- IP 地址或端口错误
- 防火墙阻止连接

**解决方法：**
```bash
# 1. 检查服务是否运行
ps aux | grep yuanlai_mcp_server_knot.py

# 2. 检查端口是否监听
netstat -tlnp | grep 8080

# 3. 测试本地访问
curl http://localhost:8080/health

# 4. 查看日志
# 查看服务器输出的日志信息
```

### **问题 2：Agent 调用工具失败**

**可能原因：**
- 工具未正确注册
- 参数格式错误

**解决方法：**
- 在 Knot MCP 管理中查看工具列表
- 检查工具定义 JSON 是否正确
- 查看 DevCloud 服务器日志

### **问题 3：子 Agent 响应超时**

**可能原因：**
- 子 Agent API 响应慢
- 网络问题

**解决方法：**
- 增加超时时间（在 MCP 配置中修改）
- 检查网络连接

---

## 📞 **支持**

如有问题，可以：
1. 查看 GitHub 仓库：https://github.com/XiaoyuanNO1/yuanlai-mcp-server
2. 查看服务器日志
3. 联系开发者

---

## 🎉 **恭喜！**

如果一切顺利，你现在已经成功部署了"元来如此公司智能 Agent 集群"！

在企微中直接提问，Agent 会自动识别意图并调用相应的工具，无需重复配置！
