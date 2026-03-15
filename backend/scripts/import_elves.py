"""
import_elves.py
读取 elves_data.json，将精灵模板数据批量插入数据库的 elf_templates 表。
"""

import sys
import json
from pathlib import Path

# 将 backend 根目录加入 sys.path，以便导入 core / models 等包
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 导入模型（触发 Base.metadata 注册，必须全部导入才能解析关系）
import models.user   # noqa: F401
import models.task   # noqa: F401
import models.boss   # noqa: F401
import models.achievement  # noqa: F401
from models.elf import ElfTemplate, ElfRarity, ElfElement  # noqa: E402
from core.database import Base  # noqa: E402

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "elves_data.json"

# 数据库文件路径（backend 根目录下）
DB_PATH = BACKEND_DIR / "game_seer.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"


def get_engine_and_session():
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    # 确保表存在（如果后端还没有 alembic 迁移，这里直接建表）
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, Session


def main():
    print("=== 导入精灵模板到数据库 ===")
    print(f"数据库：{DB_PATH}")
    print(f"数据文件：{DATA_FILE}")

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"找不到 {DATA_FILE}，请先运行 assign_elf_data.py"
        )

    data_list: list[dict] = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    print(f"共读取 {len(data_list)} 条精灵数据\n")

    engine, Session = get_engine_and_session()
    db = Session()

    try:
        # 检查是否已有数据，避免重复导入
        existing_count = db.query(ElfTemplate).count()
        if existing_count > 0:
            print(f"[警告] elf_templates 表中已有 {existing_count} 条记录。")
            print("若要重新导入，请先清空表数据（DELETE FROM elf_templates）。")
            print("跳过导入，退出。")
            return

        print("表为空，开始批量插入...")

        # 第一遍：插入所有精灵（不设置 evolves_from_id，避免外键顺序问题）
        id_to_obj: dict[int, ElfTemplate] = {}
        for d in data_list:
            elf = ElfTemplate(
                id=d["id"],
                name=d["name"],
                image_path=d["image_path"],
                rarity=ElfRarity(d["rarity"]),
                element=ElfElement(d["element"]),
                stage=d["stage"],
                evolves_from_id=None,          # 先设 None，第二遍更新
                unlock_condition=d["unlock_condition"],
            )
            db.add(elf)
            id_to_obj[d["id"]] = elf

        db.flush()  # 写入 id，但不提交

        # 第二遍：更新 evolves_from_id
        updated = 0
        for d in data_list:
            if d["evolves_from_id"] is not None:
                elf = id_to_obj[d["id"]]
                elf.evolves_from_id = d["evolves_from_id"]
                updated += 1

        db.commit()
        total = db.query(ElfTemplate).count()
        print(f"\n=== 导入完成 ===")
        print(f"成功插入：{total} 条")
        print(f"设置进化链：{updated} 条")

    except Exception as e:
        db.rollback()
        print(f"\n[错误] 导入失败，已回滚：{e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
