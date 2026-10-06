from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock_quantity: float
    unit: str
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: float


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: float
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: str
    total_price: float
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True

        
class UserRegister(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str