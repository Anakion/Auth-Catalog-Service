from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        examples=["Электроника"],
        description="Название категории",
    )


class UpdateCategoryRequest(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
