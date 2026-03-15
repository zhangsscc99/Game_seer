from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship
import enum

from core.database import Base


class ElfRarity(str, enum.Enum):
    N = "N"
    R = "R"
    SR = "SR"
    SSR = "SSR"
    UR = "UR"


class ElfElement(str, enum.Enum):
    fire = "fire"
    water = "water"
    grass = "grass"
    thunder = "thunder"
    ice = "ice"
    dark = "dark"


class ElfTemplate(Base):
    __tablename__ = "elf_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    rarity = Column(SAEnum(ElfRarity), default=ElfRarity.N, nullable=False)
    element = Column(SAEnum(ElfElement), default=ElfElement.fire, nullable=False)
    stage = Column(Integer, default=1)  # 1/2/3 evolution stage
    evolves_from_id = Column(Integer, ForeignKey("elf_templates.id"), nullable=True)
    unlock_condition = Column(String, nullable=True)
    description = Column(String, nullable=True)

    evolves_from = relationship("ElfTemplate", remote_side=[id], foreign_keys=[evolves_from_id])
    user_elves = relationship("UserElf", back_populates="template")


class UserElf(Base):
    __tablename__ = "user_elves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("elf_templates.id"), nullable=False)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    bond = Column(Integer, default=0)  # 好感度
    is_active = Column(Boolean, default=False)
    obtained_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="elves")
    template = relationship("ElfTemplate", back_populates="user_elves")
