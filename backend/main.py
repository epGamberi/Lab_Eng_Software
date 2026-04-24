from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select
import hashlib
import os

from database import engine, get_db, Base
import models
import schemas

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodLink API", version="1.0.0")

# CORS – permite o front-end (arquivo local) chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────
# Utilitários
# ─────────────────────────────────────────────────────────────
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def gerar_token(usuario_id: int, email: str) -> str:
    """Token simples (base64-like) para o escopo do projeto."""
    raw = f"{usuario_id}:{email}:foodlink_secret"
    return hashlib.sha256(raw.encode()).hexdigest()

def _seed_categorias(db: Session):
    """Popula categorias padrão se ainda não existirem."""
    if db.query(models.CategoriaAlimento).count() == 0:
        cats = [
            models.CategoriaAlimento(nome="Perecível", descricao="Itens com validade curta"),
            models.CategoriaAlimento(nome="Não-perecível", descricao="Enlatados, grãos, etc."),
            models.CategoriaAlimento(nome="Hortifrúti", descricao="Frutas, verduras e legumes"),
            models.CategoriaAlimento(nome="Padaria", descricao="Pães, bolos e similares"),
            models.CategoriaAlimento(nome="Laticínios", descricao="Leite, queijo, iogurte"),
        ]
        db.add_all(cats)
        db.commit()

# ─────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "FoodLink API rodando!", "docs": "/docs"}


# ─────────────────────────────────────────────────────────────
# Categorias
# ─────────────────────────────────────────────────────────────
@app.get("/categorias", response_model=list[schemas.CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    _seed_categorias(db)
    return db.query(models.CategoriaAlimento).all()


# ─────────────────────────────────────────────────────────────
# Autenticação
# ─────────────────────────────────────────────────────────────
@app.post("/cadastro", response_model=schemas.TokenOut, status_code=201)
def cadastrar_usuario(dados: schemas.UsuarioCadastro, db: Session = Depends(get_db)):
    _seed_categorias(db)

    # Verifica e-mail duplicado
    if db.query(models.Usuario).filter(models.Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # Cria usuário
    usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        tipo_perfil=dados.tipo_perfil.upper(),
    )
    db.add(usuario)
    db.flush()  # para obter o ID antes de commitar

    # Cria endereço vinculado
    endereco = models.Endereco(
        cep=dados.cep,
        logradouro=dados.logradouro,
        numero=dados.numero,
        bairro=dados.bairro,
        cidade=dados.cidade,
        uf=dados.uf,
        usuario_id=usuario.id_usuario,
    )
    db.add(endereco)
    db.commit()
    db.refresh(usuario)

    token = gerar_token(usuario.id_usuario, usuario.email)
    return schemas.TokenOut(
        access_token=token,
        token_type="bearer",
        usuario_id=usuario.id_usuario,
        nome=usuario.nome,
        tipo_perfil=usuario.tipo_perfil,
    )


@app.post("/login", response_model=schemas.TokenOut)
def login(dados: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email,
        models.Usuario.tipo_perfil == dados.tipo_perfil.upper(),
    ).first()

    if not usuario or usuario.senha_hash != hash_senha(dados.senha):
        raise HTTPException(status_code=401, detail="E-mail, senha ou perfil incorretos.")

    token = gerar_token(usuario.id_usuario, usuario.email)
    return schemas.TokenOut(
        access_token=token,
        token_type="bearer",
        usuario_id=usuario.id_usuario,
        nome=usuario.nome,
        tipo_perfil=usuario.tipo_perfil,
    )


# ─────────────────────────────────────────────────────────────
# Doações
# ─────────────────────────────────────────────────────────────
def _enriquecer(doacao: models.Doacao) -> dict:
    """Adiciona nome/endereço do doador e nome da categoria."""
    end = doacao.doador.endereco
    endereco_str = ""
    if end:
        endereco_str = f"{end.logradouro}, {end.numero} – {end.bairro}, {end.cidade}/{end.uf}"

    return {
        "id_doacao": doacao.id_doacao,
        "titulo": doacao.titulo,
        "quantidade": doacao.quantidade,
        "unidade_medida": doacao.unidade_medida,
        "data_vencimento": doacao.data_vencimento,
        "status": doacao.status,
        "categoria_id": doacao.categoria_id,
        "doador_id": doacao.doador_id,
        "instituicao_id": doacao.instituicao_id,
        "doador_nome": doacao.doador.nome if doacao.doador else None,
        "doador_endereco": endereco_str,
        "categoria_nome": doacao.categoria.nome if doacao.categoria else None,
    }


@app.post("/doacoes", response_model=schemas.DoacaoOut, status_code=201)
def criar_doacao(
    dados: schemas.DoacaoCriar,
    doador_id: int,
    db: Session = Depends(get_db),
):
    doador = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == doador_id,
        models.Usuario.tipo_perfil == "DOADOR",
    ).first()
    if not doador:
        raise HTTPException(status_code=404, detail="Doador não encontrado.")

    doacao = models.Doacao(
        titulo=dados.titulo,
        quantidade=dados.quantidade,
        unidade_medida=dados.unidade_medida,
        data_vencimento=dados.data_vencimento,
        categoria_id=dados.categoria_id,
        doador_id=doador_id,
        status="DISPONIVEL",
    )
    db.add(doacao)
    db.commit()
    db.refresh(doacao)
    return _enriquecer(doacao)


@app.get("/doacoes", response_model=list[schemas.DoacaoOut])
def listar_doacoes(categoria_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Doacao).filter(models.Doacao.status == "DISPONIVEL")
    if categoria_id:
        query = query.filter(models.Doacao.categoria_id == categoria_id)
    return [_enriquecer(d) for d in query.all()]


@app.get("/doacoes/usuario/{usuario_id}", response_model=list[schemas.DoacaoOut])
def listar_doacoes_usuario(usuario_id: int, db: Session = Depends(get_db)):
    doacoes = db.query(models.Doacao).filter(
        models.Doacao.doador_id == usuario_id
    ).order_by(models.Doacao.id_doacao.desc()).all()
    return [_enriquecer(d) for d in doacoes]


@app.post("/doacoes/{doacao_id}/reservar", response_model=schemas.DoacaoOut)
def reservar_doacao(doacao_id: int, instituicao_id: int, db: Session = Depends(get_db)):
    # SELECT FOR UPDATE equivalente no SQLite (lock de linha via transação)
    doacao = db.query(models.Doacao).filter(
        models.Doacao.id_doacao == doacao_id
    ).with_for_update().first()

    if not doacao:
        raise HTTPException(status_code=404, detail="Doação não encontrada.")
    if doacao.status != "DISPONIVEL":
        raise HTTPException(status_code=409, detail="Este item não está mais disponível.")

    instituicao = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == instituicao_id,
        models.Usuario.tipo_perfil == "INSTITUICAO",
    ).first()
    if not instituicao:
        raise HTTPException(status_code=404, detail="Instituição não encontrada.")

    doacao.status = "RESERVADO"
    doacao.instituicao_id = instituicao_id
    db.commit()
    db.refresh(doacao)
    return _enriquecer(doacao)


