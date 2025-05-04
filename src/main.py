from fastapi import FastAPI, HTTPException
from agents.states import ChatRequest
from agents.service import chatbot_output

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = await chatbot_output(request.session_id, request.user_message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)