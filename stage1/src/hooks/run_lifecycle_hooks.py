import json
import logging

from agents.lifecycle import RunHooksBase  # <-- hooks base
# from agents.run import RunConfig  # optional if you want run_config settings

from shared.logs.structured_logging import setup_json_logging

setup_json_logging()
logger = logging.getLogger(__name__)

"""
Run-level lifecycle hooks.

Observes:
- agent execution
    - on_agent_start (fires for → Agents and tool-agents)
    - on_agent_end   (fires for → Agents and tool-agents)
- LLM calls
    - on_llm_start   (fires for → Agents and tool-agents)
    - on_llm_end     (fires for → Agents and tool-agents)
- tool execution     (including @function_tool, agent-as-tool)
    - on_tool_start  (fires for → Agents and tool-agents)
    - on_tool_end    (fires for → Agents and tool-agents)

That means it can receive callbacks for:
    - Agent lifecycle (on_agent_start/end, on_llm_start/end)
    - llm lifecycle   (on_llm_end/end, on_agent_start/end)
    - Tool lifecycle  (on_tool_start/end)
    

Intended for logging, tracing, and observability.
"""


class RunLifecycleHooks(RunHooksBase):
    async def on_tool_end(self, context, agent, tool, result: str) -> None:
        # result is the tool output as a string (your generated email text)
        logger.info(
            "***** tool.email.generated *****",
            extra={
                "running_agent": getattr(agent, "name", None),
                "tool_name": getattr(tool, "name", None),
                "tool_type": type(tool).__name__,
                "email_text": result,
            },
        )

    async def on_agent_end(self, context, agent, output) -> None:
        # optional: log each agent's final output too
        logger.info(
            "***** agent.output.generated *****",
            extra={
                "agent_name": getattr(agent, "name", None),
                "agent_output": output,
            },
        )

    async def on_llm_end(self, context, agent, response) -> None:
        logger.info("***** llm.end *****",
                    extra={"calling.agent": agent.name,},
                    )
