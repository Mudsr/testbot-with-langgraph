from typing import Annotated, Dict, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.graph import Graph, END
from .base_agent import BaseAgent

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_agent: str
    current_agent: str
    final_answer: str

class RestaurantAgents:
    def __init__(self, provider: str = "anthropic", model_name: str = "claude-3-sonnet"):
        self.menu_agent = BaseAgent(
            model_name=model_name,
            temperature=0.7,
            system_prompt="You are a menu expert. You provide detailed information about menu items, ingredients, and help customers understand dish descriptions.",
            provider=provider
        )
        
        self.pricing_agent = BaseAgent(
            model_name=model_name,
            temperature=0.7,
            system_prompt="You are a pricing specialist. You help calculate total costs, suggest combinations within budget, and handle any pricing queries.",
            provider=provider
        )
        
        self.dietary_agent = BaseAgent(
            model_name=model_name,
            temperature=0.7,
            system_prompt="You are a dietary consultant. You help identify suitable dishes based on dietary restrictions (vegetarian, vegan, gluten-free, etc) and provide nutritional guidance.",
            provider=provider
        )
        
        self.coordinator_agent = BaseAgent(
            model_name=model_name,
            temperature=0.7,
            system_prompt="You are the coordinator. Analyze user queries and decide which specialist agent should handle them: 'menu' for menu information, 'pricing' for cost calculations, 'dietary' for dietary advice, or 'final' if the query is resolved.",
            provider=provider
        )
    
    def route_query(self, state: AgentState) -> str:
        """Determine which agent should handle the query next"""
        messages = state["messages"]
        response = self.coordinator_agent.process_message(messages[-1].content)
        
        last_line = response.strip().split('\n')[-1].lower()
        
        if "menu" in last_line:
            return "menu_agent"
        elif "pricing" in last_line:
            return "pricing_agent"
        elif "dietary" in last_line:
            return "dietary_agent"
        else:
            return "end"
    
    def menu_agent_step(self, state: AgentState) -> AgentState:
        """Handle menu-related queries"""
        response = self.menu_agent.process_message(state["messages"][-1].content)
        state["messages"].append(AIMessage(content=response))
        return state
    
    def pricing_agent_step(self, state: AgentState) -> AgentState:
        """Handle pricing-related queries"""
        response = self.pricing_agent.process_message(state["messages"][-1].content)
        state["messages"].append(AIMessage(content=response))
        return state
    
    def dietary_agent_step(self, state: AgentState) -> AgentState:
        """Handle dietary-related queries"""
        response = self.dietary_agent.process_message(state["messages"][-1].content)
        state["messages"].append(AIMessage(content=response))
        return state
    
    def build_graph(self) -> Graph:
        """Build the LangGraph workflow"""
        workflow = Graph()
        
        workflow.add_node("route", self.route_query)
        workflow.add_node("menu_agent", self.menu_agent_step)
        workflow.add_node("pricing_agent", self.pricing_agent_step)
        workflow.add_node("dietary_agent", self.dietary_agent_step)
        
        workflow.set_entry_point("route")
        
        workflow.add_conditional_edges(
            "route",
            lambda x: x,
            {
                "menu_agent": "menu_agent",
                "pricing_agent": "pricing_agent",
                "dietary_agent": "dietary_agent",
                "end": END
            }
        )
        
        workflow.add_edge("menu_agent", "route")
        workflow.add_edge("pricing_agent", "route")
        workflow.add_edge("dietary_agent", "route")
        
        return workflow.compile()