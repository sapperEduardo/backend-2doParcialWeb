from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base

class Alumno(Base):
    __tablename__ = 'alumnos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    edad = Column(Integer)

    # Relación con AlumnoMateria
    materias = relationship('AlumnoMateria', cascade="all, delete-orphan", back_populates='alumno')





class Materia(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, index=True)
    profesor = Column(String)
    promocional = Column(Boolean)

    # Relación con AlumnoMateria
    alumnos = relationship('AlumnoMateria', cascade="all, delete-orphan", back_populates='materia')





class AlumnoMateria(Base):
    __tablename__ = 'alumno_materia'

    idAlumno = Column(Integer, ForeignKey('alumnos.id', ondelete='CASCADE'), primary_key=True)
    idMateria = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'), primary_key=True)

    alumno = relationship('Alumno', back_populates='materias', passive_deletes=True)
    materia = relationship('Materia', back_populates='alumnos', passive_deletes=True)
