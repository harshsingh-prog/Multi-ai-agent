from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.config.settings import settings


def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):

    llm = ChatGroq(
        model=llm_id,
        api_key=settings.GROQ_API_KEY
    )

    tools = [TavilySearch(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # ✅ FIXED MESSAGE FORMAT
    messages = []

    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))

    for q in query:
        messages.append(HumanMessage(content=q))

    state = {"messages": messages}

    response = agent.invoke(state)

    ai_messages = [
        msg.content for msg in response["messages"]
        if isinstance(msg, AIMessage)
    ]

    return ai_messages[-1]
