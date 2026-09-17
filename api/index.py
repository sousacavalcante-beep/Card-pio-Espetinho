import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "/tmp/database.db" if os.environ.get("VERCEL") else "./api/database.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EspetinhoModel(Base):
    __tablename__ = "espetinhos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    imagem = Column(String)

Base.metadata.create_engine(bind=engine)

app = FastAPI()

class EspetinhoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    imagem: str

@app.get("/api/espetinhos")
def listar_espetinhos():
    db = SessionLocal()
    itens = db.query(EspetinhoModel).all()
    db.close()
    return itens

@app.post("/api/espetinhos")
def criar_espetinho(item: EspetinhoCreate):
    db = SessionLocal()
    novo = EspetinhoModel(
        nome=item.nome,
        descricao=item.descricao,
        preco=item.preco,
        imagem=item.imagem
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    db.close()
    return novo
