from datetime import date
from pydantic import BaseModel


class Usuario(BaseModel):
    Id: int
    Nombre: str
    Email: str
    Clave: str

class Alergia(BaseModel):
    Id: int
    Nombre: str

class Paciente(BaseModel):
    Id: int
    Cedula: str
    Foto: str
    Nombre: str
    Apellido: str
    TipoSangre: str
    Email: str
    Sexo: str
    FechaNacimiento: date
    Alergias: Alergia
    SignoZodiacal: str


class Consulta(BaseModel):
    PacienteId: int
    Fecha: date
    Motivo: str
    Seguro: str
    MontoPagado: float
    Diagnostico: str
    Notas: str
    Archivo: str