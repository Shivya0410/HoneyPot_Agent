##SSH Honeypot AI Agent System — Full Setup & Explanation

#What You're Building
A complete AI-powered honeypot system using:
SSH Honeypot — Python + Paramiko to simulate an SSH server


LangChain Agents — Autonomously control honeypot, analyze logs, and send alerts


FastAPI — REST API interface for your agents


Spammer Bot — Simulated brute-force attacker


Core ML (optional) — Detect anomalous behavior in logs



#Project Structure
bash
CopyEdit
honeypot_agent/
├── server/                # SSH honeypot
│   └── ssh_honeypot.py
├── agents/                # LangChain agents
│   ├── honeypot_agent.py
│   ├── analyzer_agent.py
│   └── alert_agent.py
├── scripts/               # CLI utilities
│   ├── spam_ssh.py        # Brute-force attacker
│   └── start_honeypot.sh
├── main.py                # FastAPI server
├── honeypot.log           # Captured logs
├── requirements.txt
├── .env                   # OpenAI and email creds
└── userlist.txt, passlist.txt


#SETUP — COPY & PASTE
1. Clone & install
bash
CopyEdit
git clone https://github.com/YOU/honeypot_agent.git
cd honeypot_agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Generate SSH key for honeypot
bash
CopyEdit
ssh-keygen -t rsa -b 2048 -f server/host_rsa_key -N ""


3. Fix Paramiko constant bug
bash
CopyEdit
nano server/ssh_honeypot.py

At the top, add:
python
CopyEdit
from paramiko.common import OPEN_SUCCEEDED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

Then update the method:
python
CopyEdit
def check_channel_request(self, kind, chanid):
    return OPEN_SUCCEEDED if kind == 'session' else OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


#RUNNING THE SYSTEM
4. Start everything
bash
CopyEdit
source venv/bin/activate
pkill -f ssh_honeypot.py || true
pkill -f "uvicorn main:app" || true
bash scripts/start_honeypot.sh &
uvicorn main:app --reload &

5. Launch attacker bot
bash
CopyEdit
chmod +x scripts/spam_ssh.py
./scripts/spam_ssh.py --forever &

6. Watch log
bash
CopyEdit
tail -f honeypot.log

7. Test endpoints
bash
CopyEdit
# Start honeypot
curl -X POST http://127.0.0.1:8000/honeypot/start

# Get log summary
curl http://127.0.0.1:8000/logs/summary

# Send alert
curl -X POST http://127.0.0.1:8000/alert \
  -H "Content-Type: application/json" \
  -d '{"message":"Test alert"}'


#GPT CANVAS — How It Works
pgsql
CopyEdit
User
   ↓
FastAPI (main.py) — RESTful endpoints
   ↓
LangChain Agents (honeypot, analyzer, alert)
   ↓
Tools (start honeypot, read logs, send email)
   ↓
SSH Honeypot logs activity to honeypot.log
   ↓
Spammer triggers AUTH & CMD entries
   ↓
Analyzer summarizes logs / Alert sends email


#CODE EXPLANATION (BEGINNER → ADVANCED)
server/ssh_honeypot.py
Uses Paramiko to simulate an SSH server


Accepts any password, logs all attempts and shell input


Sends fake shell responses (like "command not found")


Uses ServerInterface and Transport to handle SSH sessions



agents/*.py
Each file is a LangChain-powered tool:


honeypot_agent.py → start/stop honeypot server


analyzer_agent.py → summarize honeypot.log by IP/command


alert_agent.py → send email alerts


Uses Tool, initialize_agent, OpenAI, and AgentType.ZERO_SHOT_REACT_DESCRIPTION



main.py
FastAPI app that exposes the above tools over HTTP endpoints


Lets you control the system with curl/Postman/browser


Runs with uvicorn main:app --reload



scripts/spam_ssh.py
Uses Paramiko to run fake brute-force attacks


Loops through username/password combos


Simulates commands like uname -a to trigger logs

