# 41. What is AgentFactory? How to isolate and create Agents within factory
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648237
# 42. Part 1 - Build mcp Config file & connect Factory ,Config file to main test flow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648247
# 43. Part 2 - Build mcp Config file & connect Factory ,Config file to main test flow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648263
from autogen_agentchat.agents import AssistantAgent
from mcp_config import McpConfig


class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client
        self.mcp_config = McpConfig()

    def create_database_agent(self, system_message):
        database_agent = AssistantAgent(
            name="DatabaseAgent",
            model_client=self.model_client,
            workbench=self.mcp_config.get_mysql_workbench(),
            system_message=system_message,
        )
        return database_agent

    def create_api_agent(self, system_message):
        api_agent = AssistantAgent(
            name="ApiAgent",
            model_client=self.model_client,
            workbench=[
                self.mcp_config.get_rest_api_workbench(),
                self.mcp_config.get_filesystem_workbench(),
            ],
            system_message=system_message,
        )
        return api_agent

    def create_excel_agent(self, system_message):
        excel_agent = AssistantAgent(
            name="ExcelAgent",
            model_client=self.model_client,
            workbench=self.mcp_config.get_excel_workbench(),
            system_message=system_message,
        )
        return excel_agent
