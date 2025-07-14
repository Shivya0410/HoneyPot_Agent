
cd "$(dirname "$0")/.."
python agents/honeypot_agent.py &
python agents/analyzer_agent.py &
python agents/alert_agent.py &
wait
