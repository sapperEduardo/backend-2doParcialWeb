from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.alumnos import alumno
from routers.materias import materia
from routers.alumnosmaterias import alumnomateria

from db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Lista de orígenes permitidos
origins = [
    "http://127.0.0.1:5500",  # Permite tu origen de desarrollo
    "http://localhost:5500",  # Alternativa por si usas localhost
    # Añade otros orígenes si los necesitas
]

# Configura el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Permitir los orígenes especificados
    allow_credentials=True,            # Permitir el uso de cookies
    allow_methods=["*"],               # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],               # Permitir todos los encabezados
)

@app.get("/")
def read_root():
    return {"message": "¡La API está activa y funcionando!"}


app.include_router(alumno)
app.include_router(materia)
app.include_router(alumnomateria)
