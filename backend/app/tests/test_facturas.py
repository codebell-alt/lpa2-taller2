import pytest
from fastapi.testclient import TestClient
from datetime import date
import json

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Generador de Facturas v1.0"}


def test_health_check():
    """Test del endpoint de salud"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_obtener_factura_basico():
    """Test básico del endpoint de factura"""
    numero_factura = "F001-001"
    response = client.get(f"/facturas/v1/{numero_factura}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Validar estructura básica
    assert data["numero_factura"] == numero_factura
    assert "fecha_emision" in data
    assert "cliente_nombre" in data
    assert "cliente_email" in data
    assert "items" in data
    assert "subtotal" in data
    assert "iva" in data
    assert "total" in data


def test_factura_schema_completo():
    """Test del schema completo de la factura"""
    response = client.get("/facturas/v1/F002-001")
    
    assert response.status_code == 200
    data = response.json()
    
    # Validar todos los campos requeridos
    required_fields = [
        "numero_factura", "fecha_emision", "cliente_nombre", 
        "cliente_email", "cliente_telefono", "cliente_direccion", 
        "cliente_ciudad", "items", "subtotal", "iva", "total"
    ]
    
    for field in required_fields:
        assert field in data, f"Campo {field} faltante en la respuesta"
    
    # Validar tipos de datos
    assert isinstance(data["numero_factura"], str)
    assert isinstance(data["cliente_nombre"], str)
    assert isinstance(data["items"], list)
    assert isinstance(data["subtotal"], (int, float))
    assert isinstance(data["iva"], (int, float))
    assert isinstance(data["total"], (int, float))
    
    # Validar que hay al menos un item
    assert len(data["items"]) > 0
    
    # Validar estructura de items
    item = data["items"][0]
    item_fields = ["descripcion", "cantidad", "precio_unitario", "subtotal"]
    for field in item_fields:
        assert field in item, f"Campo {field} faltante en item"


def test_calculo_matematico():
    """Test que verifica los cálculos matemáticos"""
    response = client.get("/facturas/v1/F003-001")
    
    assert response.status_code == 200
    data = response.json()
    
    # Calcular subtotal basado en items
    subtotal_calculado = sum(item["subtotal"] for item in data["items"])
    
    # Verificar subtotal (con tolerancia por redondeo)
    assert abs(data["subtotal"] - subtotal_calculado) < 0.01
    
    # Verificar IVA (21%)
    iva_esperado = round(data["subtotal"] * 0.21, 2)
    assert abs(data["iva"] - iva_esperado) < 0.01
    
    # Verificar total
    total_esperado = round(data["subtotal"] + data["iva"], 2)
    assert abs(data["total"] - total_esperado) < 0.01


def test_diferentes_numeros_factura():
    """Test con diferentes números de factura"""
    numeros = ["F001-001", "F999-999", "ABC-123", "test-factura"]
    
    for numero in numeros:
        response = client.get(f"/facturas/v1/{numero}")
        assert response.status_code == 200
        data = response.json()
        assert data["numero_factura"] == numero


def test_factura_validacion_fecha():
    """Test que valida el formato de fecha"""
    response = client.get("/facturas/v1/F004-001")
    
    assert response.status_code == 200
    data = response.json()
    
    # Validar que la fecha está en formato correcto
    fecha_str = data["fecha_emision"]
    try:
        date.fromisoformat(fecha_str)
    except ValueError:
        pytest.fail(f"Fecha inválida: {fecha_str}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])