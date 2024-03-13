from fastapi import FastAPI
from fastapi.responses import JSONResponse
from iniya import process_command

app = FastAPI()

@app.post("/process-command")
async def process_command_endpoint(command: str):
    try:
        process_command(command)
        return JSONResponse(content={"message": "Command processed successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
