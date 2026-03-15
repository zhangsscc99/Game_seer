"""
parse_elves.py
解析立绘目录，提取每个文件的序号和精灵名，保存为 elves_raw.json。
"""

import re
import json
from pathlib import Path

# 立绘源目录
IMAGES_DIR = Path(r"C:\Users\宇庭\Desktop\seer_resources\赛尔号页游立绘\赛尔号页游立绘\序号1~500")

# 输出文件路径（脚本所在目录）
SCRIPT_DIR = Path(__file__).parent
OUTPUT_FILE = SCRIPT_DIR / "elves_raw.json"

FILENAME_RE = re.compile(r"^(\d+)(.+)\.png$")


def parse_elves(images_dir: Path) -> list[dict]:
    """扫描目录，解析所有精灵文件名，返回 {id, name, filename} 列表。"""
    elves = []

    if not images_dir.exists():
        raise FileNotFoundError(f"立绘目录不存在：{images_dir}")

    for filepath in images_dir.iterdir():
        if not filepath.is_file():
            continue
        filename = filepath.name
        match = FILENAME_RE.match(filename)
        if not match:
            print(f"  [跳过] 无法解析文件名：{filename}")
            continue
        elf_id = int(match.group(1))
        elf_name = match.group(2)
        elves.append({
            "id": elf_id,
            "name": elf_name,
            "filename": filename,
        })

    # 按 id 数字排序
    elves.sort(key=lambda x: x["id"])
    return elves


def main():
    print("=== 解析立绘目录 ===")
    print(f"源目录：{IMAGES_DIR}")

    elves = parse_elves(IMAGES_DIR)
    total = len(elves)
    print(f"\n共解析到 {total} 只精灵\n")

    print("--- 前10条预览 ---")
    for elf in elves[:10]:
        print(f"  id={elf['id']:>4}  name={elf['name']}  filename={elf['filename']}")

    OUTPUT_FILE.write_text(
        json.dumps(elves, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n已保存至：{OUTPUT_FILE}")
    print(f"总计 {total} 条记录")


if __name__ == "__main__":
    main()
