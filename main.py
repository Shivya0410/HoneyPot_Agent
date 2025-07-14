# main.py
from fastapi import FastAPI
from agents.honeypot_agent import start_honeypot, stop_honeypot
from agents.analyzer_agent import analyze_logs
from agents.alert_agent import send_email

app = FastAPI(title="SSH Honeypot Agent API")

@app.get("/")
async def root():
    return {"message": "🔒 SSH Honeypot Agent running"}

@app.post("/honeypot/start")
async def api_start_honeypot():
    result = start_honeypot("")   # calls your tool
    return {"status": result}

@app.post("/honeypot/stop")
async def api_stop_honeypot():
    result = stop_honeypot("")
    return {"status": result}

@app.get("/logs/summary")
async def api_analyze_logs():
    report = analyze_logs("")
    return {"report": report}

@app.post("/alert")
async def api_send_alert(message: str):
    result = send_email(message)
    return {"status": result}
