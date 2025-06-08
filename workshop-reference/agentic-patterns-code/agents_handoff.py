from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

german_agent = Agent(
    name="German Assistant",
    instructions="Always respond in German. Be polite and concise.",
)

english_agent = Agent(
    name="English Assistant",
    instructions="Always respond in English.",
)

customer_service_manager = Agent(
    name="Customer Service Manager",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[german_agent, english_agent],
)

async def main():
    query = "Halo, what a good day!"
    result = await Runner.run(
        customer_service_manager,
        query
    )
    print(f"👧: {query}")
    print(f"🤖: {result.final_output}")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())