@app.post("/doacoes/{doacao_id}/entregar", response_model=schemas.DoacaoOut)
def confirmar_entrega(doacao_id: int, doador_id: int, db: Session = Depends(get_db)):
    doacao = db.query(models.Doacao).filter(
        models.Doacao.id_doacao == doacao_id,
        models.Doacao.doador_id == doador_id,
    ).first()
    if not doacao:
        raise HTTPException(status_code=404, detail="Doação não encontrada.")
    if doacao.status != "RESERVADO":
        raise HTTPException(status_code=400, detail="Só é possível confirmar entrega de itens reservados.")

    doacao.status = "ENTREGUE"
    db.commit()
    db.refresh(doacao)
    return _enriquecer(doacao)


@app.post("/doacoes/{doacao_id}/cancelar", response_model=schemas.DoacaoOut)
def cancelar_doacao(doacao_id: int, usuario_id: int, db: Session = Depends(get_db)):
    doacao = db.query(models.Doacao).filter(
        models.Doacao.id_doacao == doacao_id
    ).first()
    if not doacao:
        raise HTTPException(status_code=404, detail="Doação não encontrada.")
    if doacao.status == "ENTREGUE":
        raise HTTPException(status_code=400, detail="Não é possível cancelar uma doação já entregue.")

    # Se instituição cancela reserva → volta a DISPONIVEL
    if doacao.instituicao_id == usuario_id and doacao.status == "RESERVADO":
        doacao.status = "DISPONIVEL"
        doacao.instituicao_id = None
    elif doacao.doador_id == usuario_id:
        doacao.status = "CANCELADO"
    else:
        raise HTTPException(status_code=403, detail="Sem permissão para cancelar esta doação.")

    db.commit()
    db.refresh(doacao)
    return _enriquecer(doacao)
