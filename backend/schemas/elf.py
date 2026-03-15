from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from models.elf import ElfRarity, ElfElement


class ElfTemplateResponse(BaseModel):
    id: int
    name: str
    image_path: Optional[str]
    rarity: ElfRarity
    element: ElfElement
    stage: int
    evolves_from_id: Optional[int]
    unlock_condition: Optional[str]
    description: Optional[str]
    unlock_cost: int = 5   # 解锁所需额度

    class Config:
        from_attributes = True


class ElfPageResponse(BaseModel):
    items: List[ElfTemplateResponse]
    total: int
    page: int
    page_size: int
    pages: int


class ElfTemplateCreate(BaseModel):
    name: str
    image_path: Optional[str] = None
    rarity: ElfRarity = ElfRarity.N
    element: ElfElement = ElfElement.fire
    stage: int = 1
    evolves_from_id: Optional[int] = None
    unlock_condition: Optional[str] = None
    description: Optional[str] = None


class ElfTemplateUpdate(BaseModel):
    name: Optional[str] = None
    image_path: Optional[str] = None
    rarity: Optional[ElfRarity] = None
    element: Optional[ElfElement] = None
    stage: Optional[int] = None
    unlock_condition: Optional[str] = None
    description: Optional[str] = None


class UserElfResponse(BaseModel):
    id: int
    user_id: int
    template_id: int
    level: int
    exp: int
    bond: int
    is_active: bool
    obtained_at: datetime
    template: ElfTemplateResponse

    class Config:
        from_attributes = True


class UserElfUpdate(BaseModel):
    is_active: Optional[bool] = None
