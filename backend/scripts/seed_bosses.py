"""
seed_bosses.py
为指定精灵创建 Boss 记录（如需重新生成，先清空 bosses 表）
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import models.user, models.task, models.achievement  # noqa
from models.boss import Boss, BossType
from models.elf import ElfTemplate
from core.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PATH = BACKEND_DIR / "game_seer.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

# elf_id, boss_type, required_tasks, reward_exp, reward_coins
BOSS_ELVES = [
    (34,  "daily",   10, 150,  75),   # 钢牙鲨
    (47,  "weekly",  20, 250, 120),   # 蘑菇怪
    (42,  "daily",   10, 150,  75),   # 里奥斯
    (69,  "weekly",  18, 220, 110),   # 提亚斯
    (88,  "weekly",  25, 300, 150),   # 纳多雷
    (113, "monthly", 35, 500, 250),   # 雷纳多
    (132, "monthly", 40, 600, 300),   # 尤纳斯
]

ELEM_DESC = {
    "fire":    "烈焰肆虐，炙热难当",
    "water":   "深海之力，波涛汹涌",
    "grass":   "生命涌动，藤蔓缠绕",
    "thunder": "雷霆万钧，闪电肆虐",
    "ice":     "寒冰封印，冻结一切",
    "dark":    "暗影笼罩，诡异莫测",
}

def main():
    existing = db.query(Boss).count()
    if existing > 0:
        print(f"Boss 表已有 {existing} 条，跳过（清空后重新运行）")
        db.close()
        return

    created = 0
    for elf_id, btype, req_tasks, exp, coins in BOSS_ELVES:
        elf = db.query(ElfTemplate).filter(ElfTemplate.id == elf_id).first()
        if not elf:
            print(f"未找到精灵 #{elf_id}")
            continue
        desc = ELEM_DESC.get(elf.element, "神秘力量蠢蠢欲动")
        db.add(Boss(
            name=elf.name,
            description=f"{desc}。完成 {req_tasks} 个任务后可挑战，击败后解锁该精灵。",
            image_path=elf.image_path,
            boss_type=getattr(BossType, btype),
            required_tasks=req_tasks,
            reward_exp=exp,
            reward_coins=coins,
            reward_elf_id=elf.id,
            is_repeatable=(btype == "daily"),
        ))
        created += 1
        print(f"创建 #{elf_id} {elf.name} ({btype})")

    db.commit()
    print(f"完成！共创建 {created} 个 Boss")
    db.close()

if __name__ == "__main__":
    main()
