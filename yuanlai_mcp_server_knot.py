#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元来如此公司智能 Agent 集群 - MCP Server (Knot 版本)
支持 SSE (Server-Sent Events) 协议，符合 Knot 平台 MCP 标准
"""

import json
import logging
import sys
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 子 Agent 配置
SUB_AGENTS = {
    "finance": {
        "name": "财务助手",
        "bot_app_key": "UeqYdhsBgREPsPqOcXImvHoIjnOzKtaxhYichSIbNPPCLpFLjiafaBFuDYpqArqcdKdCYBtAjJkqKyotbtamdfabIwKRcsnHRVVcPLLVzeVxpFttoaDpAfUNDCnevQlD",
        "keywords": ["财务", "收入", "利润", "负债", "资产", "现金", "毛利", "营收", "经营", "财报", "账款"]
    },
    "hr": {
        "name": "人力资源助手",
        "bot_app_key": "wKiLcMbXyKMmfQaJNIqEZhAcPVOhPMdlFHrBnMZXPYfNlMCNtVpZkUwWBpGAYXWmRYKwwlUZILpwZRJQJUgDvOtTzlLPFuIKlkDCRVxXdPLGJgXLfIHxEcgZjqgZvHAy",
        "keywords": ["人力", "员工", "职级", "薪资", "工资", "月薪", "人员", "团队", "招聘", "离职", "入职"]
    },
    "rd": {
        "name": "研发助手",
        "bot_app_key": "ofQEVhJwESeFpsjKtWZybrSOpHMSsMoBymRlDllhuNswHNKXlEOyhRAIQVQujpVnSINfNJExAWaUtuoEiCzaNsZRYKGqbkCXLtXdHtRepmCcogrfVmxPGkNUieOyeCML",
        "keywords": ["研发", "项目", "开发", "进度", "技术", "代码", "产品", "需求", "测试", "上线"]
    }
}

# API 配置
API_URL = "https://wss.lke.tencentcloud.com/v1/qbot/chat/sse"
VISITOR_BIZ_ID = "xiaoxiaoyuan_master_agent"


class MCPRequestHandler(BaseHTTPRequestHandler):
    """处理 MCP 请求的 HTTP Handler"""
    
    def do_GET(self):
        """处理 GET 请求 - 健康检查"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "yuanlai-company-agent",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """处理 POST 请求 - MCP 工具调用"""
        if self.path.startswith('/mcp'):
            self._handle_mcp_request()
        else:
            self.send_response(404)
            self.end_headers()
    
    def _handle_mcp_request(self):
        """处理 MCP 请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(body)
            
            logger.info(f"收到 MCP 请求: {request_data}")
            
            # 解析请求
            tool_name = request_data.get('method', '')
            params = request_data.get('params', {})
            
            # 路由到对应的工具处理函数
            if tool_name == 'query_finance':
                result = self._query_finance(params)
            elif tool_name == 'query_hr':
                result = self._query_hr(params)
            elif tool_name == 'query_rd':
                result = self._query_rd(params)
            elif tool_name == 'query_company':
                result = self._query_company(params)
            elif tool_name == 'list_tools':
                result = self._list_tools()
            else:
                result = {
                    "error": f"未知的工具: {tool_name}",
                    "available_tools": ["query_finance", "query_hr", "query_rd", "query_company", "list_tools"]
                }
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "jsonrpc": "2.0",
                "id": request_data.get('id', 1),
                "result": result
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            logger.info(f"MCP 响应已发送")
            
        except Exception as e:
            logger.error(f"处理 MCP 请求失败: {str(e)}", exc_info=True)
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                "jsonrpc": "2.0",
                "id": request_data.get('id', 1) if 'request_data' in locals() else 1,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def _call_sub_agent(self, agent_type: str, query: str) -> str:
        """调用子 Agent"""
        try:
            agent_config = SUB_AGENTS.get(agent_type)
            if not agent_config:
                return f"错误: 未找到 {agent_type} Agent"
            
            session_id = str(uuid.uuid4())
            payload = {
                "content": query,
                "session_id": session_id,
                "bot_app_key": agent_config["bot_app_key"],
                "visitor_biz_id": VISITOR_BIZ_ID,
                "stream": "disable"
            }
            
            headers = {"Content-Type": "application/json"}
            
            logger.info(f"调用 {agent_config['name']}: {query}")
            
            response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines:
                    if line.startswith('data:'):
                        data_str = line[5:].strip()
                        if data_str and data_str != '[DONE]':
                            try:
                                data = json.loads(data_str)
                                if data.get('type') == 'reply':
                                    content = data.get('payload', {}).get('content', '')
                                    if content:
                                        logger.info(f"{agent_config['name']} 响应成功")
                                        return content
                            except:
                                pass
                
                return f"{agent_config['name']} 未返回有效内容"
            else:
                return f"{agent_config['name']} 请求失败: HTTP {response.status_code}"
                
        except Exception as e:
            logger.error(f"调用 {agent_type} Agent 失败: {str(e)}")
            return f"{agent_type} Agent 调用异常: {str(e)}"
    
    def _identify_intent(self, query: str) -> list:
        """识别用户意图，返回需要调用的 Agent 列表"""
        query_lower = query.lower()
        agents_needed = []
        
        # 检查是否匹配各个 Agent 的关键词
        for agent_type, config in SUB_AGENTS.items():
            if any(keyword in query_lower for keyword in config["keywords"]):
                agents_needed.append(agent_type)
        
        # 如果没有匹配到任何关键词，返回空列表
        return agents_needed if agents_needed else []
    
    def _query_finance(self, params: dict) -> dict:
        """查询财务数据"""
        query = params.get('query', '公司财务情况怎么样？')
        result = self._call_sub_agent('finance', query)
        return {
            "agent": "财务助手",
            "query": query,
            "response": result
        }
    
    def _query_hr(self, params: dict) -> dict:
        """查询人力资源数据"""
        query = params.get('query', '公司人力资源情况怎么样？')
        result = self._call_sub_agent('hr', query)
        return {
            "agent": "人力资源助手",
            "query": query,
            "response": result
        }
    
    def _query_rd(self, params: dict) -> dict:
        """查询研发项目数据"""
        query = params.get('query', '公司研发项目情况怎么样？')
        result = self._call_sub_agent('rd', query)
        return {
            "agent": "研发助手",
            "query": query,
            "response": result
        }
    
    def _query_company(self, params: dict) -> dict:
        """智能综合查询"""
        query = params.get('query', '')
        
        if not query:
            return {
                "error": "请提供查询问题",
                "example": "公司现在经营情况怎么样？在做什么项目？"
            }
        
        # 识别意图
        agents_needed = self._identify_intent(query)
        
        if not agents_needed:
            return {
                "message": "抱歉，这个问题超出了我的服务范围。我可以帮你查询公司的财务、人力资源和研发项目信息。",
                "available_services": [
                    "财务数据（收入、利润、负债等）",
                    "人力资源（员工信息、职级、薪资等）",
                    "研发项目（项目进度、团队规模等）"
                ]
            }
        
        # 调用相应的 Agent
        results = {}
        for agent_type in agents_needed:
            agent_config = SUB_AGENTS[agent_type]
            result = self._call_sub_agent(agent_type, query)
            results[agent_config["name"]] = result
        
        # 汇总结果
        summary = f"根据您的问题「{query}」，我为您查询了以下信息：\n\n"
        for agent_name, response in results.items():
            summary += f"## {agent_name}\n{response}\n\n"
        
        return {
            "query": query,
            "agents_called": [SUB_AGENTS[a]["name"] for a in agents_needed],
            "summary": summary,
            "details": results
        }
    
    def _list_tools(self) -> dict:
        """列出所有可用工具"""
        return {
            "tools": [
                {
                    "name": "query_finance",
                    "description": "查询公司财务数据（收入、利润、负债、资产等）",
                    "parameters": {
                        "query": "查询问题（可选，默认查询整体财务情况）"
                    }
                },
                {
                    "name": "query_hr",
                    "description": "查询人力资源数据（员工信息、职级、薪资等）",
                    "parameters": {
                        "query": "查询问题（可选，默认查询整体人力情况）"
                    }
                },
                {
                    "name": "query_rd",
                    "description": "查询研发项目数据（项目进度、团队规模等）",
                    "parameters": {
                        "query": "查询问题（可选，默认查询整体项目情况）"
                    }
                },
                {
                    "name": "query_company",
                    "description": "智能综合查询，自动识别意图并调用相应的子 Agent（推荐使用）",
                    "parameters": {
                        "query": "查询问题（必填）"
                    }
                }
            ]
        }
    
    def log_message(self, format, *args):
        """重写日志方法"""
        logger.info(f"{self.client_address[0]} - {format % args}")


def run_server(port=8080):
    """启动 MCP Server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    
    logger.info(f"元来如此公司 MCP Server 启动成功！")
    logger.info(f"监听端口: {port}")
    logger.info(f"健康检查: http://localhost:{port}/health")
    logger.info(f"MCP 端点: http://localhost:{port}/mcp")
    logger.info(f"支持的子 Agent: {', '.join([v['name'] for v in SUB_AGENTS.values()])}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭服务器...")
        httpd.shutdown()
        logger.info("服务器已关闭")


if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error(f"无效的端口号: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(port)
