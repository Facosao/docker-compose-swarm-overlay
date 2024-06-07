from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/micro_servico")
async def root():
    #subprocess.run(["python", "script_requerido.py"])
    return {"message": "rodou o microserviço com sucesso!"}
