from fastapi import FastAPI
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.controllers import (
    alunos_controller,
    escola_controller,
    matricula_controller,
    professores_controller,
)


app = FastAPI(
    title="Trabalho Trio",
    description="Escola de idiomas",
    version="0.1.0"
)

app.include_router(matricula_controller.router)
app.include_router(escola_controller.router)
app.include_router(alunos_controller.router)
app.include_router(professores_controller.router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)
    
    