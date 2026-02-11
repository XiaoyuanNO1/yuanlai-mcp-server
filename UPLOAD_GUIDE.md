# GitHub 上传指南

## 📋 当前状态

✅ 已完成：
- Git 仓库已初始化
- 所有文件已添加并提交
- 分支已切换到 `main`

## 🚀 上传步骤

### 方式一：手动在 GitHub 网页创建仓库（推荐）

1. **访问 GitHub**：https://github.com/new

2. **创建新仓库**：
   - Repository name: `yuanlai-mcp-server`
   - Description: `元来如此公司智能Agent集群 - MCP Server`
   - 选择 **Public**
   - ❌ **不要**勾选 "Add a README file"
   - ❌ **不要**勾选 "Add .gitignore"
   - ❌ **不要**勾选 "Choose a license"
   - 点击 "Create repository"

3. **在 AnyDev 开发机执行推送命令**：

```bash
cd /data/workspace/yuanlai-mcp-server
git remote add origin https://github.com/xiaoyuan_no1_888/yuanlai-mcp-server.git
git push -u origin main
```

4. **输入凭据**：
   - Username: `xiaoyuan_no1_888`
   - Password: 使用 **Personal Access Token**（不是密码）

### 方式二：使用 Personal Access Token

#### 步骤 1：创建 Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选权限：
   - ✅ `repo` (完整仓库访问权限)
4. 点击 "Generate token"
5. **复制 Token**（只显示一次！）

#### 步骤 2：在 AnyDev 执行

```bash
cd /data/workspace/yuanlai-mcp-server

# 先在 GitHub 网页创建仓库（见方式一步骤2）

# 添加远程仓库（使用 Token）
git remote add origin https://YOUR_TOKEN@github.com/xiaoyuan_no1_888/yuanlai-mcp-server.git

# 推送
git push -u origin main
```

将 `YOUR_TOKEN` 替换为你的 Token。

### 方式三：SSH 方式（最安全）

#### 步骤 1：生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "xiaoyuan_no1_888@github.com"
cat ~/.ssh/id_ed25519.pub
```

#### 步骤 2：添加到 GitHub

1. 复制公钥内容
2. 访问：https://github.com/settings/keys
3. 点击 "New SSH key"
4. 粘贴公钥，保存

#### 步骤 3：推送

```bash
cd /data/workspace/yuanlai-mcp-server
git remote add origin git@github.com:xiaoyuan_no1_888/yuanlai-mcp-server.git
git push -u origin main
```

## 📦 仓库内容

- `yuanlai_mcp_server.py` - MCP Server 核心代码
- `yuanlai_mcp_config.json` - MCP 配置文件
- `yuanlai_agents_registry.json` - 子 Agent 注册表
- `requirements.txt` - Python 依赖
- `README.md` - 项目文档

## 🎯 预期结果

上传成功后，你可以访问：
```
https://github.com/xiaoyuan_no1_888/yuanlai-mcp-server
```

查看你的仓库！

## ❓ 常见问题

### Q: 推送时提示 "Authentication failed"
A: 需要使用 Personal Access Token，不能使用密码

### Q: 如何获取 Token？
A: 访问 https://github.com/settings/tokens 创建

### Q: Token 需要什么权限？
A: 勾选 `repo` 权限即可

## 🔒 安全提醒

- ⚠️ 密码 `Xiaoyuan888` 已在对话中暴露
- ✅ 建议上传完成后立即修改密码
- ✅ 或使用 Token 代替密码（更安全）
