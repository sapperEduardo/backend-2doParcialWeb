from pydantic import BaseModel, Field
from typing import Optional, List

# Esquemas para Alumnos
class AlumnoCreate(BaseModel):
    nombre: str = Field(..., max_length=50)
    apellido: str = Field(..., max_length=50)
    edad: int = Field(..., ge=0, le=120)

class AlumnoResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int

    class Config:
        orm_mode = True

class AlumnoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None





# Esquemas para Materias
class MateriaCreate(BaseModel):
    nombre: str = Field(..., max_length=50)
    profesor: str = Field(..., max_length=50)
    promocional: bool

class MateriaResponse(BaseModel):
    id: int
    nombre: str
    profesor: str
    promocional: bool

    class Config:
        orm_mode = True

class MateriaUpdate(BaseModel):
    nombre: Optional[str] = None
    profesor: Optional[str] = None
    promocional: Optional[bool] = None




# Esquema para la inscripción de Alumnos en Materias (AlumnoMateria)
class AlumnoMateriaCreate(BaseModel):
    idAlumno: int
    idMateria: int




# Esquema para verificar la inscripción de Alumnos en Materias
class MateriasDeAlumnoResponse(BaseModel):
    materia_id: int
    nombre: str
    profesor: str
    promocional: bool

    class Config:
        orm_mode = True

class AlumnosDeMateriaResponse(BaseModel):
    alumno_id: int
    nombre: str
    apellido: str
    edad: int

    class Config:
        orm_mode = True
