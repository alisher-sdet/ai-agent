# 40. Database-API-Excel -Understand the Goals of the Multi Agents and its workflow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648233
#       SCENARIO
# - Connect to the database and retrieve necessary information from multiple tables.
# - Read API contract files to understand the required structure for API calls.
# - Use the data fetched from the database to construct a Registration API POST call.
# - Validate the data submission by triggering a Login API GET call.
# - Finally, store the successfully registered user data into an Excel sheet.
#       PLAN of Approach
# • Database Agent
#   A dedicated agent capable of connecting to any database and retrieving data from multiple tables. This agent is responsible for structuring the gathered data and passing it to the downstream agents.
# • API + File System Agent
#   This agent reads API contract definitions from the local file system and prepares itself to make API calls based on the specifications. It consumes the structured data provided by the Database Agent to perform the Registration POST and Login GET calls.
# • Excel Agent
#   Responsible for writing the final, successfully registered user data into an Excel tracker.
#       TECHNICAL IMPLEMENTATION
# • The entire workflow is executed through a multi-agent system that collaborates autonomously to complete the task.
#       TOOLING Support
# • Database MCP - For interacting with various databases
# • API MCP - To manage API call execution
# • File MCP - For accessing and reading API contracts
# • Excel MCP - To write structured data to Excel

# 41. What is AgentFactory? How to isolate and create Agents within factory
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648237
# 42. Part 1 - Build mcp Config file & connect Factory ,Config file to main test flow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648247
# 43. Part 2 - Build mcp Config file & connect Factory ,Config file to main test flow
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648263
# 44. Complete end to end workflow to build Agentic AI solution with AutoGen concepts
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648269
# 45. Part 1 -Provide System messages to Database, API, Excel Agents in logical manner
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648287
# 46. Part 2-Provide System messages to Database, API, Excel Agents in logical manner
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648299
# 47. Run the Multi Agentic workflow & analyze the agents output behaviour in detail
# https://www.udemy.com/course/agentic-ai-for-automation-multi-agent-autogen/learn/lecture/51648301
from dotenv import load_dotenv
import asyncio
import os
from openai import RateLimitError

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from agent_factory import AgentFactory
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

load_dotenv()

os.environ["MCP_REQUEST_TIMEOUT"] = "20"  # 20 секунд
os.environ["AUTOGEN_ALLOWED_DIRS"] = (
    "/Users/user/Documents/ai/ai_rahul/a_autoGen:/Users/user/Documents/ai/ai_agent/a_rahul/LLM-MCP (AI Agent)"
)


