from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from sqlalchemy import SQLColumnExpression

from db.schemas import AlumnoMateriaCreate, AlumnoResponse, MateriaResponse
from db.session import get_db
from db.models import AlumnoMateria, Materia, Alumno

alumnomateria = APIRouter()


# CREATE
@alumnomateria.post("/alta/alumno/{idAlumno}/materia/{idMateria}")
async def create_alumnomateria(
    idAlumno: int = Path(...),
    idMateria: int = Path(...),
    db: Session = Depends(get_db)
):
    try:
        nueva_relacion = AlumnoMateria(idAlumno=idAlumno, idMateria=idMateria)
        
        db.add(nueva_relacion)
        db.commit()

        return {"Status": "Successful", "data": {"idAlumno": idAlumno, "idMateria": idMateria}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la relación: {str(e)}")  



# DELETE
@alumnomateria.delete("/baja/alumno/{idAlumno}/materia/{idMateria}")
async def delete_alumnomateria(
    idAlumno: int = Path(...),
    idMateria: int = Path(...),
    db: Session = Depends(get_db)
):
    try:
        relacion = db.query(AlumnoMateria).filter(
            AlumnoMateria.idAlumno == idAlumno,
            AlumnoMateria.idMateria == idMateria
        ).first()        
        
        if not relacion:
            raise HTTPException(status_code=404, detail="Relación no encontrada")

        db.delete(relacion)
        db.commit()

        return {"Status": "Successful", "data": {"idAlumno": idAlumno, "idMateria": idMateria}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la relación: {str(e)}")  




# METODO PARA LISTAR MATERIAS DE ALUMNO {ID}
# READ
@alumnomateria.get("/materias/alumno/{id}", response_model=list[MateriaResponse])
async def get_materias_alumno(
    id:int = Path(...,),
    db:Session = Depends(get_db)
):
    try:
        # Buscar todas las inscripciones de ese alumno en AlumnoMateria
        inscripciones = db.query(AlumnoMateria).filter(AlumnoMateria.idAlumno == id).all()

        # Obtener las materias correspondientes a cada inscripción
        materias = db.query(Materia).filter(
            Materia.id.in_([inscripcion.idMateria for inscripcion in inscripciones])
        ).all()

        # Verificar si se encontraron materias
        if not materias:
            raise HTTPException(status_code=404, detail="No se encontraron materias para el alumno especificado")

        return materias

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener materias: {str(e)}")




# METODO PARA LISTAR ALUMNOS DE UNA MATERIA {ID}
# READ
@alumnomateria.get("/alumnos/materia/{id}", response_model=list[AlumnoResponse])
async def get_alumnos_materia(
    id: int = Path(...),
    db: Session = Depends(get_db)
):
    try:
        # Buscar todas las inscripciones de esa materia en AlumnoMateria
        inscripciones = db.query(AlumnoMateria).filter(AlumnoMateria.idMateria == id).all()

        # Obtener los alumnos correspondientes a cada inscripción
        alumnos = db.query(Alumno).filter(
            Alumno.id.in_([inscripcion.idAlumno for inscripcion in inscripciones])
        ).all()

        # Verificar si se encontraron alumnos
        if not alumnos:
            raise HTTPException(status_code=404, detail="No se encontraron alumnos para la materia especificada")
            

        return alumnos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alumnos: {str(e)}")






# METODO PARA VERIFICAR SI UN ALUMNO ESTÁ INSCRITO EN UNA MATERIA
# READ
@alumnomateria.get("/inscripcion/alumno/{idAlumno}/materia/{idMateria}")
async def verificar_inscripcion(
    idAlumno: int = Path(...),
    idMateria: int = Path(...),
    db: Session = Depends(get_db)
):
    try:
        # Verificar si existe una inscripción en AlumnoMateria con los ids dados
        inscripcion = db.query(AlumnoMateria).filter(
            AlumnoMateria.idAlumno == idAlumno,
            AlumnoMateria.idMateria == idMateria
        ).first()

        # Retornar true si existe la inscripción, false si no
        return {"inscripto": inscripcion is not None}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar inscripción: {str(e)}")
