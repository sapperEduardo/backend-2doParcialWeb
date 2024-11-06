from fastapi import FastAPI

from routers.alumnos import alumno
from routers.materias import materia
from routers.alumnosmaterias import alumnomateria

from db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(alumno)
app.include_router(materia)
app.include_router(alumnomateria)
