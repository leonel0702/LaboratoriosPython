from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from database import Base


class ProductoModel(Base):
  __tablename__ = "productos"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  nombre = Column(String, nullable=False)
  precio = Column(Float, nullable=False)


class VentaModel(Base):
  __tablename__ = "ventas"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  fecha = Column(Date, nullable=False)
  hora = Column(Time, nullable=False)
  id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
  cantidad = Column(Integer, nullable=False)
  precio_total = Column(Float, nullable=False)

  # Relación para poder mostrar los datos del producto en los endpoints de ventas
  producto = relationship("ProductoModel")