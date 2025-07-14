import pandas as pd
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI

def analyze_logs(_: str) -> str:
    df = pd.read_csv('honeypot.log', sep=' - ', names=['timestamp','message'], engine='python')
    # Extract IPs and commands
    df_cmds = df['message'].str.extract(r"CMD (\d+\.\d+\.\d+\.\d+):\d+ -> (.*)")
    df_cmds.columns = ['ip','cmd']
    counts = df_cmds['ip'].value_counts().to_dict()
    report = "🔍 **Connection attempts by IP**\n"
    for ip, cnt in counts.items():
        report += f"- {ip}: {cnt} attempts\n"
    return report

tools = [
    Tool(name="analyze_logs", func=analyze_logs,
         description="Summarize connection attempts from honeypot.log"),
]

llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    print("🕵️ AnalyzerAgent ready.")
    while True:
        q = input("AnalyzerAgent> ")
        if q.lower() in ("exit", "quit"): break
        print(agent.run(q))
