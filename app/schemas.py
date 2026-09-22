from pydantic import BaseModel, Field
from typing import Optional


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=150)
    tipo_usuario: str = Field(min_length=2, max_length=30)


class DispositivoCreate(BaseModel):
    id_usuario: int
    identificador: str
    sistema_operacional: Optional[str] = None
    navegador: Optional[str] = None


class LoginRequest(BaseModel):
    id_usuario: int
    id_dispositivo: Optional[int] = None
    ip_origem: str
    pais: str
    cidade: Optional[str] = None
    horario: str
    conhecido_ip: bool = False
    conhecido_dispositivo: bool = False