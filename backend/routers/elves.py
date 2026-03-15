from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User, UserProfile
from models.elf import ElfTemplate, UserElf, ElfRarity, ElfElement
from schemas.elf import ElfTemplateResponse, ElfPageResponse, UserElfResponse

router = APIRouter(prefix="/elves", tags=["elves"])

UNLOCK_COST = {
    ElfRarity.N:   5,
    ElfRarity.R:   15,
    ElfRarity.SR:  30,
    ElfRarity.SSR: 60,
    ElfRarity.UR:  100,
}


@router.get("/my", response_model=List[UserElfResponse])
def get_my_elves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(UserElf).filter(UserElf.user_id == current_user.id).all()


@router.get("/", response_model=ElfPageResponse)
def list_elves(
    rarity: Optional[ElfRarity] = Query(None),
    element: Optional[ElfElement] = Query(None),
    name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ElfTemplate)
    if rarity:
        query = query.filter(ElfTemplate.rarity == rarity)
    if element:
        query = query.filter(ElfTemplate.element == element)
    if name:
        query = query.filter(ElfTemplate.name.ilike(f"%{name}%"))

    total = query.count()
    offset = (page - 1) * page_size
    raw_items = query.order_by(ElfTemplate.id).offset(offset).limit(page_size).all()
    pages = max(1, (total + page_size - 1) // page_size)

    items = []
    for e in raw_items:
        d = {c.name: getattr(e, c.name) for c in e.__table__.columns}
        d["unlock_cost"] = UNLOCK_COST.get(e.rarity, 5)
        items.append(d)

    return ElfPageResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{elf_id}", response_model=ElfTemplateResponse)
def get_elf(
    elf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    elf = db.query(ElfTemplate).filter(ElfTemplate.id == elf_id).first()
    if not elf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elf not found")
    d = {c.name: getattr(elf, c.name) for c in elf.__table__.columns}
    d["unlock_cost"] = UNLOCK_COST.get(elf.rarity, 5)
    return d


@router.post("/{elf_id}/unlock", response_model=UserElfResponse, status_code=status.HTTP_201_CREATED)
def unlock_elf_with_credits(
    elf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """花费解锁额度解锁精灵。"""
    template = db.query(ElfTemplate).filter(ElfTemplate.id == elf_id).first()
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="精灵不存在")

    existing = db.query(UserElf).filter(
        UserElf.user_id == current_user.id, UserElf.template_id == elf_id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="已拥有该精灵")

    cost = UNLOCK_COST.get(template.rarity, 5)
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile or profile.unlock_credits < cost:
        available = profile.unlock_credits if profile else 0
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"额度不足，需要 {cost} 额度，当前剩余 {available}"
        )

    profile.unlock_credits -= cost
    new_elf = UserElf(user_id=current_user.id, template_id=elf_id, level=1, exp=0, bond=0, is_active=False)
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
