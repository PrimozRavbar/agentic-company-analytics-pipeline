
from smolagents import ToolCallingAgent, TransformersModel


def build_agent(tools):
    model = TransformersModel(
        model_id="Qwen/Qwen3-1.7B",
        device_map="auto",
        max_new_tokens=100,
        apply_chat_template_kwargs={"enable_thinking": False},
    )

    return ToolCallingAgent(
        tools=tools,
        model=model,
        max_steps=3,
    )


def run_agent(agent, task):
    return agent.run(task)
