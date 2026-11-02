from database import SessionLocal, engine
import models
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, time

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

# 1. Crear una venta (POST /ventas)
@app.post("/ventas", status_code=status.HTTP_201_CREATED)
def crear_venta(
    id_producto: int,
    cantidad: int,
    fecha: date,
    hora: time,
    db: Session = Depends(get_db),
):
  # Verificar que el producto exista para obtener su precio
  producto = (
      db.query(models.ProductoModel)
      .filter(models.ProductoModel.id == id_producto)
      .first()
  )
  if not producto:
    raise HTTPException(status_code=404, detail="Producto no encontrado")

  # Calcular el precio total automáticamente
  precio_total = producto.precio * cantidad

  nueva_venta = models.VentaModel(
      id_producto=id_producto,
      cantidad=cantidad,
      fecha=fecha,
      hora=hora,
      precio_total=precio_total,
  )

  db.add(nueva_venta)
  db.commit()
  db.refresh(nueva_venta)
  return nueva_venta


# 2. Obtener listado de ventas (GET /ventas)
@app.get("/ventas")
def listar_ventas(db: Session = Depends(get_db)):
  ventas = db.query(models.VentaModel).all()
  return ventas


# 3. Obtener una venta por ID (GET /ventas/{id})
@app.get("/ventas/{id}")
def obtener_venta(id: int, db: Session = Depends(get_db)):
  venta = (
      db.query(models.VentaModel)
      .filter(models.VentaModel.id == id)
      .first()
  )
  if not venta:
    raise HTTPException(status_code=404, detail="Venta no encontrada")
  return venta


# 4. Eliminar una venta (DELETE /ventas/{id})
@app.delete("/ventas/{id}")
def eliminar_venta(id: int, db: Session = Depends(get_db)):
  venta = (
      db.query(models.VentaModel)
      .filter(models.VentaModel.id == id)
      .first()
  )
  if not venta:
    raise HTTPException(status_code=404, detail="Venta no encontrada")

  db.delete(venta)
  db.commit()
  return {"mensaje": f"Venta con id {id} eliminada correctamente"}