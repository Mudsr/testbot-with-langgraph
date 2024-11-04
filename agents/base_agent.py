from typing import List, Tuple, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_models import ChatOllama
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

class BaseAgent:
    def __init__(
        self,
        model_name: str = "claude-3-sonnet",
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        provider: str = "anthropic"
    ):
        self.provider = provider
        self.model_name = model_name
        self.temperature = temperature
        
        if provider == "ollama":
            self.llm = ChatOllama(
                model=model_name,
                temperature=temperature
            )
        elif provider == "huggingface":
            self.llm = HuggingFaceHub(
                repo_id=model_name,
                task="text-generation",
                model_kwargs={
                    "temperature": temperature,
                    "max_length": 512
                }
            )
        elif provider == "anthropic":
            self.llm = ChatAnthropic(
                model_name=model_name,
                temperature=temperature
            )
        elif provider == "openai":
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
        self.system_prompt = system_prompt
        
    def process_message(
        self,
        message: str,
        chat_history: Optional[List[Tuple[str, str]]] = None
    ) -> str:
        messages = []
        
        if self.system_prompt:
            messages.append(SystemMessage(content=self.system_prompt))
        
        if chat_history:
            for human, ai in chat_history:
                messages.append(HumanMessage(content=human))
                messages.append(AIMessage(content=ai))
        
        messages.append(HumanMessage(content=message))
        
        response = self.llm.invoke(messages)
        return response.content 