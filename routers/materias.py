from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from sqlalchemy import SQLColumnExpression

from db.schemas import MateriaCreate, MateriaResponse, MateriaUpdate
from db.session import get_db
from db.models import Materia 

materia = APIRouter()

# CREATE
@materia.post("/materias")
async def create_materia(
    data: MateriaCreate,
    db:Session = Depends(get_db)
):
    try:
        new_materia = Materia(
            nombre = data.nombre,
            profesor = data.profesor,
            promocional = data.promocional
        )

        db.add(new_materia)
        db.commit()

        return {'Status':'Successful'}
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e    
    

# READ LISTA
@materia.get("/materias", response_model=list[MateriaResponse])
async def get_all_materias(
    db:Session = Depends(get_db)
):
    try:
        get_materias:Materia = db.query(Materia).all()
        if not get_materias:
            raise HTTPException(status_code=404, detail='materias not Found')

        return get_materias
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e
        
# READ INDIVIDUAL
@materia.get("/materias/{id}")
async def get_one_materia(
    id:int = Path(...,),
    db:Session = Depends(get_db)
):
    try:
        get_materia:Materia = db.query(Materia).get(id)
        if not get_materia:
            raise HTTPException(status_code=404, detail='materias not Found')

        return get_materia
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e

# READ INDIVIDUAL POR NOMBRE
@materia.get("/materia/nombre/{nombre}")
async def get_materia_by_name(
    nombre: str = Path(..., description="Nombre de la materia"),
    db: Session = Depends(get_db)
):

    try:
        get_materia: Materia = db.query(Materia).filter(Materia.nombre == nombre).first()
        if not get_materia:
            raise HTTPException(status_code=404, detail="Materia not found")
        return get_materia
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar materia: {str(e)}")




# UPDATE
@materia.put("/materia/{id}")
async def update_materia(
    id:int = Path(...,),
    data:MateriaUpdate = Body(...),
    db:Session = Depends(get_db)
):
    try:
        get_materia: Materia = db.query(Materia).get(id)
        if not get_materia:
            raise HTTPException(status_code=404, detail='materia not Found')
        if data.nombre:
            get_materia.nombre = data.nombre
        if data.profesor:
            get_materia.profesor = data.profesor
        if data.promocional != None:
            get_materia.promocional = data.promocional

        db.commit()

        return {'Status':'Successful'}

    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e


# DELETE
@materia.delete("/materia/{id}")
async def delete_materia(
    id:int = Path(...,),
    db:Session = Depends(get_db)
):
    try:
        del_materia:Materia = db.query(Materia).get(id)
        if not del_materia:
            raise HTTPException(status_code=404, detail='materia not Found')
        db.delete(del_materia)
        db.commit()
        
        return {'Status':'Successful'}
    
    except SQLColumnExpression as e:
        return e
    except HTTPException as e:
        return e
    except Exception as e:
        return e
