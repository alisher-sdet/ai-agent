# 41. What is AgentFactory? How to isolate and create Agents within factory
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648237
# 42. Part 1 - Build mcp Config file & connect Factory ,Config file to main test flow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648247
# 43. Part 2 - Build mcp Config file & connect Factory ,Config file to main test flow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648263


# 47. Run the Multi Agentic workflow & analyze the agents output behaviour in detail
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648301
import os
from pathlib import Path
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

# Путь к проекту
PROJECT_ROOT = Path(__file__).parent
# PROJECT_ROOT = Path(__file__)

# Путь к виртуальной среде .venv
VENV_PATH = PROJECT_ROOT / ".venv"


class McpConfig:

    @staticmethod
    def get_mysql_workbench():
        # https://github.com/designcomputer/mysql_mcp_server
        mysql_server_params = StdioServerParams(
            # command="/Users/user/Documents/my/ai_ag/.venv/bin/uv",
            command=str(VENV_PATH / "bin" / "uv"),  # uv из .venv/bin/
            args=[
                "--directory",
                # "/Users/user/Documents/my/ai_ag/.venv/lib/python3.14/site-packages",
                str(VENV_PATH / "lib" / "python3.14" / "site-packages"),
                "run",
                "mysql_mcp_server",
            ],
            env={
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "root",
                "MYSQL_PASSWORD": "Qwerty123@",
                "MYSQL_DATABASE": "rahulshettyacademy",
                # передаем текущие переменные окружения (по желанию)
                # **os.environ,
            },
        )
        return McpWorkbench(server_params=mysql_server_params)

    @staticmethod
    def get_rest_api_workbench():
        rest_api_server_params = StdioServerParams(
            command="node",
            args=["/opt/homebrew/lib/node_modules/dkmaker-mcp-rest-api/build/index.js"],
            env={
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json",
            },
        )
        # rest_api_server_params = StdioServerParams(
        #     command="npx",
        #     args=["-y", "dkmaker-mcp-rest-api"],
        #     env={
        #         "REST_BASE_URL": "https://rahulshettyacademy.com",
        #         "HEADER_Accept": "application/json",
        #     },
        # )
        return McpWorkbench(server_params=rest_api_server_params)

    @staticmethod
    def get_excel_workbench():
        # excel_server_params = StdioServerParams(
        #     command="npx",
        #     args=[
        #         "-y",
        #         "@smithery/cli@latest",
        #         "run",
        #         "@negokaz/excel-mcp-server",
        #         "--key",
        #         "e714c374-25e0-4bf4-b1c3-229b65ad2db2",
        #     ],
        # )
        excel_server_params = StdioServerParams(
            command="npx",
            args=[
                "@negokaz/excel-mcp-server",
            ],
            env={
                "NODE_NO_WARNINGS": "1",
                "NO_SMITHERY_RELAY": "true",
            },
        )
        return McpWorkbench(server_params=excel_server_params)

    @staticmethod
    def get_filesystem_workbench():
        filesystem_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                # "/Users/user/Documents/ai/ai_agent/a_rahul/LLM-MCP (AI Agent)",
                "/Users/user/Documents/my/ai_ag",
            ],
        )
        return McpWorkbench(server_params=filesystem_server_params)
