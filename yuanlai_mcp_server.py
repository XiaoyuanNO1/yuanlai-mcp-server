#!/usr/bin/env python3
"""
元来如此公司 MCP Server
提供统一的子 Agent 调用接口，支持意图识别和任务编排
"""

import json
import uuid
import requests
from typing import Dict, List, Any
from mcp.server import Server
from mcp.types import Tool, TextContent

# 子 Agent 配置
SUB_AGENTS = {
    "finance": {
        "name": "财务助手",
        "app_key": "UeqYdhsBgREPsPqOcXImvHoIjnOzKtaxhYichSIbNPPCLpFLjiafaBFuDYpqArqcdKdCYBtAjJkqKyotbtamdfabIwKRcsnHRVVcPLLVzeVxpFttoaDpAfUNDCnevQlD",
        "description": "负责公司财务数据查询，包括营业收入、利润、负债、现金流等",
        "keywords": ["财务", "收入", "利润", "负债", "现金", "经营", "资产", "成本"]
    },
    "hr": {
        "name": "人力资源助手",
        "app_key": "udeWyBcohDQebXFpbUlhDnhQWoHbtOZWOCuLVInbzVEPyJWUtBkHAvaXwPLzDciTrjyFIdKeepDGvPlWNpmDuxDILeZygBPZjjJtJFzwyXEJyyBjbZzwrGqOCqZdUvuZ",
        "description": "负责人事数据查询，包括员工信息、职级、薪资、入职时间等",
        "keywords": ["员工", "人力", "职级", "薪资", "入职", "人员", "团队", "老张", "老李"]
    },
    "rd": {
        "name": "研发助手",
        "app_key": "ofQEVhJwESeFpsjKtWZybrSOpHMSsMoBymRlDllhuNswHNKXlEOyhRAIQVQujpVnSINfNJExAWaUtuoEiCzaNsZRYKGqbkCXLtXdHtRepmCcogrfVmxPGkNUieOyeCML",
        "description": "负责研发项目查询，包括项目进度、团队规模、技术栈等",
        "keywords": ["项目", "研发", "开发", "进度", "技术", "产品"]
    }
}

# API 配置
API_URL = "https://wss.lke.tencentcloud.com/v1/qbot/chat/sse"
TIMEOUT = 60


def call_sub_agent(agent_type: str, question: str) -> Dict[str, Any]:
    """
    调用子 Agent
    
    Args:
        agent_type: Agent 类型 (finance/hr/rd)
        question: 用户问题
        
    Returns:
        包含回复内容和状态的字典
    """
    if agent_type not in SUB_AGENTS:
        return {
            "success": False,
            "error": f"未知的 Agent 类型: {agent_type}"
        }
    
    agent = SUB_AGENTS[agent_type]
    session_id = str(uuid.uuid4())
    
    payload = {
        "content": question,
        "session_id": session_id,
        "bot_app_key": agent["app_key"],
        "visitor_biz_id": "yuanlai_mcp_server",
        "stream": "disable"
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=TIMEOUT)
        
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            reply = ""
            
            for line in lines:
                if line.startswith('data:'):
                    data_str = line[5:].strip()
                    if data_str and data_str != '[DONE]':
                        try:
                            data = json.loads(data_str)
                            if 'type' in data and data['type'] == 'reply':
                                if 'payload' in data and 'content' in data['payload']:
                                    reply = data['payload']['content']
                        except:
                            pass
            
            if reply:
                return {
                    "success": True,
                    "agent_name": agent["name"],
                    "reply": reply
                }
            else:
                return {
                    "success": False,
                    "error": "未收到有效回复"
                }
        else:
            return {
                "success": False,
                "error": f"API 请求失败: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"调用失败: {str(e)}"
        }


def identify_agents(question: str) -> List[str]:
    """
    识别问题需要调用哪些子 Agent
    
    Args:
        question: 用户问题
        
    Returns:
        需要调用的 Agent 类型列表
    """
    agents = []
    question_lower = question.lower()
    
    for agent_type, config in SUB_AGENTS.items():
        for keyword in config["keywords"]:
            if keyword in question_lower or keyword in question:
                if agent_type not in agents:
                    agents.append(agent_type)
                break
    
    # 如果没有匹配到关键词，尝试通用匹配
    if not agents:
        if any(word in question for word in ["公司", "整体", "情况", "怎么样"]):
            # 可能是综合性问题，返回所有 Agent
            agents = ["finance", "hr", "rd"]
    
    return agents


# 创建 MCP Server
app = Server("yuanlai-company-agent")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="query_finance",
            description="查询公司财务数据，包括营业收入、利润、负债、现金流等财务指标",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "财务相关问题"
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="query_hr",
            description="查询人力资源数据，包括员工信息、职级、薪资、入职时间等",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "人力资源相关问题"
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="query_rd",
            description="查询研发项目数据，包括项目进度、团队规模、技术栈等",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "研发项目相关问题"
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="query_company",
            description="智能查询公司信息，自动识别问题类型并调用相应的子 Agent。支持跨领域的综合查询。",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "关于公司的任何问题"
                    }
                },
                "required": ["question"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """处理工具调用"""
    question = arguments.get("question", "")
    
    if not question:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": "问题不能为空"
            }, ensure_ascii=False)
        )]
    
    # 根据工具名称调用对应的 Agent
    if name == "query_finance":
        result = call_sub_agent("finance", question)
    elif name == "query_hr":
        result = call_sub_agent("hr", question)
    elif name == "query_rd":
        result = call_sub_agent("rd", question)
    elif name == "query_company":
        # 智能识别并调用多个 Agent
        agents = identify_agents(question)
        
        if not agents:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": "这个问题超出了 Agent 的服务范围，咱们换个问题吧"
                }, ensure_ascii=False)
            )]
        
        results = []
        for agent_type in agents:
            result = call_sub_agent(agent_type, question)
            if result["success"]:
                results.append(result)
        
        if results:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "results": results
                }, ensure_ascii=False)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": "所有子 Agent 调用均失败"
                }, ensure_ascii=False)
            )]
    else:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": f"未知的工具: {name}"
            }, ensure_ascii=False)
        )]
    
    return [TextContent(
        type="text",
        text=json.dumps(result, ensure_ascii=False)
    )]


if __name__ == "__main__":
    # 启动 MCP Server
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(main())
