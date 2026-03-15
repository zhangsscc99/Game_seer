"""
assign_elf_data.py
读取 elves_raw.json，为每只精灵分配稀有度、属性、进化阶段等游戏数据，
保存为 elves_data.json。
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "elves_raw.json"
OUTPUT_FILE = SCRIPT_DIR / "elves_data.json"


# ---------- 稀有度规则 ----------
def assign_rarity(elf_id: int) -> str:
    if elf_id <= 200:
        return "N"
    elif elf_id <= 350:
        return "R"
    elif elf_id <= 450:
        return "SR"
    elif elf_id <= 490:
        return "SSR"
    else:
        return "UR"


# ---------- 属性规则 ----------
ELEMENT_MAP = {
    0: "fire",
    1: "water",
    2: "grass",
    3: "thunder",
    4: "ice",
    5: "dark",
}

def assign_element(elf_id: int) -> str:
    return ELEMENT_MAP[elf_id % 6]


# ---------- 进化阶段规则 ----------
def assign_evolution(elf_id: int) -> tuple[int, int | None]:
    """
    以3为一组推断进化阶段：
      组内位置 = (id - 1) % 3
        0 -> stage 1, evolves_from_id = None
        1 -> stage 2, evolves_from_id = id - 1
        2 -> stage 3, evolves_from_id = id - 1
    """
    pos = (elf_id - 1) % 3  # 0, 1, 2
    stage = pos + 1          # 1, 2, 3
    evolves_from_id = None if stage == 1 else elf_id - 1
    return stage, evolves_from_id


# ---------- 解锁条件文本 ----------
UNLOCK_CONDITION_MAP = {
    "N":   "完成任意5个任务解锁",
    "R":   "累计完成20个任务解锁",
    "SR":  "连续打卡7天或完成周Boss解锁",
    "SSR": "完成月Boss或月目标达成率90%以上解锁",
    "UR":  "完成特殊成就解锁",
}


def build_elf_data(raw: dict) -> dict:
    elf_id = raw["id"]
    rarity = assign_rarity(elf_id)
    element = assign_element(elf_id)
    stage, evolves_from_id = assign_evolution(elf_id)

    return {
        "id": elf_id,
        "name": raw["name"],
        "filename": raw["filename"],
        "rarity": rarity,
        "element": element,
        "stage": stage,
        "evolves_from_id": evolves_from_id,
        "image_path": f"elves/{elf_id}.png",
        "unlock_condition": UNLOCK_CONDITION_MAP[rarity],
    }


def main():
    print("=== 分配精灵游戏属性 ===")
    print(f"读取：{INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"找不到 {INPUT_FILE}，请先运行 parse_elves.py"
        )

    raw_list: list[dict] = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    print(f"共读取 {len(raw_list)} 条原始数据\n")

    data_list = [build_elf_data(raw) for raw in raw_list]

    # 统计各稀有度数量
    from collections import Counter
    rarity_count = Counter(d["rarity"] for d in data_list)
    print("--- 稀有度分布 ---")
    for rarity in ["N", "R", "SR", "SSR", "UR"]:
        print(f"  {rarity:<4}: {rarity_count.get(rarity, 0)} 只")

    # 统计各属性数量
    element_count = Counter(d["element"] for d in data_list)
    print("\n--- 属性分布 ---")
    for elem in ["fire", "water", "grass", "thunder", "ice", "dark"]:
        print(f"  {elem:<8}: {element_count.get(elem, 0)} 只")

    print("\n--- 前5条预览 ---")
    for d in data_list[:5]:
        print(
            f"  id={d['id']:>3}  name={d['name']:<8}  "
            f"rarity={d['rarity']:<4}  element={d['element']:<8}  "
            f"stage={d['stage']}  evolves_from={d['evolves_from_id']}"
        )

    OUTPUT_FILE.write_text(
        json.dumps(data_list, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n已保存至：{OUTPUT_FILE}")
    print(f"总计 {len(data_list)} 条记录")


if __name__ == "__main__":
    main()
