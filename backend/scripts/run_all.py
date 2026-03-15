"""
run_all.py
一键按顺序运行所有精灵导入脚本的入口文件。
在 backend/ 目录下运行：python scripts/run_all.py
"""

import subprocess
import sys

scripts = [
    "parse_elves.py",
    "assign_elf_data.py",
    "copy_elves.py",
    "import_elves.py",
]

for s in scripts:
    print(f"\n=== 运行 {s} ===")
    result = subprocess.run(
        [sys.executable, f"scripts/{s}"],
        cwd="..",
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"❌ {s} 失败，停止")
        sys.exit(result.returncode)
    print(f"✅ {s} 完成")

print("\n🎉 所有脚本执行完毕！")
