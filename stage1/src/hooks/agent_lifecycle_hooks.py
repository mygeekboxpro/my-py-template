import logging

from agents.lifecycle import AgentHooksBase


from shared.logs.structured_logging import setup_json_logging

setup_json_logging()
logger = logging.getLogger(__name__)


"""
Usage:

# attach to a specific agent
specific_agent.hooks = PerAgentHooks()

If you want it on the agent-tools, you must set it before .as_tool(...):
    a = build_agent(...)
    a.hooks = PerAgentHooks()
    tool = a.as_tool(...)
"""

class PerAgentHooks(AgentHooksBase):
    async def on_llm_end(self, context, agent, response):
        logger.info("agent.llm_end", extra={"agent": agent.name})


