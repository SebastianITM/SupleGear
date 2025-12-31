# SupleGear Backend - Clean Architecture FastAPI

> E-commerce backend para venta de suplementos deportivos desarrollado con **FastAPI**, **SQLAlchemy**, y **Clean Architecture**.

## 📋 Tabla de Contenidos

- [Visión General](#-visión-general)
- [Arquitectura](#-arquitectura)
- [Estructura de Carpetas](#-estructura-de-carpetas)
- [Flujo de Peticiones](#-flujo-de-peticiones)
- [Módulos del E-commerce](#-módulos-del-e-commerce)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Ejemplo Práctico: Crear Producto](#-ejemplo-práctico-crear-producto)
- [Buenas Prácticas](#-buenas-prácticas)
- [Escalabilidad](#-escalabilidad)
- [Testing](#-testing)
- [Deployment](#-deployment)

---

## 🎯 Visión General

**SupleGear Backend** es una API RESTful profesional construida siguiendo los principios de **Clean Architecture** y **SOLID**. El proyecto está diseñado para ser:

- ✅ **Escalable**: Estructura modular preparada para crecimiento
- ✅ **Mantenible**: Separación clara de responsabilidades
- ✅ **Testeable**: Altamente testeable con inyección de dependencias
- ✅ **Segura**: Autenticación JWT y autorización por roles
- ✅ **Producción-Ready**: Configuración profesional con Docker

**Stack Tecnológico:**
- **Framework**: FastAPI 0.104+
- **Base de Datos**: PostgreSQL + SQLAlchemy ORM
- **Autenticación**: JWT (JSON Web Tokens)
- **Validación**: Pydantic v2
- **Servidor**: Uvicorn
- **Contenedorización**: Docker + Docker Compose

---

## 🏗️ Arquitectura

### Clean Architecture: Las 4 Capas

```
┌─────────────────────────────────────────────────────────┐
│                   API / CONTROLLERS                      │
│            (FastAPI Routers & Endpoints)                │
├─────────────────────────────────────────────────────────┤
│                    APPLICATION                           │
│              (Use Cases / Business Logic)                │
├─────────────────────────────────────────────────────────┤
│                     DOMAIN                               │
│          (Entities / Business Rules / Interfaces)        │
├─────────────────────────────────────────────────────────┤
│                INFRASTRUCTURE                            │
│      (Database / Repositories / External Services)       │
└─────────────────────────────────────────────────────────┘
```

### Principios Implementados

#### 1. **Dependency Inversion**
   - Capas superiores no dependen de inferiores
   - Las dependencias apuntan hacia el core (domain)

#### 2. **Single Responsibility Principle**
   - Cada clase tiene una única responsabilidad
   - Separación clara entre capas

#### 3. **Open/Closed Principle**
   - Código abierto a extensión, cerrado a modificación
   - BaseRepository permite extender sin modificar

#### 4. **Liskov Substitution**
   - Interfaces consistentes
   - Repositorios intercambiables

#### 5. **Interface Segregation**
   - Clientes no dependen de métodos que no usan
   - DTOs específicos por caso de uso

---

## 📁 Estructura de Carpetas

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # Factory y configuración FastAPI
│   │
│   ├── core/                      # Configuración y utilidades core
│   │   ├── config.py             # Settings (pydantic-settings)
│   │   ├── security.py           # JWT, hash de contraseñas
│   │   └── constants.py          # Constantes y enums
│   │
│   ├── domain/                    # CAPA DE DOMINIO - Lógica de negocio pura
│   │   ├── users/
│   │   │   └── entities.py       # Reglas de dominio de usuarios
│   │   ├── products/
│   │   │   └── entities.py       # Reglas de dominio de productos
│   │   ├── categories/
│   │   │   └── entities.py       # Reglas de dominio de categorías
│   │   ├── orders/
│   │   │   └── entities.py       # Reglas de dominio de pedidos
│   │   ├── coupons/
│   │   │   └── entities.py       # Reglas de dominio de cupones
│   │   ├── payments/
│   │   │   └── entities.py       # Reglas de dominio de pagos
│   │   └── roles/
│   │       └── entities.py       # Roles y permisos
│   │
│   ├── application/               # CAPA DE APLICACIÓN - Casos de uso
│   │   ├── users/
│   │   │   ├── create_user.py    # Use cases de usuarios
│   │   │   ├── update_user.py
│   │   │   └── delete_user.py
│   │   ├── products/
│   │   │   ├── create_product.py # Use cases de productos
│   │   │   ├── update_product.py
│   │   │   └── list_products.py
│   │   ├── categories/
│   │   │   └── ...               # Use cases de categorías
│   │   ├── orders/
│   │   │   └── ...               # Use cases de pedidos
│   │   ├── coupons/
│   │   │   └── ...               # Use cases de cupones
│   │   ├── payments/
│   │   │   └── ...               # Use cases de pagos
│   │   └── auth/
│   │       ├── login.py          # Login y refresh token
│   │       └── register.py       # Registro de usuarios
│   │
│   ├── infrastructure/            # CAPA DE INFRAESTRUCTURA - Implementaciones técnicas
│   │   ├── database/
│   │   │   ├── database.py       # Configuración DB y SessionLocal
│   │   │   ├── models_user.py    # ORM models
│   │   │   ├── models_product.py
│   │   │   ├── models_order.py
│   │   │   └── models_coupon.py
│   │   ├── repositories/
│   │   │   ├── base_repository.py # Base CRUD genérica
│   │   │   ├── user_repository.py # Queries específicas de usuarios
│   │   │   ├── product_repository.py
│   │   │   ├── order_repository.py
│   │   │   └── coupon_repository.py
│   │   ├── services/
│   │   │   ├── email_service.py  # Envío de emails
│   │   │   ├── sms_service.py    # Envío de SMS
│   │   │   └── notification_service.py
│   │   └── external/
│   │       ├── stripe_service.py # Integración Stripe
│   │       ├── paypal_service.py # Integración PayPal
│   │       └── twilio_service.py # SMS
│   │
│   ├── api/                       # CAPA DE PRESENTACIÓN - HTTP
│   │   ├── v1/
│   │   │   ├── router.py         # Router principal v1
│   │   │   ├── dependencies.py   # Inyección de dependencias (JWT, roles)
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py       # POST /auth/login
│   │   │   │   ├── users.py      # CRUD usuarios
│   │   │   │   ├── products.py   # CRUD productos
│   │   │   │   ├── categories.py
│   │   │   │   ├── orders.py
│   │   │   │   ├── coupons.py
│   │   │   │   └── payments.py
│   │   │   └── middleware/
│   │   │       ├── auth_middleware.py
│   │   │       └── error_handler.py
│   │   └── v2/                   # Versiones futuras
│   │
│   ├── schemas/                   # DTOs con Pydantic
│   │   ├── user_schemas.py       # UserCreate, UserResponse, etc
│   │   ├── product_schemas.py
│   │   ├── auth_schemas.py
│   │   └── common_schemas.py     # Schemas compartidos
│   │
│   └── utils/
│       ├── helpers.py            # Funciones auxiliares
│       └── exceptions.py         # Excepciones personalizadas
│
├── tests/
│   ├── unit/
│   │   ├── test_products.py      # Tests unitarios
│   │   ├── test_users.py
│   │   └── test_auth.py
│   └── integration/
│       ├── test_product_flow.py  # Tests de integración
│       └── test_order_flow.py
│
├── main.py                        # Punto de entrada
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Contenedor
├── docker-compose.yml             # Orquestación
├── .env.example                   # Variables de entorno ejemplo
├── .env                          # Variables (NO en git)
├── .gitignore
├── conftest.py                   # Configuración pytest
└── README.md
```

---

## 🔄 Flujo de Peticiones

### Ejemplo: Crear un Producto

```
┌──────────────┐
│   Cliente    │
│  (React SPA) │
└──────┬───────┘
       │ POST /api/v1/products
       │ {name, price, sku, category_id, ...}
       ↓
┌──────────────────────────────────────────────────────────┐
│ 1. API LAYER - FastAPI Router                            │
│    └─ Validación básica (401, 403)                       │
│    └─ Dependency Injection (get_current_vendor)          │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────┐
│ 2. APPLICATION LAYER - Use Case                          │
│    CreateProductUseCase                                  │
│    ├─ Validar que categoría existe                       │
│    ├─ Validar que SKU es único                           │
│    ├─ Llamar a repository.create()                       │
│    └─ Retornar ProductResponse                           │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────┐
│ 3. DOMAIN LAYER - Entidades y Reglas                     │
│    ├─ Product entity (con validaciones)                  │
│    ├─ Category entity                                    │
│    └─ Reglas de negocio                                  │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────┐
│ 4. INFRASTRUCTURE LAYER                                  │
│    ├─ ProductRepository.create()                         │
│    ├─ CategoryRepository.get_by_id()                     │
│    ├─ SQLAlchemy ORM                                     │
│    └─ PostgreSQL                                         │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────────────────┐
│ Respuesta HTTP 201                                       │
│ {                                                        │
│   "id": 1,                                               │
│   "name": "Whey Protein",                                │
│   "price": 99.99,                                        │
│   "sku": "WHEY-001",                                     │
│   "status": "active",                                    │
│   "created_at": "2024-01-15T10:30:00Z"                   │
│ }                                                        │
└──────────────────────────────────────────────────────────┘
```

### Flujo de Autenticación

```
POST /api/v1/auth/login
├─ Recibir {email, password}
├─ LoginUseCase.execute()
│  ├─ UserRepository.get_by_email()
│  ├─ verify_password()
│  ├─ create_access_token() → JWT válido 30 min
│  └─ create_refresh_token() → JWT válido 7 días
└─ Respuesta: {access_token, refresh_token, token_type}

Peticiones subsecuentes:
POST /api/v1/products
├─ Header: Authorization: "Bearer {access_token}"
├─ Dependency: get_current_vendor()
│  ├─ Extraer token del header
│  ├─ decode_token() → payload
│  ├─ Verificar user_id existe en DB
│  ├─ Verificar role (vendor/admin)
│  └─ Inyectar current_user en endpoint
└─ Endpoint puede acceder a current_user
```

---

## 🛒 Módulos del E-commerce

### 1. **USUARIOS** (`app/domain/users/` + `app/application/users/`)
   - **Entidades**: User (id, email, username, role, is_active)
   - **Casos de uso**: Crear, leer, actualizar, eliminar usuarios
   - **Repositorio**: UserRepository (búsqueda por email, username, etc)
   - **Endpoints**:
     ```
     POST   /api/v1/users           # Crear usuario
     GET    /api/v1/users/{id}      # Obtener usuario
     PUT    /api/v1/users/{id}      # Actualizar usuario
     DELETE /api/v1/users/{id}      # Eliminar usuario (admin)
     GET    /api/v1/users/search    # Buscar usuarios (admin)
     ```

### 2. **AUTENTICACIÓN** (`app/application/auth/`)
   - **Casos de uso**: Login, refresh token, logout
   - **JWT**: HS256, 30min acceso, 7d refresh
   - **Endpoints**:
     ```
     POST /api/v1/auth/login         # Login
     POST /api/v1/auth/refresh       # Refresh token
     POST /api/v1/auth/logout        # Logout
     ```

### 3. **PRODUCTOS** (`app/domain/products/` + `app/application/products/`)
   - **Entidades**: Product (id, name, sku, price, stock, status, category_id)
   - **Casos de uso**: CRUD, búsqueda, stock bajo
   - **Repositorio**: ProductRepository (búsqueda por SKU, categoría, etc)
   - **Endpoints**:
     ```
     POST   /api/v1/products              # Crear (vendor/admin)
     GET    /api/v1/products              # Listar activos
     GET    /api/v1/products/{id}         # Obtener
     PUT    /api/v1/products/{id}         # Actualizar (vendor/admin)
     DELETE /api/v1/products/{id}         # Eliminar (admin)
     GET    /api/v1/products/search       # Buscar
     ```

### 4. **CATEGORÍAS** (`app/domain/categories/`)
   - **Entidades**: Category (id, name, description, icon)
   - **Casos de uso**: CRUD categorías
   - **Endpoints**:
     ```
     POST   /api/v1/categories       # Crear (admin)
     GET    /api/v1/categories       # Listar
     GET    /api/v1/categories/{id}  # Obtener
     PUT    /api/v1/categories/{id}  # Actualizar (admin)
     ```

### 5. **ÓRDENES** (`app/domain/orders/` + `app/application/orders/`)
   - **Entidades**: Order, OrderItem
   - **Estados**: pending → confirmed → processing → shipped → delivered/cancelled
   - **Casos de uso**: Crear orden, actualizar estado, cancelar
   - **Endpoints**:
     ```
     POST   /api/v1/orders              # Crear orden
     GET    /api/v1/orders/{id}         # Obtener detalle
     PUT    /api/v1/orders/{id}         # Actualizar
     GET    /api/v1/orders              # Mis órdenes
     ```

### 6. **PAGOS** (`app/domain/payments/` + `app/infrastructure/external/`)
   - **Integraciones**: Stripe, PayPal
   - **Estados**: pending, completed, failed, refunded
   - **Casos de uso**: Procesar pago, webhook
   - **Endpoints**:
     ```
     POST   /api/v1/payments/process     # Procesar pago
     POST   /api/v1/payments/webhook     # Webhook Stripe
     GET    /api/v1/payments/{id}        # Estado de pago
     ```

### 7. **CUPONES** (`app/domain/coupons/` + `app/application/coupons/`)
   - **Entidades**: Coupon (code, discount, max_uses, valid_from/until)
   - **Casos de uso**: Validar cupón, aplicar descuento
   - **Repositorio**: CouponRepository (validación compleja)
   - **Endpoints**:
     ```
     POST   /api/v1/coupons              # Crear (admin)
     POST   /api/v1/coupons/validate     # Validar código
     GET    /api/v1/coupons              # Listar activos
     ```

### 8. **ROLES Y PERMISOS** (`app/domain/roles/`)
   - **Roles**: ADMIN, VENDOR, CUSTOMER
   - **Control**: Decoradores/dependencias en endpoints
   - **Ejemplo**:
     ```python
     @router.post("/products")
     async def create_product(
         product: ProductCreate,
         current_user: dict = Depends(get_current_vendor)  # Solo vendor/admin
     ):
         ...
     ```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.11+
- PostgreSQL 13+
- Docker & Docker Compose (opcional)
- Git

### Opción 1: Instalación Local

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd backend

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 5. Crear base de datos
createdb -U postgres suplegear

# 6. Ejecutar migraciones (si existen)
alembic upgrade head

# 7. Ejecutar servidor
python main.py
```

**URL Accesible en:** `http://localhost:8000`
- **API Docs**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`

### Opción 2: Con Docker Compose (Recomendado)

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd backend

# 2. Configurar .env
cp .env.example .env

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar salud
curl http://localhost:8000/health
```

**Servicios disponibles:**
- **Backend API**: `http://localhost:8000`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

---

## 📖 Uso

### Autenticación: Obtener Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'

# Respuesta:
# {
#   "access_token": "eyJhbGc...",
#   "refresh_token": "eyJhbGc...",
#   "token_type": "bearer"
# }
```

### Usar Token en Peticiones

```bash
curl -X GET "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer {access_token}"
```

### Crear Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "SecurePass123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

---

## 💡 Ejemplo Práctico: Crear Producto

### 1️⃣ Vista General

Para crear un producto, seguiremos el flujo de Clean Architecture:

```
Petición HTTP → API Router → Use Case → Repository → Database
```

### 2️⃣ Endpoint (API Layer)

```python
# app/api/v1/endpoints/products.py

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_vendor)
):
    """Create a new product (vendor/admin only)"""
    try:
        use_case = CreateProductUseCase(db)
        return use_case.execute(product)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### 3️⃣ Use Case (Application Layer)

```python
# app/application/products/create_product.py

class CreateProductUseCase:
    """Use case for creating a new product"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)
    
    def execute(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product"""
        # Validar categoría
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise ValueError(f"Category {product_data.category_id} not found")
        
        # Validar SKU único
        existing = self.repository.get_by_sku(product_data.sku)
        if existing:
            raise ValueError(f"SKU {product_data.sku} already exists")
        
        # Crear producto
        product = self.repository.create(product_data)
        return ProductResponse.from_orm(product)
```

### 4️⃣ Repository (Infrastructure Layer)

```python
# app/infrastructure/repositories/product_repository.py

class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, Product)
    
    def get_by_sku(self, sku: str) -> Product | None:
        return self.db.query(self.model).filter(Product.sku == sku).first()
```

### 5️⃣ Base Repository (Infrastructure Layer)

```python
# app/infrastructure/repositories/base_repository.py

class BaseRepository(Generic[T, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def create(self, obj_in: CreateSchemaType) -> T:
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
```

### 6️⃣ Schema/DTO (Pydantic)

```python
# app/schemas/product_schemas.py

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    sku: str = Field(..., min_length=3)
    category_id: int
```

### 7️⃣ Modelo ORM (Database)

```python
# app/infrastructure/database/models_product.py

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    status = Column(Enum(ProductStatusEnum), default=ProductStatusEnum.ACTIVE)
```

### 8️⃣ Petición cURL

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Whey Protein 5KG",
    "description": "Premium whey protein concentrate",
    "price": 89.99,
    "stock": 50,
    "sku": "WHEY-5KG-001",
    "category_id": 1
  }'

# Respuesta 201:
# {
#   "id": 1,
#   "name": "Whey Protein 5KG",
#   "description": "Premium whey protein concentrate",
#   "price": 89.99,
#   "stock": 50,
#   "sku": "WHEY-5KG-001",
#   "status": "active",
#   "created_at": "2024-01-15T10:30:00Z",
#   "updated_at": "2024-01-15T10:30:00Z"
# }
```

---

## ✅ Buenas Prácticas

### 1. **Separación de Responsabilidades**

```python
# ❌ MAL - Lógica de negocio en endpoint
@router.post("/products")
async def create_product(product: ProductCreate, db: Session):
    if not category_exists(product.category_id):
        raise HTTPException(400)
    sku_product = db.query(Product).filter_by(sku=product.sku).first()
    if sku_product:
        raise HTTPException(400)
    # ... más lógica

# ✅ BIEN - Lógica en use case
@router.post("/products")
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_vendor)
):
    use_case = CreateProductUseCase(db)
    return use_case.execute(product)
```

### 2. **Validación en Múltiples Niveles**

```python
# Nivel 1: Pydantic (esquema)
class ProductCreate(BaseModel):
    price: Decimal = Field(..., gt=0)  # Validación básica
    sku: str = Field(..., min_length=3)

# Nivel 2: Repository (lógica de datos)
def get_by_sku(self, sku: str):
    return self.db.query(...).filter(Product.sku == sku).first()

# Nivel 3: Use case (lógica de negocio)
def execute(self, product_data: ProductCreate):
    if self.repository.get_by_sku(product_data.sku):
        raise ValueError("SKU duplicado")
```

### 3. **Inyección de Dependencias**

```python
# ✅ Fácil de testear
class CreateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    def execute(self, product: ProductCreate):
        return self.repository.create(product)

# En tests
@pytest.fixture
def mock_repository():
    return MagicMock(spec=ProductRepository)

def test_create_product(mock_repository):
    use_case = CreateProductUseCase(mock_repository)
    use_case.execute(product_data)
    mock_repository.create.assert_called_once()
```

### 4. **DTOs para Respuestas Específicas**

```python
# ✅ Diferentes schemas para diferentes contextos
class UserResponse(BaseModel):
    id: int
    email: str
    username: str

class UserDetailedResponse(UserResponse):
    phone: Optional[str]
    address: Optional[str]
    email_verified: bool

# En endpoints
@router.get("/users/{id}")
async def get_user(id: int) -> UserResponse:
    ...

@router.get("/admin/users/{id}")
async def get_user_detailed(
    id: int,
    current_user: dict = Depends(get_current_admin)
) -> UserDetailedResponse:
    ...
```

### 5. **Versionamiento de API**

```python
# Estructura para múltiples versiones
app/api/
├── v1/
│   ├── endpoints/
│   │   ├── products.py
│   └── router.py
└── v2/
    ├── endpoints/
    │   ├── products.py  # Endpoint mejorado
    └── router.py

# En main.py
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")
```

### 6. **Manejo de Errores Consistente**

```python
# app/utils/exceptions.py
class SupleGearException(Exception):
    pass

class DuplicateResourceError(SupleGearException):
    pass

class ResourceNotFoundError(SupleGearException):
    pass

# En endpoints
try:
    return use_case.execute(data)
except DuplicateResourceError as e:
    raise HTTPException(400, detail=str(e))
except ResourceNotFoundError as e:
    raise HTTPException(404, detail=str(e))
```

### 7. **Logging Estructurado**

```python
import logging

logger = logging.getLogger(__name__)

class CreateProductUseCase:
    def execute(self, product_data: ProductCreate):
        logger.info(f"Creating product: {product_data.name}")
        try:
            result = self.repository.create(product_data)
            logger.info(f"Product created: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Failed to create product: {str(e)}")
            raise
```

### 8. **Paginación Consistente**

```python
# ✅ Paginación en todos los endpoints
@router.get("/products")
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    products = repository.get_all(skip, limit)
    return {
        "data": products,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": repository.count()
        }
    }
```

---

## 🌱 Escalabilidad

### 1. **Agregar Nuevo Módulo (Ej: Reviews)**

```
# Crear estructura
app/domain/reviews/
app/application/reviews/
app/infrastructure/database/models_review.py
app/infrastructure/repositories/review_repository.py
app/api/v1/endpoints/reviews.py
app/schemas/review_schemas.py

# Pasos:
1. Crear entidad (models_review.py)
2. Crear DTOs (review_schemas.py)
3. Crear repositorio (review_repository.py)
4. Crear use cases (app/application/reviews/)
5. Crear endpoints (endpoints/reviews.py)
6. Incluir router en main.py

# Include en main.py
from app.api.v1.endpoints import reviews
app.include_router(reviews.router, prefix=settings.API_V1_STR)
```

### 2. **Usar Caché Redis**

```python
# app/infrastructure/services/cache_service.py
import redis

class CacheService:
    def __init__(self):
        self.redis = redis.Redis(host='redis', port=6379)
    
    def get(self, key: str):
        return self.redis.get(key)
    
    def set(self, key: str, value: str, ttl: int = 3600):
        self.redis.setex(key, ttl, value)

# En repository
def get_by_id(self, obj_id: int):
    cache_key = f"product_{obj_id}"
    cached = cache_service.get(cache_key)
    if cached:
        return json.loads(cached)
    
    product = self.db.query(self.model).filter(...).first()
    if product:
        cache_service.set(cache_key, json.dumps(product))
    return product
```

### 3. **Migraciones con Alembic**

```bash
# Inicializar Alembic
alembic init migrations

# Crear migración
alembic revision --autogenerate -m "Add reviews table"

# Aplicar migraciones
alembic upgrade head

# Revertir
alembic downgrade -1
```

### 4. **Mensajería Asíncrona (Celery)**

```python
# app/infrastructure/services/celery_app.py
from celery import Celery

celery_app = Celery(
    "suplegear",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def send_order_confirmation_email(order_id: int):
    order = Order.query.get(order_id)
    email_service.send(order.user.email, ...)

# Usar en use case
def execute(self, order_data):
    order = self.repository.create(order_data)
    send_order_confirmation_email.delay(order.id)
    return order
```

### 5. **Búsqueda Fulltext (Elasticsearch)**

```python
# app/infrastructure/services/search_service.py
from elasticsearch import Elasticsearch

class SearchService:
    def __init__(self):
        self.es = Elasticsearch(["elasticsearch:9200"])
    
    def index_product(self, product: Product):
        self.es.index(
            index="products",
            id=product.id,
            body={
                "name": product.name,
                "description": product.description,
                "price": product.price
            }
        )
    
    def search_products(self, query: str):
        return self.es.search(
            index="products",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name", "description"]
                    }
                }
            }
        )
```

### 6. **Rate Limiting**

```python
# app/api/v1/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.post("/products")
@limiter.limit("10/minute")
async def create_product(request: Request, ...):
    ...
```

### 7. **Documentación Automática**

```python
# En endpoints
@router.post(
    "/products",
    response_model=ProductResponse,
    summary="Create a new product",
    description="Create a new product. Requires vendor or admin role.",
    tags=["Products"]
)
async def create_product(...):
    """
    Create a new product.
    
    - **name**: Product name (required, 3-255 chars)
    - **price**: Product price (required, > 0)
    - **sku**: Stock Keeping Unit (required, unique)
    - **category_id**: Category ID (required)
    
    Returns:
    - **id**: Product ID
    - **created_at**: Creation timestamp
    """
    ...
```

---

## 🧪 Testing

### Tests Unitarios

```python
# tests/unit/test_products.py
import pytest
from app.application.products.create_product import CreateProductUseCase
from app.schemas.product_schemas import ProductCreate

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_create_product_success(mock_db):
    product_data = ProductCreate(
        name="Test Product",
        price=99.99,
        stock=10,
        sku="TEST-001",
        category_id=1
    )
    
    use_case = CreateProductUseCase(mock_db)
    result = use_case.execute(product_data)
    
    assert result.name == "Test Product"
    assert result.sku == "TEST-001"

def test_create_product_duplicate_sku(mock_db):
    with pytest.raises(ValueError):
        use_case.execute(duplicate_sku_product)
```

### Tests de Integración

```python
# tests/integration/test_product_flow.py
def test_create_and_list_products(client, db_session):
    # Crear categoría
    category_response = client.post(
        "/api/v1/categories",
        json={"name": "Proteins"},
        headers=admin_headers
    )
    category_id = category_response.json()["id"]
    
    # Crear producto
    product_response = client.post(
        "/api/v1/products",
        json={
            "name": "Test Whey",
            "price": 99.99,
            "sku": "TEST-001",
            "stock": 50,
            "category_id": category_id
        },
        headers=vendor_headers
    )
    assert product_response.status_code == 201
    
    # Listar productos
    list_response = client.get("/api/v1/products")
    assert len(list_response.json()) >= 1
```

### Ejecutar Tests

```bash
# Tests unitarios
pytest tests/unit -v

# Tests de integración
pytest tests/integration -v

# Con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/unit/test_products.py::test_create_product_success -v
```

---

## 🐳 Deployment

### Opción 1: Servidor EC2 (AWS)

```bash
# 1. SSH en servidor
ssh -i key.pem ubuntu@ec2-instance.amazonaws.com

# 2. Instalar dependencias
sudo apt-get update
sudo apt-get install python3.11 postgres postgresql-contrib nginx docker.io

# 3. Clonar repo
git clone <repository-url>
cd backend

# 4. Con Docker
docker build -t suplegear-api:1.0 .
docker run -p 8000:8000 suplegear-api:1.0

# 5. Configurar Nginx como proxy reverso
# /etc/nginx/sites-available/default
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Opción 2: Heroku

```bash
heroku create suplegear-api
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=postgresql://...
git push heroku main
```

### Opción 3: Railway/Render

```bash
# railway.json
{
  "buildCommand": "pip install -r requirements.txt",
  "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
}
```

### CI/CD con GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        options: >-
          --health-cmd pg_isready
        env:
          POSTGRES_PASSWORD: postgres
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - run: pip install -r requirements.txt
      - run: pytest
      - run: docker build -t suplegear-api .
      - run: docker push yourdockeruser/suplegear-api
```

---

## 📊 Variables de Entorno

```env
# Core
APP_NAME=SupleGear API
DEBUG=False
SECRET_KEY=your-production-secret-key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/suplegear

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your-app-password

# Stripe
STRIPE_API_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# CORS
CORS_ORIGINS=["https://yourdomain.com"]
```

---

## 📞 Soporte y Contacto

Para preguntas o problemas:
1. Revisar documentación en `/docs`
2. Abrir issue en GitHub
3. Contactar al equipo: `dev@suplegear.com`

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙌 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crear rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

**Última actualización:** Enero 2024
**Versión:** 1.0.0
