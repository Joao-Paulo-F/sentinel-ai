from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    nome: str
    email: str
    tipo_usuario: str
    status: str = "ATIVO"


@dataclass
class Dispositivo:
    id_usuario: int
    identificador: str
    sistema_operacional: Optional[str] = None
    navegador: Optional[str] = None


@dataclass
class Acesso:
    id_usuario: int
    id_dispositivo: Optional[int]
    ip_origem: str
    pais: Optional[str]
    cidade: Optional[str]
    resultado: str