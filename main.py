import os
import asyncio
from dotenv import load_dotenv
from agents.restaurant_agents import RestaurantAgents, AgentState
from rich.console import Console
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage

console = Console()

async def main():
    load_dotenv()
    
    provider = "anthropic"
    model_map = {
        "anthropic": "claude-3-sonnet",
        "openai": "gpt-4",
        "ollama": "mistral"
    }
    
    restaurant_agents = RestaurantAgents(
        provider=provider,
        model_name=model_map[provider]
    )
    graph = restaurant_agents.build_graph()
    
    console.print(f"[bold blue]Multi-Agent Restaurant Assistant[/bold blue] using {provider}")
    console.print("[yellow]Type 'quit' to exit, 'clear' to clear history[/yellow]")
    console.print("=" * 50)
    
    while True:
        try:
            user_input = await asyncio.get_event_loop().run_in_executor(
                None, lambda: input("You: ").strip()
            )
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                console.print("[green]Chat history cleared![/green]")
                continue
            elif not user_input:
                continue
            
            state = AgentState(
                messages=[HumanMessage(content=user_input)],
                next_agent="",
                current_agent="",
                final_answer=""
            )
            
            result = graph.invoke(state)
            final_message = result["messages"][-1].content
            
            console.print("\n[bold cyan]AI:[/bold cyan]")
            console.print(Markdown(final_message))
            console.print("\n" + "=" * 50)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Gracefully shutting down...[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    asyncio.run(main())