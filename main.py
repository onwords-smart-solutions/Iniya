from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from iniya import process_command

app = FastAPI(docs_url="/")
    
@app.post("/process-command")
async def process_command_endpoint(command: str, uid : str):
    try:
        process_command(command,uid)
        return JSONResponse(content={"message": f"Command {command}"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)