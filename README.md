# 🧾 Generador de Facturas

Sistema completo de generación de facturas profesionales con datos sintéticos. Utiliza **FastAPI** para el backend con datos generados por **Faker**, y un frontend moderno en **Flask** con **Tailwind CSS** que genera PDFs de alta calidad con **ReportLab**.

## Autor

- **Isabella Ramirez Franco** - [@codebell-alt](https://github.com/codebell-alt)

## Descripción del Proyecto

Este proyecto implementa un generador de facturas completo con los siguientes componentes:

### 🔧 Backend API (FastAPI)
- **Endpoint**: `GET /facturas/v1/{numero_factura}`
- **Tecnología**: FastAPI + Faker + Pydantic
- **Puerto**: 8000
- **Funcionalidad**: Genera datos sintéticos realistas para facturas españolas

### Frontend Web (Flask)
- **Tecnología**: Flask + Tailwind CSS + JavaScript
- **Puerto**: 3000
- **Funcionalidad**: Interfaz moderna que consume la API y genera PDFs

## Arquitectura

```
┌─────────────────────────┐    HTTP    ┌──────────────────────┐
│    Frontend Flask      │ ────────> │   Backend FastAPI    │
│   Puerto: 3000         │           │    Puerto: 8000      │
│ ┌─────────────────────┐ │           │ ┌──────────────────┐ │
│ │   Tailwind CSS      │ │           │ │      Faker       │ │
│ │   JavaScript        │ │           │ │    Pydantic      │ │
│ │   ReportLab PDF     │ │           │ │   Datos Sint.    │ │
│ └─────────────────────┘ │           │ └──────────────────┘ │
└─────────────────────────┘           └──────────────────────┘
```

## Estructura del Proyecto

```
lpa2-taller2/
├── docker-compose.yml          # Orquestación de servicios
├── README.md                   # Esta documentación
├── .pre-commit-config.yaml     # Configuración de pre-commit hooks
├── backend/                    # Servicio API FastAPI
│   ├── Dockerfile             # Contenedor del backend
│   └── app/
│       ├── main.py            # Aplicación FastAPI principal
│       ├── requirements.txt   # Dependencias Python backend
│       └── tests/
│           └── test_facturas.py # Tests pytest para API
└── frontend/                   # Servicio Web Flask
    ├── Dockerfile             # Contenedor del frontend
    └── app/
        ├── main.py            # Aplicación Flask principal
        ├── requirements.txt   # Dependencias Python frontend
        ├── static/
        │   ├── css/
        │   │   └── style.css  # Estilos CSS personalizados
        │   └── js/
        │       └── app.js     # JavaScript para interactividad
        └── templates/
            └── index.html     # Template HTML con Tailwind
```



### 📋 Prerrequisitos

- **Docker** (v20.10+)
- **Docker Compose** (v2.0+)
- **Git**

### 🔧 Solución de Problemas Comunes

#### Error "docker-compose command not found" en WSL 2

Si obtienes el error:
```
The command 'docker-compose' could not be found in this WSL 2 distro.
```

**Solución 1** (Recomendada): Usar Docker Compose v2
```bash
# Usar 'docker compose' (sin guión) en lugar de 'docker-compose'
docker compose up --build -d
```

**Solución 2**: Activar integración WSL en Docker Desktop
1. Abrir Docker Desktop → Settings → Resources → WSL Integration
2. Activar "Enable integration with my default WSL distro"
3. Seleccionar tu distribución WSL específica
4. Apply & Restart


1. **Clonar el repositorio**

```bash
git clone https://github.com/codebell-alt/lpa2-taller2.git
cd lpa2-taller2
```

2. **Construir y levantar los servicios**

```bash
# Construir e iniciar ambos servicios (Docker Compose v2)
docker compose up --build

# O en modo background (recomendado)
docker compose up --build -d

# Si tienes Docker Compose v1 (legacy), usar:
# docker-compose up --build -d
```

> **Nota**: Este proyecto usa **Docker Compose v2** (`docker compose` sin guión). Si estás en WSL 2, asegúrate de tener la integración de Docker Desktop activada.

3. **Verificar que los servicios estén funcionando**

```bash
# Ver logs
docker compose logs

# Ver estado de containers
docker compose ps
```

## Acceso a los Servicios

- **Frontend Web**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

## Uso del Sistema

### Backend API (FastAPI)

El backend expone un endpoint REST que genera facturas sintéticas con datos realistas:

**Endpoint Principal:** `GET /facturas/v1/{numero_factura}`

**Ejemplo de uso:**

```bash
# Generar factura con número personalizado
curl http://localhost:8000/facturas/v1/F001-2024-001

# Verificar salud del servicio
curl http://localhost:8000/health
```

**Ejemplo de respuesta JSON:**

```json
{
  "numero_factura": "F001-2024-001",
  "fecha_emision": "2024-10-15",
  "cliente_nombre": "María García Rodríguez",
  "cliente_email": "maria.garcia@email.com",
  "cliente_telefono": "+34 612 345 678",
  "cliente_direccion": "Calle de Alcalá 123, 28009 Madrid",
  "cliente_ciudad": "Madrid",
  "items": [
    {
      "descripcion": "Servicio de consultoría empresarial",
      "cantidad": 2,
      "precio_unitario": 350.00,
      "subtotal": 700.00
    }
  ],
  "subtotal": 700.00,
  "iva": 147.00,
  "total": 847.00
}
```

### Frontend Web (Flask)

La interfaz web ofrece:

1. **Formulario intuitivo** - Ingresa cualquier número de factura
2. **Vista previa** - Visualiza los datos antes de generar el PDF
3. **Descarga PDF** - Genera y descarga facturas profesionales
4. **Diseño responsive** - Funciona en desktop y móvil

## Frontend (Generador de PDF)

El frontend proporciona una interfaz web donde:

1. El usuario ingresa un número de factura
2. Se consulta el API backend
3. Se genera un PDF profesional con los datos
4. El usuario puede descargar o imprimir el PDF

### Tecnologías del Frontend

- **Flask**: Servidor web
- **Jinja2**: Motor de plantillas
- **HTML/CSS/JavaScript**: Interfaz de usuario

### Modificar el Frontend

- Editar `frontend/app/main.py` para crear la lógica de la consulta del API y generación del PDF
- Editar `frontend/app/templates/index.html` para modificar el diseño de la interfaz Web
- Editar `frontend/app/static/css/style.css` para modificar los estilos
- Editar `frontend/app/static/js/app.js` para ajustar lógica de la interfaz, si se requiere

## Configuración Avanzada

### Variables de Entorno

Puedes modificar el `docker-compose.yml` para añadir variables de entorno:

```yaml
environment:
  - API_URL=http://backend:8000
  - DEBUG=true
```

### Puertos Personalizados

Modificar en `docker-compose.yml`:

```yaml
ports:
  - "8080:3000"  # Frontend en puerto 8080
  - "9000:8000"  # Backend en puerto 9000
```

## Uso del Sistema

### Proceso Completo
1. **Abrir navegador**: http://localhost:3000
2. **Ingresar número de factura**: Cualquier formato (F001-001, FAC-2024-123, etc.)
3. **Vista previa**: Clic en "Vista Previa" para ver datos generados
4. **Generar PDF**: Clic en "Generar PDF" para descargar
5. **Descargar**: El navegador descarga automáticamente el PDF

### Ejemplos de Números de Factura
- `F001-001` - Formato simple
- `FAC-2024-001` - Con año
- `INVOICE-2024-OCT-001` - Formato detallado
- `TEST-12345` - Para pruebas

## 🐳 Comandos Docker Útiles

```bash
```bash
# Construir y levantar servicios
docker compose up --build -d

# Ver logs en tiempo real
docker compose logs -f

# Ver logs de servicio específico
docker compose logs -f backend
docker compose logs -f frontend

# Reiniciar servicios
docker compose restart

# Detener servicios
docker compose down

# Limpiar todo (containers, networks, volúmenes)
docker compose down -v --rmi all

# Ver estado de containers
docker compose ps

# Acceder a shell de container
docker compose exec backend bash
docker compose exec frontend bash
```
```

## Testing y Validación

### Tests Automatizados (Pytest)

```bash
# Ejecutar todos los tests
docker compose exec backend python -m pytest tests/ -v

# Tests con coverage detallado
docker compose exec backend python -m pytest tests/ --cov=. --cov-report=html

# Tests específicos
docker compose exec backend python -m pytest tests/test_facturas.py::test_obtener_factura_basico -v
```

### Pruebas Manuales de API

```bash
# Health check
curl http://localhost:8000/health

# Generar factura simple
curl http://localhost:8000/facturas/v1/TEST-001

# Con formato JSON legible
curl http://localhost:8000/facturas/v1/TEST-001 | python -m json.tool

# Múltiples facturas
curl http://localhost:8000/facturas/v1/F{001..005}-2024
```

### Validación Frontend

1. **Funcionalidad básica**: Navegación y formularios
2. **Vista previa AJAX**: Carga de datos sin recargar página
3. **Generación PDF**: Descarga correcta de archivos
4. **Responsive**: Prueba en diferentes tamaños de pantalla
5. **Manejo de errores**: Números de factura inválidos

## Tecnologías Utilizadas

### Backend
- **FastAPI** 0.104.1 - Framework web moderno y rápido
- **Pydantic** 2.4.2 - Validación de datos con tipos
- **Faker** 19.12.0 - Generación de datos sintéticos
- **Uvicorn** 0.24.0 - Servidor ASGI de alto rendimiento
- **Pytest** 7.4.3 - Framework de testing

### Frontend
- **Flask** 3.0.0 - Framework web minimalista
- **ReportLab** 4.0.7 - Generación de PDFs profesionales
- **Requests** 2.31.0 - Cliente HTTP para consumir API
- **Tailwind CSS** - Framework CSS utilitario moderno
- **Font Awesome** - Iconografía profesional

### DevOps & Tools
- **Docker** & **Docker Compose** - Containerización
- **Pre-commit hooks** - Calidad de código automatizada
- **Black** - Formateador de código Python
- **Ruff** - Linter Python ultrarrápido
- **isort** - Ordenamiento de imports

## Referencias y Documentación

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ReportLab User Guide](https://docs.reportlab.com/)
- [Faker Documentation](https://faker.readthedocs.io/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Contribución

1. Fork el proyecto
2. Crear una rama para la feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request


## API Documentation

La documentación interactiva de Swagger está disponible en:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)
