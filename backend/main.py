import os
import sys
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

sys.path.append('/Quantarion_AI/backend')
from quantum_engine import quantum_core
from file_manager import file_engine
from agent_builder import agent_builder

app = FastAPI(title="Quantarion AI Master Engine")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    frontend_path = "/Quantarion_AI/frontend/index.html"
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Quantarion AI Frontend Error: index.html not found!</h1>"

@app.post("/api/chat")
async def handle_chat(request: ChatRequest):
    user_message = request.message.strip()
    
    # Trigger Auto Code Generator if user asks to make an app
    if "make" in user_message.lower() or "build" in user_message.lower() or "banao" in user_message.lower():
        result = await agent_builder.build_app_from_idea(user_message)
        return {"reply": f"🤖 [AGENT ACTIVE]: {result}\n\nNow you can compile this generated app folder using Buildozer into a real APK!"}

    if "+" in user_message or " and " in user_message.lower() or " मिला " in user_message:
        delimiters = ["+", " and ", " मिला ", "और"]
        items = [user_message]
        for delimiter in delimiters:
            if delimiter in items[0]:
                items = items[0].split(delimiter)
                break
        if len(items) >= 2:
            item1 = items[0].strip()
            item2 = items[1].strip()
            sim_result = await quantum_core.simulate_chemical_reaction(item1, item2)
            reply_text = (
                f"🧪 【QUANTUM REACTION ANALYSIS】\n\n"
                f"🔹 Item 1: {item1}\n"
                f"🔹 Item 2: {item2}\n"
                f"➔ Combined Result: {sim_result['combined_result']}\n"
                f"🔥 Energy Profile: {sim_result['energy_profile']}\n\n"
                f"🔬 Scientific Analysis: {sim_result['scientific_analysis']}"
            )
            return {"reply": reply_text}

    quantum_response = await quantum_core.execute_quantum_logic(user_message)
    return {"reply": f"Quantarion AI Core: Simulation successful.\n\n[Output]: {quantum_response}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
