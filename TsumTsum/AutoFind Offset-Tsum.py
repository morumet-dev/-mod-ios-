import zipfile
import os
import shutil
import re

changes = [
    {'name': 'コインアドレス1', 'pattern': '0840201EA8', 'offset': 0x1C, 'index': 0},
    {'name': 'コインアドレス2', 'pattern': '0840201EA8', 'offset': 0x18, 'index': 0},
    {'name': 'メダルアドレス1', 'pattern': '0019201e01', 'offset': -0x68, 'index': 1},
    {'name': 'メダルアドレス2', 'pattern': '0019201e01', 'offset': -0x64, 'index': 1},
    {'name': 'ツムEXP', 'pattern': '8812088B', 'offset': 0x18, 'index': 2},
    {'name': 'スコアMAX', 'pattern': '136868F8', 'offset': -0x18, 'index': 1},
    {'name': '全ツムチェーン', 'pattern': 'B31000B4F4', 'offset': -0x20, 'index': 0},
    {'name': 'スキル無限', 'pattern': '014140f900102d1e', 'offset': 0x28, 'index': 0},
    {'name': '倍速MAX', 'pattern': 'df0e0ef8', 'offset': -0x8, 'index': 0},
    {'name': '広告削除', 'pattern': '600C0034', 'offset': -0x48, 'index': 2},
    {'name': '利用規約スキップ', 'pattern': 'E800F837FD7B', 'offset': -0x2C, 'index': 5},
    {'name': '時間停止', 'pattern': '0101012A', 'offset': 0x38, 'index': 0},
    {'name': '即終了', 'pattern': 'C00300347F', 'offset': -0x4, 'index': 0},
]

def extract_ipa(ipa_path, extract_to):
    with zipfile.ZipFile(ipa_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def display_offsets(binary_path):
    with open(binary_path, 'rb') as f:
        data = f.read()

    print("==== OFFSET LIST ====")
    for c in changes:
        pattern = bytes.fromhex(c['pattern'])
        matches = [m.start() for m in re.finditer(re.escape(pattern), data)]

        if len(matches) <= c['index']:
            print(f"{c['name']}: NOT FOUND")
            continue

        base = matches[c['index']]
        target = base + c['offset']
        print(f"{c['name']}: {hex(target)}")

def main():
    ipa_path = "/home/container/Tsum.ipa"
    extract_dir = "temp_extracted"

    extract_ipa(ipa_path, extract_dir)

    binary_path = os.path.join(
        extract_dir,
        "Payload",
        "TsumTsum.app",
        "TsumTsum"
    )

    display_offsets(binary_path)

    shutil.rmtree(extract_dir)

if __name__ == "__main__":
    main()

