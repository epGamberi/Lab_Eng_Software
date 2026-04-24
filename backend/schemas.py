from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


# ── Endereço ──────────────────────────────────────────────
class EnderecoBase(BaseModel):
    cep: str
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    uf: str

class EnderecoOut(EnderecoBase):
    id_endereco: int
    class Config:
        from_attributes = True


# ── Usuário ───────────────────────────────────────────────
class UsuarioCadastro(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_perfil: str          # "DOADOR" ou "INSTITUICAO"
    cep: str
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    uf: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str
    tipo_perfil: str

class UsuarioOut(BaseModel):
    id_usuario: int
    nome: str
    email: str
    tipo_perfil: str
    data_cadastro: Optional[datetime]
    endereco: Optional[EnderecoOut]
    class Config:
        from_attributes = True


# ── Categoria ─────────────────────────────────────────────
class CategoriaOut(BaseModel):
    id_categoria: int
    nome: str
    descricao: Optional[str]
    class Config:
        from_attributes = True


# ── Doação ────────────────────────────────────────────────
class DoacaoCriar(BaseModel):
    titulo: str
    quantidade: float
    unidade_medida: str
    data_vencimento: date
    categoria_id: int

class DoacaoOut(BaseModel):
    id_doacao: int
    titulo: str
    quantidade: float
    unidade_medida: str
    data_vencimento: date
    status: str
    categoria_id: int
    doador_id: int
    instituicao_id: Optional[int]
    doador_nome: Optional[str] = None
    doador_endereco: Optional[str] = None
    categoria_nome: Optional[str] = None
    class Config:
        from_attributes = True


# ── Auth ──────────────────────────────────────────────────
class TokenOut(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int
    nome: str
    tipo_perfil: str
