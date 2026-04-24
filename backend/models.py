from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class TipoPerfil(str, enum.Enum):
    DOADOR = "DOADOR"
    INSTITUICAO = "INSTITUICAO"


class StatusDoacao(str, enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    RESERVADO = "RESERVADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    tipo_perfil = Column(String, nullable=False)  # DOADOR ou INSTITUICAO
    data_cadastro = Column(DateTime, default=func.now())

    endereco = relationship("Endereco", back_populates="usuario", uselist=False, cascade="all, delete")
    doacoes = relationship("Doacao", foreign_keys="Doacao.doador_id", back_populates="doador")
    reservas = relationship("Doacao", foreign_keys="Doacao.instituicao_id", back_populates="instituicao")


class Endereco(Base):
    __tablename__ = "enderecos"

    id_endereco = Column(Integer, primary_key=True, index=True)
    cep = Column(String)
    logradouro = Column(String)
    numero = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    uf = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True)

    usuario = relationship("Usuario", back_populates="endereco")


class CategoriaAlimento(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)

    doacoes = relationship("Doacao", back_populates="categoria")


class Doacao(Base):
    __tablename__ = "doacoes"

    id_doacao = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    quantidade = Column(Float, nullable=False)
    unidade_medida = Column(String, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    status = Column(String, default="DISPONIVEL")
    doador_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=False)
    instituicao_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    doador = relationship("Usuario", foreign_keys=[doador_id], back_populates="doacoes")
    instituicao = relationship("Usuario", foreign_keys=[instituicao_id], back_populates="reservas")
    categoria = relationship("CategoriaAlimento", back_populates="doacoes")
