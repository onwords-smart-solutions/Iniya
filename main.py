from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from firebase_admin import auth
import uvicorn
from firebase import authenticate_user
from iniya import process_command

app = FastAPI()

user = None

@app.post('/login')
async def login(email: str):
    global user
    user = authenticate_user(email)
    return {"uid": user['localId']}  
    
@app.post("/process-command")
async def process_command_endpoint(command: str):
    global user
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    try:
        owner_id = user['localId']
        process_command(command,owner_id)
        
        return JSONResponse(content={"message": f"Command '{command}' processed successfully for user with UID '{owner_id}'"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)