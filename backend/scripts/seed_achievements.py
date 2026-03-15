"""
seed_achievements.py
创建基于击败Boss数量的成就记录
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import models.user, models.task, models.elf, models.boss  # noqa
from models.achievement import Achievement, ConditionType
from core.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PATH = BACKEND_DIR / "game_seer.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()

ACHIEVEMENTS = [
    dict(
        name="初战告捷",
        description="击败你的第一个 Boss，踏上征服之路。",
        icon="🏅",
        condition_type=ConditionType.boss_defeat,
        condition_value=1,
        reward_title="新星指挥官",
    ),
    dict(
        name="战场老手",
        description="累计击败 3 个 Boss，经验逐渐丰富。",
        icon="⚔️",
        condition_type=ConditionType.boss_defeat,
        condition_value=3,
        reward_title="战场老手",
    ),
    dict(
        name="精灵猎手",
        description="累计击败 5 个 Boss，威名远播。",
        icon="🎯",
        condition_type=ConditionType.boss_defeat,
        condition_value=5,
        reward_title="精灵猎手",
    ),
    dict(
        name="Boss终结者",
        description="击败全部 7 个 Boss，成为最强指挥官！",
        icon="👑",
        condition_type=ConditionType.boss_defeat,
        condition_value=7,
        reward_title="Boss终结者",
    ),
]

def main():
    existing = db.query(Achievement).count()
    if existing > 0:
        print(f"成就表已有 {existing} 条，跳过")
        db.close()
        return

    for a in ACHIEVEMENTS:
        db.add(Achievement(**a))
    db.commit()
    print(f"创建了 {len(ACHIEVEMENTS)} 个成就")
    for a in ACHIEVEMENTS:
        print(f"  [{a['condition_value']} Boss] {a['name']}")
    db.close()

if __name__ == "__main__":
    main()
