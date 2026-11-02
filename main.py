from database import SessionLocal, engine
import models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Laboratorio - Ventas UNLa 2026", version="1.0"
)  #[cite: 1, 3]



def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
# 1. Crear un producto (POST /productos)
@app.post("/productos", status_code=status.HTTP_201_CREATED)
def crear_producto(nombre: str, precio: float, db: Session = Depends(get_db)):
  nuevo_producto = models.ProductoModel(nombre=nombre, precio=precio)
  db.add(nuevo_producto)
  db.commit()
  db.refresh(nuevo_producto)
  return nuevo_producto


# 2. Obtener listado de productos (GET /productos)
@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
  productos = db.query(models.ProductoModel).all()
  return productos


# 3. Obtener un producto por ID (GET /productos/{id})
@app.get("/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
  producto = (
      db.query(models.ProductoModel).filter(models.ProductoModel.id == id).first()
  )
  if not producto:
    raise HTTPException(status_code=404, detail="Producto no encontrado")
  return producto


# 4. Actualizar un producto (PUT /productos/{id})
@app.put("/productos/{id}")
def actualizar_producto(
    id: int, nombre: str, precio: float, db: Session = Depends(get_db)
):
  producto = (
      db.query(models.ProductoModel).filter(models.ProductoModel.id == id).first()
  )
  if not producto:
    raise HTTPException(status_code=404, detail="Producto no encontrado")

  producto.nombre = nombre
  producto.precio = precio
  db.commit()
  db.refresh(producto)
  return producto


# 5. Eliminar un producto (DELETE /productos/{id})
@app.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
  producto = (
      db.query(models.ProductoModel).filter(models.ProductoModel.id == id).first()
  )
  if not producto:
    raise HTTPException(status_code=404, detail="Producto no encontrado")

  db.delete(producto)
  db.commit()
  return {"mensaje": f"Producto con id {id} eliminado correctamente"}