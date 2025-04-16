import os, time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def create_project_client() -> AIProjectClient:
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["AZURE_AI_PROJECT_CONNECTION_STRING"],
    )
    return project_client


def create_agent_thread(project_client) -> tuple:
    agent = project_client.agents.create_agent(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are helpful assistant",
    )
    thread = project_client.agents.create_thread()
    return agent.id, thread.id


def agent_run(project_client, agent_id: str, thread_id: str, query: str):
    run = project_client.agents.create_run(thread_id=thread_id, agent_id=agent_id)

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = project_client.agents.get_run(thread_id=thread_id, run_id=run.id)

    messages = project_client.agents.list_messages(thread_id=thread_id)

    for item in messages["data"]:
        if item["role"] == "assistant":
            answer = item["content"][0]
            return answer["text"]["value"]

    print("No assistant message found in the response.")
    return None
