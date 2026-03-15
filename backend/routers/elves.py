from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.elf import ElfTemplate, UserElf, ElfRarity, ElfElement
from schemas.elf import ElfTemplateResponse, UserElfResponse

router = APIRouter(prefix="/elves", tags=["elves"])


@router.get("/my", response_model=List[UserElfResponse])
def get_my_elves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the current user's collected elves."""
    return (
        db.query(UserElf)
        .filter(UserElf.user_id == current_user.id)
        .all()
    )


@router.get("/", response_model=List[ElfTemplateResponse])
def list_elves(
    rarity: Optional[ElfRarity] = Query(None),
    element: Optional[ElfElement] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the elf compendium with optional rarity/element filters and pagination."""
    query = db.query(ElfTemplate)
    if rarity:
        query = query.filter(ElfTemplate.rarity == rarity)
    if element:
        query = query.filter(ElfTemplate.element == element)

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()


@router.get("/{elf_id}", response_model=ElfTemplateResponse)
def get_elf(
    elf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get details of a specific elf template."""
    elf = db.query(ElfTemplate).filter(ElfTemplate.id == elf_id).first()
    if not elf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elf not found")
    return elf


@router.post("/my/{template_id}", response_model=UserElfResponse, status_code=status.HTTP_201_CREATED)
def unlock_elf(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Unlock an elf for the current user (admin or condition-based)."""
    template = db.query(ElfTemplate).filter(ElfTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elf template not found")

    existing = (
        db.query(UserElf)
        .filter(UserElf.user_id == current_user.id, UserElf.template_id == template_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Elf already unlocked",
        )

    new_elf = UserElf(
        user_id=current_user.id,
        template_id=template_id,
        level=1,
        exp=0,
        bond=0,
        is_active=False,
    )
    db.add(new_elf)
    db.commit()
    db.refresh(new_elf)
    return new_elf


@router.put("/my/{user_elf_id}/active", response_model=UserElfResponse)
def set_active_elf(
    user_elf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Set an elf as the active (main) elf; deactivates the previously active one."""
    elf_to_activate = (
        db.query(UserElf)
        .filter(UserElf.id == user_elf_id, UserElf.user_id == current_user.id)
        .first()
    )
    if not elf_to_activate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User elf not found")

    # Deactivate all other elves for this user
    db.query(UserElf).filter(
        UserElf.user_id == current_user.id,
        UserElf.id != user_elf_id,
    ).update({"is_active": False})

    elf_to_activate.is_active = True
    db.commit()
    db.refresh(elf_to_activate)
    return elf_to_activate
