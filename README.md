# ☕ RoastimeAnalyzer

Aillio Bullet の焙煎ログ解析アプリ。Roastime のローカルデータを自動で読み込み、焙煎プロファイルの比較・分析ができます。

**データはすべてPC内で処理されます。外部には送信されません。**

## 機能

| タブ | 内容 |
|------|------|
| 📊 サマリー | バッチ数、豆の種類、平均焙煎時間・DTR・ドロップ温度、豆別/月別チャート |
| 📈 プロファイル比較 | IBTS / BT / ET / RoR のオーバーレイ表示、TP・YP・FC・SC マーカー |
| ⚖️ 重量 | 重量減少率の分布・豆別平均・トレンド |
| 🔍 相関分析 | 任意の指標ペアの散布図・回帰直線・相関行列 |
| 🎨 カラー分析 | Whole / Ground カラー値、Gap 分析・時系列・箱ひげ図 |
| 📋 バッチ一覧 | 全データのテーブル表示 |
| 📥 エクスポート | CSV / Excel 出力、豆別サマリー統計 |

## フィルタ

- 豆の種類
- バッチ量（範囲指定）
- 日付範囲
- テストバッチ除外（キーワード指定）
- バッチハイライト（最新バッチ自動選択対応）

## データソース

Roastime のローカルデータを自動検出して読み込みます（フォルダ選択不要）。

| OS | パス |
|----|------|
| macOS | `~/Library/Application Support/roast-time/roasts/` |
| Windows | `%APPDATA%/roast-time/roasts/` |
| Linux | `~/.config/roast-time/roasts/` |

## インストール・起動

### Python から直接実行

```bash
pip install streamlit plotly pandas statsmodels openpyxl
streamlit run app.py
```

### macOS アプリ（.dmg）

[Releases](https://github.com/mkuriya4989/roastime-analyzer/releases) からダウンロードしてください。

### Linux（.deb）

[Releases](https://github.com/mkuriya4989/roastime-analyzer/releases) から `.deb` をダウンロードしてインストールできます。

```bash
sudo dpkg -i roastime-analyzer_1.0.0_all.deb
roastime-analyzer
```

## ビルド（開発者向け）

### macOS (.dmg)

```bash
pip install pyinstaller
python -m PyInstaller RoastimeAnalyzer_mac.spec --noconfirm
hdiutil create -volname "RoastimeAnalyzer" -srcfolder dist/RoastimeAnalyzer.app -ov -format UDZO dist/RoastimeAnalyzer.dmg
```

### Linux (.deb)

```bash
bash build-deb.sh
```

## 言語

日本語 / English 切替対応

## ライセンス

MIT
