from typing import Annotated, Optional

from pydantic import BaseModel
from pydantic.types import StringConstraints


class CategoryBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
    slug: Annotated[str, StringConstraints(min_length=1)]
    is_active: Optional[bool] = False
    level: Optional[bool] = 100
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass
