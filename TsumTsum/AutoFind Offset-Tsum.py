import zipfile
import os
import shutil
import re

changes = [
    {'name': 'コイン1億固定', 'pattern': '0840201EA8', 'offset':0x1C, 'index': 0, 'value': '01209C72', 'group': 'コイン1億'},
    {'name': 'コイン1億固定2', 'pattern': '0840201EA8', 'offset':0x18, 'index': 0, 'value': 'A1BEA052', 'group': 'コイン1億'},
    {'name': 'メダル1億固定', 'pattern': '0019201e01', 'offset':-0x68, 'index': 1, 'value': 'A1BEA052', 'group': 'メダル1億'},
    {'name': 'メダル1億固定2', 'pattern': '0019201e01', 'offset':-0x64, 'index': 1, 'value': '01209C72', 'group': 'メダル1億'},
    {'name': 'メダル2億固定', 'pattern': '0019201e01', 'offset':-0x68, 'index': 1, 'value': '617DA152', 'group': 'メダル2億'},
    {'name': 'メダル2億固定2', 'pattern': '0019201e01', 'offset':-0x64, 'index': 1, 'value': '01409872', 'group': 'メダル2億'},
     {'name': 'LIAPP ALERT 回避1', 'pattern': '1f0100f12419', 'offset': 0x8, 'index': 2, 'value': '1f2003d5'},
     {'name': 'LIAPP ALERT 回避2', 'pattern': '1f0100f12419', 'offset': 0x30, 'index': 2, 'value': 'A3010094'},
    {'name': '1ツムコイン', 'pattern': '01310B91', 'offset': 0x8, 'index': 2, 'value': '68008052', 'group': '1ツム1コイン'},
    {'name': 'ツムEXP', 'pattern': '8812088B', 'offset': 0x18, 'index': 2, 'value': '016A9852'},
    {'name': 'スコアMAX', 'pattern': '136868F8', 'offset': -0x18, 'index': 1, 'value': 'C0035FD6'},
    {'name': 'フィーバー時終了', 'pattern': 'b42a40f9', 'offset': 0x14, 'index': 0, 'value': 'E003271E'},
    {'name': 'レベルロックリザルトスキップ', 'pattern': 'C1050035', 'offset': -0x20, 'index': 0, 'value': 'C0035FD6'},
    {'name': 'ツム消し2秒増加', 'pattern': '68160639', 'offset': 0x20, 'index': 1, 'value': '1F2003D5'},
    {'name': '全ツムチェーン', 'pattern': 'B31000B4F4', 'offset': -0x20, 'index': 0, 'value': 'C0035FD6'},
    {'name': 'スキル無限', 'pattern': '014140f900102d1e', 'offset': 0x28, 'index': 0, 'value': '22008052'},
    {'name': '倍速MAX', 'pattern': 'df0e0ef8', 'offset': -0x8, 'index': 0, 'value': '00F0271E'},
    {'name': 'プレイ倍速３倍', 'pattern': '011840bd', 'offset': 0x4, 'index': 3, 'value': '0810211E'},
    {'name': 'リザスキ', 'pattern': 'E8FEFF36600E40F9', 'offset': 0x20, 'index': 3, 'value': 'C0035FD6'},
    {'name': '試合リザスキ', 'pattern': 'C80A00B4', 'offset': -0x8, 'index': 1, 'value': '340080D2'},
    {'name': 'コンボ999', 'pattern': 'c80600b4', 'offset': -0x14, 'index': 4, 'value': 'E17C8052'},
    {'name': '5秒前スタート', 'pattern': '43B8890A40B90801094A', 'offset': 0x6, 'index': 0, 'value': 'A000271E'},
    {'name': 'フィーバーゲージ増加', 'pattern': 'BD0210301E', 'offset': 0x1, 'index': 0, 'value': '00D0271E'},
    {'name': 'ランクMAX', 'pattern': '4801144A680200B9E00313AAFD7B43A9F44F42A9', 'offset': 0x34, 'index': 11, 'value': '1400A8D2'},
    {'name': 'ガチャスキ', 'pattern': '14FF4301D1F85F01A9F65702A9F44F03A9FD7B04A9FD030191F40301AA15', 'offset': 0x1, 'index': 0, 'value': 'C0035FD6'},
    {'name': 'オートチェーン', 'pattern': '290100356A', 'offset': -0x64, 'index': 0, 'value': '016A9852'},
    {'name': '単発チェーン', 'pattern': 'c001003668', 'offset': -0x58, 'index': 0, 'value': '016a9852'},
    {'name': 'ツムサイズ', 'pattern': '2401271E', 'offset': -0x24, 'index': 2, 'value': '0849A852'},
    {'name': 'ツム一色', 'pattern': '66010F0008', 'offset': 0x3, 'index': 0, 'value': '0008251e'},
    {'name': 'ツム増量', 'pattern': '290500714B000054', 'offset': 0x0, 'index': 0, 'value': '29250071'},
    {'name': '広告削除', 'pattern': '600C0034', 'offset': -0x48, 'index': 2, 'value': 'C0035FD6'},
    {'name': '利用規約スキップ', 'pattern': 'E800F837FD7B', 'offset': -0x2c, 'index': 5, 'value': '02008052'},
    {'name': '検知アラートスキップ', 'pattern': '3F11007160', 'offset': -0x18, 'index': 0, 'value': 'C0035FD6'},
    {'name': '時間停止', 'pattern': '0101012A', 'offset': 0x38, 'index': 0, 'value': 'C0035FD6'},
    {'name': '即終了', 'pattern': 'C00300347F', 'offset': -0x4, 'index': 0, 'value': '1F2003D5'},
    {'name': '落下速度MAX', 'pattern': '2009201EC1', 'offset': -0x4, 'index': 0, 'value': '00F0271E'},
     {'name': 'ピックアップスキップ', 'pattern': 'd71240f90005', 'offset': -0x34, 'index': 0, 'value': 'c0035fd6'},
    {'name': 'ボム生成チェーン46', 'pattern': '01310B91', 'offset': 0x8, 'index': 0, 'value': 'C8058052'},
    {'name': 'ボム非生成', 'pattern': '68160639', 'offset': -0x18, 'index': 1, 'value': '010440b9'},
    {'name': 'ツム終了', 'pattern': '0028281EE00314AA', 'offset': 0x0, 'index': 2, 'value': 'e003271e'},
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
    ipa_path = "Tsum.ipa"
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
