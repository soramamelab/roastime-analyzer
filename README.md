# ☕ Roastime Analyzer

**日本語** | [English](#english)

[Aillio Bullet Roaster](https://aillio.com/) 専用の焙煎管理ソフト **ROASTIME** で保存した焙煎データを統計的に解析するローカルアプリです。
データはすべてあなたのPC内で処理されます。外部サーバーへの送信は一切ありません。

![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

---

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

**その他の特徴：**
- ROASTIMEのローカルデータを自動検出（フォルダ選択不要）
- バッチハイライト・最新バッチ自動選択
- 日本語 / English 切替対応

---

## データソース

ROASTIMEのローカルデータを自動で読み込みます。

| OS | データパス |
|----|-----------|
| macOS | `~/Library/Application Support/roast-time/roasts/` |
| Windows | `%APPDATA%/roast-time/roasts/` |
| Linux | `~/.config/roast-time/roasts/` |

---

## ダウンロード・インストール

[Releases](https://github.com/soramamelab/roastime-analyzer/releases) から最新版をダウンロードしてください。

### macOS

1. `RoastimeAnalyzer-x.x.x.dmg` をダウンロード
2. DMGファイルを開き、`RoastimeAnalyzer.app` を **アプリケーション** フォルダへドラッグ
3. 初回起動時は右クリック →「開く」を選択（Gatekeeperの警告を回避）

### Windows

1. `RoastimeAnalyzer_Setup.exe` をダウンロード
2. インストーラーを実行してウィザードに従う
3. スタートメニューまたはデスクトップのショートカットから起動

### Linux (Ubuntu / Debian)

```bash
sudo dpkg -i roastime-analyzer_x.x.x_all.deb
```

インストール後はターミナルまたはアプリケーションメニューから起動：

```bash
roastime-analyzer
```

---

## 使い方

1. アプリを起動すると ROASTIMEのデータが自動で読み込まれます
2. 豆・バッチ量・日付でフィルタしながら各タブで解析
3. **「最新バッチを自動選択」** をオンにすると、焙煎直後に自動でデータが更新される

---

## 動作要件

- **ROASTIME** がインストールされていること（データの自動検出のため）
- macOS 11.0 以降 / Windows 10 以降 / Ubuntu 20.04 以降

---

## ライセンス

MIT License

---

---

<a name="english"></a>

# ☕ Roastime Analyzer

**[日本語](#)** | **English**

A local application for statistically analyzing roast data saved by **ROASTIME**, the dedicated roast management software for the [Aillio Bullet Roaster](https://aillio.com/).
All data is processed on your PC. Nothing is sent to any external server.

---

## Features

| Tab | Content |
|-----|---------|
| 📊 Summary | Batch count, bean varieties, avg. roast time/DTR/drop temp, bean & monthly charts |
| 📈 Profile Comparison | IBTS / BT / ET / RoR overlay, TP / YP / FC / SC markers |
| ⚖️ Weight | Weight loss distribution, bean averages, trends |
| 🔍 Correlation | Scatter plots, regression lines, and correlation matrix for any metric pair |
| 🎨 Color Analysis | Whole/Ground color values, Gap analysis, time series, box plots |
| 📋 Batch List | Full data table view |
| 📥 Export | CSV / Excel output, per-bean summary statistics |

**Additional features:**
- Auto-detects ROASTIME local data (no folder selection needed)
- Batch highlight and auto-select latest batch
- Japanese / English UI toggle

---

## Data Source

Roastime Analyzer automatically reads ROASTIME's local data.

| OS | Data Path |
|----|-----------|
| macOS | `~/Library/Application Support/roast-time/roasts/` |
| Windows | `%APPDATA%/roast-time/roasts/` |
| Linux | `~/.config/roast-time/roasts/` |

---

## Download & Install

Download the latest version from [Releases](https://github.com/soramamelab/roastime-analyzer/releases).

### macOS

1. Download `RoastimeAnalyzer-x.x.x.dmg`
2. Open the DMG and drag `RoastimeAnalyzer.app` to your **Applications** folder
3. On first launch, right-click → Open (to bypass Gatekeeper warning)

### Windows

1. Download `RoastimeAnalyzer_Setup.exe`
2. Run the installer and follow the wizard
3. Launch from the Start menu or desktop shortcut

### Linux (Ubuntu / Debian)

```bash
sudo dpkg -i roastime-analyzer_x.x.x_all.deb
```

After installation, launch from the terminal or application menu:

```bash
roastime-analyzer
```

---

## Usage

1. Launch the app — ROASTIME data is loaded automatically
2. Filter by bean, batch weight, or date range and explore each tab
3. Enable **"Auto-select latest batch"** to automatically refresh data right after a roast

---

## Requirements

- **ROASTIME** must be installed (for automatic data detection)
- macOS 11.0+ / Windows 10+ / Ubuntu 20.04+

---

## License

MIT License
