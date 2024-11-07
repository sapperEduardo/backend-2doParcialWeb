from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from sqlalchemy import SQLColumnExpression

from db.schemas import AlumnoCreate, AlumnoResponse, AlumnoUpdate
from db.session import get_db
from db.models import Alumno  

alumno = APIRouter()

# CREATE
@alumno.post("/alumnos")
async def create_alumno(
    data:AlumnoCreate,
    db:Session = Depends(get_db)
):
    try:
        new_alumno = Alumno(
            nombre = data.nombre,
            apellido = data.apellido,
            edad = data.edad,
        )

        db.add(new_alumno)
        db.commit()

        return {'Status':'Successful'}
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e




# READ LISTA
@alumno.get("/alumnos", response_model=list[AlumnoResponse])
async def get_all_alumnos(
    db:Session = Depends(get_db)
):
    try:
        get_alumnos:Alumno = db.query(Alumno).all()
        if not get_alumnos:
            raise HTTPException(status_code=404, detail='alumnos not Found')

        return get_alumnos
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e
        
# READ INDIVIDUAL
@alumno.get("/alumno/{id}")
async def get_one_alumno(
    id:int = Path(...,),
    db:Session = Depends(get_db)
):
    try:
        get_alumno: Alumno = db.query(Alumno).get(id)
        if not get_alumno:
            raise HTTPException(status_code=404, detail='alumno not Found')
        
        return get_alumno

    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e

# READ INDIVIDUAL por nombre y apellido
@alumno.get("/nombre/{nombre}/apellido/{apellido}")
async def get_alumno_by_name_and_surname(
    nombre: str = Path(..., description="Nombre del alumno"),
    apellido: str = Path(..., description="Apellido del alumno"),
    db: Session = Depends(get_db)
):

    try:
        get_alumno: Alumno = db.query(Alumno).filter(Alumno.nombre == nombre, Alumno.apellido == apellido).first()
        if not get_alumno:
            raise HTTPException(status_code=404, detail="Alumno not found")
        return get_alumno
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar alumno: {str(e)}")




# UPDATE
@alumno.put("/alumno/{id}")
async def update_alumno(
    id:int = Path(...,),
    data:AlumnoUpdate = Body(...),
    db:Session = Depends(get_db)
):
    try:
        get_alumno: Alumno = db.query(Alumno).get(id)
        if not get_alumno:
            raise HTTPException(status_code=404, detail='alumno not Found')
        
        if data.nombre:
            get_alumno.nombre = data.nombre
        if data.apellido:
            get_alumno.apellido = data.apellido
        if data.edad:
            get_alumno.edad = data.edad

        db.commit()

        return {'Status':'Successful'}

    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e


# DELETE
@alumno.delete("/alumno/{id}")
async def delete_alumno(
    id:int = Path(...,),
    db:Session = Depends(get_db)
):
    try:
        del_alumno:Alumno = db.query(Alumno).get(id)
        if not del_alumno:
            raise HTTPException(status_code=404, detail='alumno not Found')
        db.delete(del_alumno)
        db.commit()
        
        return {'Status':'Successful'}
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e
