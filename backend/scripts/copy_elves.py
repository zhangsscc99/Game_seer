"""
copy_elves.py
将立绘从源目录复制到 backend/static/elves/，并按 id 重命名为 {id}.png。
"""

import json
import shutil
from pathlib import Path

# 源目录
SRC_DIR = Path(r"C:\Users\宇庭\Desktop\seer_resources\赛尔号页游立绘\赛尔号页游立绘\序号1~500")

# 目标目录（backend/static/elves/）
BACKEND_DIR = Path(__file__).parent.parent
DST_DIR = BACKEND_DIR / "static" / "elves"

# elves_raw.json 提供 id <-> filename 映射
SCRIPT_DIR = Path(__file__).parent
RAW_JSON = SCRIPT_DIR / "elves_raw.json"

PROGRESS_INTERVAL = 50  # 每复制多少张打印一次进度


def main():
    print("=== 复制精灵立绘 ===")
    print(f"源目录：{SRC_DIR}")
    print(f"目标目录：{DST_DIR}")

    if not SRC_DIR.exists():
        raise FileNotFoundError(f"源目录不存在：{SRC_DIR}")

    if not RAW_JSON.exists():
        raise FileNotFoundError(
            f"找不到 {RAW_JSON}，请先运行 parse_elves.py"
        )

    # 确保目标目录存在
    DST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"目标目录已就绪：{DST_DIR}\n")

    raw_list: list[dict] = json.loads(RAW_JSON.read_text(encoding="utf-8"))
    total = len(raw_list)
    success = 0
    skipped = 0
    errors = []

    for i, elf in enumerate(raw_list, start=1):
        src_file = SRC_DIR / elf["filename"]
        dst_file = DST_DIR / f"{elf['id']}.png"

        if not src_file.exists():
            errors.append(f"源文件不存在：{src_file}")
            continue

        try:
            shutil.copy2(src_file, dst_file)
            success += 1
        except Exception as e:
            errors.append(f"复制失败 {src_file} -> {dst_file}：{e}")
            continue

        if i % PROGRESS_INTERVAL == 0 or i == total:
            print(f"  进度：{i}/{total}  已完成：{success}  跳过/失败：{len(errors)}")

    print(f"\n=== 复制完成 ===")
    print(f"成功：{success} 张")
    print(f"失败：{len(errors)} 张")
    if errors:
        print("\n--- 错误详情 ---")
        for err in errors:
            print(f"  {err}")


if __name__ == "__main__":
    main()
