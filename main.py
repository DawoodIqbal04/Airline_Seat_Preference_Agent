from agents import Agent, Runner, trace, RunContextWrapper, SQLiteSession
from llm_connection import config
import asyncio
from pydantic import BaseModel

session = SQLiteSession('session_101')

class Passenger(BaseModel):
    seat_preference: str
    travel_experience: str
    
passenger = Passenger(
    seat_preference= input('\nIn which seat you want to travel. e.g.(Window, Middle, Any): '),
    travel_experience= input('\nHow often you travel on plane. e.g.(First time, occasional, frequent): ')
)

def dynamic_context(ctx: RunContextWrapper[Passenger], agent: Agent):
    if 'window' in ctx.context.seat_preference.lower() and 'first time' in ctx.context.travel_experience.lower():
        return 'You are Airline seat prefrence agent. Explain the benefits of window seat and as it is first time plane experience of passenger so mention scenic views and reassure about flight experience'
    elif 'middle' in ctx.context.seat_preference.lower() and 'occasional' in ctx.context.travel_experience.lower():
        return 'You are Airline seat prefrence agent. Acknowledge the compromise as it is middle seat and offer alternatives of it and suggest stratigies as the passenger travels occasionally. '
    elif 'any' in ctx.context.seat_preference.lower() and 'premium' in ctx.context.travel_experience.lower():
        return 'You are Airline seat prefrence agent. Highlight the luxury of the class as it is any seat with premium experience for passenger.'

preference_agent = Agent(
    name= 'Airline Seat Preference Agent',
    instructions= dynamic_context,
    
)

async def main():
    while True:
        user_input = input('\nIt is Your Seat Preference Agent. (quit or exit to terminate): ')
        
        if user_input.lower() in ['quit', 'exit']:
            break
        
        with trace('Airline Seat Pref Agent'):
            result = await Runner.run(
                preference_agent,
                input= user_input,
                session= session,
                run_config= config,
                context= passenger
            )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
