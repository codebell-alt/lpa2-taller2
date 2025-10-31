from datetime import date, datetime
from typing import List

import uvicorn
from faker import Faker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Generador de Facturas API", version="1.0.0")
fake = Faker("es_ES")  # Faker en español


class ItemFactura(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class Factura(BaseModel):
    numero_factura: str
    fecha_emision: date
    cliente_nombre: str
    cliente_email: str
    cliente_telefono: str
    cliente_direccion: str
    cliente_ciudad: str
    items: List[ItemFactura]
    subtotal: float
    iva: float
    total: float


@app.get("/")
async def root():
    return {"message": "API Generador de Facturas v1.0"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now()}


@app.get("/facturas/v1/{numero_factura}", response_model=Factura)
async def obtener_factura(numero_factura: str):
    """
    Genera una factura sintética usando Faker
    """
    try:
        # Generar items aleatorios
        items = []
        num_items = fake.random_int(min=1, max=5)
        subtotal = 0.0

        for _ in range(num_items):
            cantidad = fake.random_int(min=1, max=10)
            precio_unitario = round(fake.random.uniform(10.0, 500.0), 2)
            item_subtotal = round(cantidad * precio_unitario, 2)
            subtotal += item_subtotal

            items.append(
                ItemFactura(
                    descripcion=fake.catch_phrase(),
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=item_subtotal,
                )
            )

        # Calcular totales
        iva = round(subtotal * 0.21, 2)  # IVA 21%
        total = round(subtotal + iva, 2)

        # Crear factura
        factura = Factura(
            numero_factura=numero_factura,
            fecha_emision=fake.date_between(start_date="-30d", end_date="today"),
            cliente_nombre=fake.name(),
            cliente_email=fake.email(),
            cliente_telefono=fake.phone_number(),
            cliente_direccion=fake.address(),
            cliente_ciudad=fake.city(),
            items=items,
            subtotal=subtotal,
            iva=iva,
            total=total,
        )

        return factura

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generando factura: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
