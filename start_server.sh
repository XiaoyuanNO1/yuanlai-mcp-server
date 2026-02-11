#!/bin/bash
# 元来如此公司 MCP Server 启动脚本

echo "================================================"
echo "  元来如此公司智能 Agent 集群 - MCP Server"
echo "================================================"

# 检查 Python 版本
python3 --version

# 安装依赖
echo ""
echo ">>> 安装依赖..."
pip3 install -r requirements.txt

# 启动服务
echo ""
echo ">>> 启动 MCP Server..."
python3 yuanlai_mcp_server_knot.py 8080