async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    factory = AgentFactory(model_client)

    database_agent = factory.create_database_agent(
        system_message="""
            You are a Database specialist responsible for retrieving user registration data.

            Your task:
            1. Connect to the MySQL database 'rahulshettyacademy'
            2. Query the 'RegistrationDetails' table to get a random record
            3. Query the 'Usernames' table to get additional user data
            4. Combine the data from both tables to create complete registration information
            5. Ensure the email is unique by adding a timestamp or random number if needed
            6. Prepare all the registration data in a structured format so that another agent can understand
            When ready, write: "DATABASE_DATA_READY - APIAgent should proceed next"
        """
    )

    api_agent = factory.create_api_agent(
        system_message="""
            You are the ApiAgent responsible for testing REST APIs using Postman collection files.

            Execute these steps strictly:

            1. Wait for the DatabaseAgent message containing user data.  
            Expect keys like: first_name, last_name, phone_number, occupation, gender, password, email

            2. Before sending, clean the data:
            - Remove all dashes, spaces, or special chars from phone_number: mobile number format - 1234567890
            - Ensure userPassword is at least 8 chars, contains a capital letter, a number, and a special character: password should be a format of SecurePass123

            3. When you receive the data, immediately construct **two JSON request bodies**:

            **Registration Request (POST /api/ecom/auth/register)**:
            ```json
            {{
                "firstName": "<first_name>",
                "lastName": "<last_name>",
                "userEmail": "<email>",
                "userRole": "customer",
                "occupation": "<occupation>",
                "gender": "<gender>",
                "userMobile": "<phone_number>",
                "userPassword": "<password>",
                "confirmPassword": "<password>",
                "required": true
            }}

            Login Request (POST /api/ecom/auth/login):
            {{
                "userEmail": "<email>",
                "userPassword": "<password>"
            }}
            Always convert all email addresses to lowercase before making login API calls.
            If registration succeeds but login fails with "Incorrect email or password",
            retry login once automatically using the same email converted to lowercase.

            4. For each request:
            - Use the Postman collection tool test_request
            - Fill the endpoint correctly (e.g. /api/ecom/auth/register, /api/ecom/auth/login)
            - Do not leave any field empty or placeholder-like — always replace <...> with actual data values.
            - Always include the following headers in every POST request:
            {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            - Always include the correct JSON body in the "body" field of the tool call. Do not send empty requests or omit the body key.
            - Before sending each request, log:
                - The full headers you send
                - The full body content
            - If the API returns "First Name is required!" or any missing-field error, it means the request body was not transmitted — automatically retry once with the same data and explicit Content-Type: application/json.

            5. After both calls:
            - If registration succeed (statusCode 200, success true) OR fails with "User already exisits with this Email Id!", then proceed with login
            - If registration succeed (statusCode 200, success true) OR fails with "User already exisits with this Email Id!" and login succeed (statusCode 200, success true), reply exactly:
            API SUCCESS
            - If either fails, reply:
            API FAILURE - include reason

            Then stop immediately.
        """
    )

    excel_agent = factory.create_excel_agent(
        system_message="""
            You are an Excel data management specialist. ONLY proceed when APIAgent has completed testing.

            Your task:
            1. Wait for APIAgent to complete with "API_TESTING_COMPLETE" message that includes login call success
            2. Extract the registration data from DatabaseAgent's REGISTRATION_DATA message
            3. Check APIAgent's response for actual login success/failure status
            4. Only save data if login was actually successful
            5. Open /Users/user/Documents/my/ai_ag/w_registered.xlsx
            6. Add the registration data with current timestamp
            7. Save and verify the data

            CRITICAL: Only save data if APIAgent reports successful login, not just attempted login.

            When complete, write: "REGISTRATION PROCESS COMPLETE" and stop.
        """
    )

    team = RoundRobinGroupChat(
        participants=[database_agent, api_agent, excel_agent],
        termination_condition=TextMentionTermination("REGISTRATION PROCESS COMPLETE"),
    )

    # === RateLimit protection wrapper ===
    max_attempts = 1
    for attempt in range(max_attempts):
        try:
            print(
                f"🚀 Starting registration run (attempt {attempt + 1}/{max_attempts})"
            )
            result = team.run_stream(
                task="""
                Execute Sequential User Registration Process:

                STEP 1 - DatabaseAgent (FIRST): Get random registration data from database tables and format it clearly.
                
                STEP 2 - ApiAgent: Read Postman collection files, then make registration followed by login APIs using the database data.
                
                STEP 3 - ExcelAgent: Save successful registration login details to Excel file.

                Each agent should complete their work fully before the next agent begins.
                Pass data clearly between agents using the specified formats.
                """
            )
            await Console(result)
            break  # ✅ success
        except RateLimitError:
            wait_time = 10 * (attempt + 1)
            print(f"⚠️ OpenAI rate limit hit. Retrying in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            raise
    else:
        print("❌ Failed after multiple retries due to OpenAI rate limits.")

    await model_client.close()


async def shutdown_all(workbenches):
    for wb in workbenches:
        try:
            if hasattr(wb, "shutdown") and callable(wb.shutdown):
                await wb.shutdown()
        except Exception as e:
            print(f"⚠️ Workbench shutdown error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        from mcp_config import McpConfig

        asyncio.run(
            shutdown_all(
                [
                    McpConfig.get_mysql_workbench(),
                    McpConfig.get_rest_api_workbench(),
                    McpConfig.get_excel_workbench(),
                    McpConfig.get_filesystem_workbench(),
                ]
            )
        )
