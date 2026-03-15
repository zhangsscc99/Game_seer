"""
update_cdn_paths.py
将数据库中精灵的 image_path 更新为腾讯云 CloudBase CDN URL
"""
import sys
import json
from pathlib import Path
from urllib.parse import quote

BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import models.user    # noqa
import models.task    # noqa
import models.boss    # noqa
import models.achievement  # noqa
from models.elf import ElfTemplate
from core.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ===== 配置 CDN 域名 =====
CDN_BASE = "https://636c-cloud1-9gbxfuqjd1864b3c-1359119781.tcb.qcloud.la"
CDN_PATH = "seer/序号1~500"  # CloudBase 里的文件夹路径
# =========================

DB_PATH = BACKEND_DIR / "game_seer.db"
DATA_FILE = Path(__file__).parent / "elves_data.json"


def make_cdn_url(filename: str) -> str:
    """构造 CDN URL，对中文路径进行 URL 编码"""
    encoded_path = quote(CDN_PATH, safe="/")
    encoded_filename = quote(filename, safe="")
    return f"{CDN_BASE}/{encoded_path}/{encoded_filename}"


def main():
    # 读取本地精灵数据（含原始文件名）
    with open(DATA_FILE, encoding="utf-8") as f:
        elves_data = json.load(f)

    # id -> filename 映射
    id_to_filename = {e["id"]: e["filename"] for e in elves_data}

    print(f"=== 更新精灵 CDN 路径 ===")
    print(f"CDN 基础域名: {CDN_BASE}")
    print(f"精灵总数: {len(id_to_filename)}")
    print()

    # 连接数据库
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        updated = 0
        not_found = 0

        for elf_id, filename in id_to_filename.items():
            elf = db.query(ElfTemplate).filter(ElfTemplate.id == elf_id).first()
            if elf:
                elf.image_path = make_cdn_url(filename)
                updated += 1
            else:
                not_found += 1

        db.commit()
        print(f"✅ 成功更新: {updated} 条")
        if not_found:
            print(f"⚠️  未找到: {not_found} 条")

        # 预览前3条
        print("\n--- 前3条预览 ---")
        for elf in db.query(ElfTemplate).order_by(ElfTemplate.id).limit(3).all():
            print(f"  #{elf.id:03d} {elf.name} → {elf.image_path}")

    except Exception as e:
        db.rollback()
        print(f"❌ 失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
