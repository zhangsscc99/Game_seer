# scripts/ 脚本说明

本目录包含用于批量导入精灵立绘和游戏数据的一次性脚本。

---

## 脚本列表与用途

| 文件 | 用途 |
|---|---|
| `parse_elves.py` | 扫描立绘目录，解析文件名，生成原始数据 `elves_raw.json` |
| `assign_elf_data.py` | 读取原始数据，分配稀有度、属性、进化阶段，生成 `elves_data.json` |
| `copy_elves.py` | 将立绘按 id 重命名后复制到 `backend/static/elves/` |
| `import_elves.py` | 读取 `elves_data.json`，将精灵模板批量写入 SQLite 数据库 |
| `run_all.py` | 一键按顺序执行以上全部脚本 |

---

## 运行顺序

脚本之间存在依赖关系，必须按以下顺序执行：

```
1. parse_elves.py       -> 生成 elves_raw.json
2. assign_elf_data.py   -> 生成 elves_data.json
3. copy_elves.py        -> 复制图片到 static/elves/
4. import_elves.py      -> 写入数据库
```

---

## 一键运行

在 `backend/` 目录下执行：

```bash
python scripts/run_all.py
```

---

## 单独运行某个脚本

所有脚本均需在 `backend/` 目录下运行：

```bash
cd backend/

python scripts/parse_elves.py
python scripts/assign_elf_data.py
python scripts/copy_elves.py
python scripts/import_elves.py
```

---

## 数据规则说明

### 稀有度（按编号区间）

| 编号范围 | 稀有度 |
|---|---|
| 1 ~ 200 | N（普通） |
| 201 ~ 350 | R（稀有） |
| 351 ~ 450 | SR（超稀有） |
| 451 ~ 490 | SSR（传说） |
| 491 ~ 500 | UR（唯一） |

### 属性（按编号取模 6）

| id % 6 | 属性 |
|---|---|
| 0 | fire |
| 1 | water |
| 2 | grass |
| 3 | thunder |
| 4 | ice |
| 5 | dark |

### 进化阶段（以3为一组）

编号组内位置 `(id - 1) % 3`：
- 0 → stage 1，evolves_from_id = null
- 1 → stage 2，evolves_from_id = id - 1
- 2 → stage 3，evolves_from_id = id - 1

---

## 注意事项

- `import_elves.py` 会检查 `elf_templates` 表是否已有数据，若有则跳过，不会重复插入。
- 如需重新导入，先手动清空表：`DELETE FROM elf_templates;`
- 图片路径统一为 `elves/{id}.png`，对应 `backend/static/elves/` 目录。
