import os, smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI

load_dotenv()
USER = os.getenv("EMAIL_USER")
PASS = os.getenv("EMAIL_PASS")
HOST = os.getenv("EMAIL_HOST")
PORT = int(os.getenv("EMAIL_PORT", "587"))

def send_email(body: str) -> str:
    msg = MIMEText(body)
    msg['Subject'] = "🚨 Honeypot Alert"
    msg['From'] = USER
    msg['To'] = USER
    with smtplib.SMTP(HOST, PORT) as s:
        s.starttls()
        s.login(USER, PASS)
        s.send_message(msg)
    return "✉️ Alert email sent."

tools = [
    Tool(name="send_email", func=send_email,
         description="Send an email alert with given message"),
]

llm = OpenAI(temperature=0.2)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

if __name__ == "__main__":
    print("📣 AlertAgent ready.")
    while True:
        q = input("AlertAgent> ")
        if q.lower() in ("exit", "quit"): break
        print(agent.run(q))
