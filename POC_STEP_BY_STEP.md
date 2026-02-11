# 🎯 Knot 平台 POC 部署 - 每一步填写内容

Neil，这是为你准备的 POC 部署指南，包含每一步需要填写的具体内容！

---

## 📍 **你现在的位置**

你已经完成：
- ✅ 代码已上传到 GitHub
- ✅ 部署文档已准备好

你现在需要做：
- 🔄 在 DevCloud 部署 MCP Server
- 🔄 在 Knot 创建 MCP
- 🔄 在 Knot 创建 Agent
- 🔄 在企微测试

---

## 🚀 **第一步：DevCloud 部署（5分钟）**

### 1.1 登录 DevCloud
```
访问：http://devcloud.woa.com
```

### 1.2 打开终端并执行
```bash
# 克隆代码
git clone https://github.com/XiaoyuanNO1/yuanlai-mcp-server.git
cd yuanlai-mcp-server

# 启动服务
bash start_server.sh
```

### 1.3 获取服务器 IP
```bash
# 执行这个命令
hostname -I

# 你会看到类似这样的输出：
# 10.123.45.67 172.17.0.1
# 第一个 IP（10.123.45.67）就是你需要的
```

**📝 记下你的 IP：**`________________`

### 1.4 验证服务
```bash
# 测试健康检查
curl http://localhost:8080/health

# 应该看到：
# {"status": "healthy", "service": "yuanlai-company-agent", ...}
```

✅ **第一步完成！服务器已准备就绪！**

---

## 🎨 **第二步：Knot 创建 MCP（3分钟）**

### 2.1 打开 Knot 平台
```
访问：https://knot.woa.com
点击左侧菜单：MCP 管理 → 新建 MCP
```

### 2.2 填写表单

你会看到一个表单，按照下面的内容填写：

---

#### 📋 **表单字段 1：MCP 名称**
```
元来如此公司智能Agent集群
```

#### 📋 **表单字段 2：Server Name**
```
yuanlai-company-agent
```

#### 📋 **表单字段 3：描述**
```
支持财务、人力资源、研发三个子 Agent 的智能调度
```

#### 📋 **表单字段 4：MCP 类型**
```
选择下拉菜单中的：Streamable HTTP
```

#### 📋 **表单字段 5：URL 地址**
```
http://你的IP:8080/mcp
```
**⚠️ 重要：将"你的IP"替换为第一步中获取的实际 IP**

例如，如果你的 IP 是 `10.123.45.67`，则填写：
```
http://10.123.45.67:8080/mcp
```

#### 📋 **表单字段 6：超时时间**
```
60
```

#### 📋 **表单字段 7：安全区域**
```
选择下拉菜单中的：开发网络 (devnet)
```

---

### 2.3 填写 MCP 配置 JSON

找到"MCP 配置"或"配置 JSON"输入框，**复制粘贴**以下内容：

```json
{
  "mcpServers": {
    "yuanlai-company-agent": {
      "security_zone": "devnet",
      "url": "http://你的IP:8080/mcp",
      "timeout": 60,
      "transportType": "streamable-http"
    }
  }
}
```

**⚠️ 记得替换 `你的IP`！**

---

### 2.4 填写工具定义 JSON

找到"工具定义"或"Tools"输入框，**复制粘贴**以下内容：

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

---

### 2.5 测试连接

- 点击页面上的"检测"或"测试连接"按钮
- 应该显示"连接成功"✅
- 如果失败，检查：
  - DevCloud 服务是否在运行
  - IP 地址是否正确
  - 端口 8080 是否开放

### 2.6 保存

- 点击"确认"或"保存"按钮
- MCP 创建成功！

✅ **第二步完成！MCP 已创建！**

---

## 🤖 **第三步：Knot 创建 Agent（2分钟）**

### 3.1 创建新 Agent
```
在 Knot 平台点击：创建 Agent
```

### 3.2 填写基本信息

---

#### 📋 **字段 1：Agent 名称**
```
元来如此公司助手
```

#### 📋 **字段 2：描述**
```
公司智能助手，可查询财务、人力、研发信息
```

#### 📋 **字段 3：类型**
```
选择：智能体
```

---

### 3.3 填写系统提示词

找到"系统提示词"或"System Prompt"输入框，**复制粘贴**以下内容：

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

---

### 3.4 启用 MCP 工具

1. 找到"工具配置"或"MCP 配置"部分
2. 找到 `yuanlai-company-agent`
3. ✅ **勾选启用**
4. 确认看到 4 个工具：
   - query_finance
   - query_hr
   - query_rd
   - query_company

### 3.5 保存并发布

- 点击"保存"或"发布"按钮
- Agent 创建成功！

✅ **第三步完成！Agent 已就绪！**

---

## 💬 **第四步：企微测试（2分钟）**

### 4.1 打开企微

- 找到刚创建的"元来如此公司助手"
- 发起对话

### 4.2 测试用例

#### 测试 1：单领域查询
```
你输入：老李的职级是多少？
```
**预期结果**：Agent 回复老李的职级（P15）和月薪（88,888元）

---

#### 测试 2：跨领域查询
```
你输入：公司经营情况怎么样？另外在做什么项目呢？
```
**预期结果**：Agent 回复财务数据和项目进展

---

#### 测试 3：综合查询
```
你输入：公司整体情况如何？
```
**预期结果**：Agent 回复完整的公司情况报告

---

#### 测试 4：超出范围
```
你输入：今天天气怎么样？
```
**预期结果**：Agent 友好地提示超出服务范围

---

## 🎉 **恭喜！POC 部署完成！**

如果所有测试都通过，说明部署成功！🎊

---

## 📊 **总结**

你现在拥有：

✅ **在 GitHub 的代码仓库**
- https://github.com/XiaoyuanNO1/yuanlai-mcp-server

✅ **在 DevCloud 运行的 MCP Server**
- 提供 4 个智能工具
- 支持意图识别和任务编排

✅ **在 Knot 平台的 MCP**
- 连接到 DevCloud 服务器
- 注册了 4 个工具

✅ **在 Knot 平台的 Agent**
- 可以在企微中使用
- 自动调用 MCP 工具

✅ **在企微中的智能助手**
- 无需重复配置
- 直接提问即可

---

## 🔧 **如果遇到问题**

### 问题：Knot 连接 MCP 失败

**检查清单：**
```bash
# 1. DevCloud 服务是否运行？
ps aux | grep yuanlai_mcp_server_knot.py

# 2. 端口是否监听？
netstat -tlnp | grep 8080

# 3. 本地访问是否正常？
curl http://localhost:8080/health
```

### 问题：Agent 调用工具失败

**检查清单：**
- Knot MCP 管理中查看 MCP 状态
- 查看 Agent 配置中是否启用了 MCP
- 查看 DevCloud 服务器日志

---

## 📞 **需要帮助？**

- **GitHub 仓库**：https://github.com/XiaoyuanNO1/yuanlai-mcp-server
- **详细文档**：查看 KNOT_POC_DEPLOYMENT_GUIDE.md
- **填写清单**：查看 KNOT_FILL_CHECKLIST.md

---

**祝你 POC 测试顺利！** 😊🚀
