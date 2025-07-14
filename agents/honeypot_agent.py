import subprocess, os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI

load_dotenv()

def start_honeypot(_: str) -> str:
    subprocess.Popen(['bash', 'scripts/start_honeypot.sh'])
    return "✔️ Honeypot server starting on port 2222."

def stop_honeypot(_: str) -> str:
    subprocess.run(['pkill', '-f', 'ssh_honeypot.py'])
    return "🛑 Honeypot server stopped."

tools = [
    Tool(name="start_honeypot", func=start_honeypot,
         description="Start the SSH honeypot server."),
    Tool(name="stop_honeypot", func=stop_honeypot,
         description="Stop the SSH honeypot server."),
]

llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    print("🕹️  HoneypotAgent ready. Type 'exit' to quit.")
    while True:
        q = input("HoneypotAgent> ")
        if q.lower() in ("exit", "quit"): break
        print(agent.run(q))
