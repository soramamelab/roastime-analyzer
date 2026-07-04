import json
import os
import glob
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ── i18n ─────────────────────────────────────────────────────────────────────
_TEXTS = {
    "ja": {
        "page_title": "Roastime 焙煎ログ解析",
        "app_title": "☕ Roastime 焙煎ログ解析",
        "app_caption": "データはすべてこのPC内で処理されます。外部には送信されません。",
        "lang_label": "Language / 言語",
        "sidebar_load_header": "データ読み込み",
        "btn_load": "読み込む",
        "btn_quit": "⏹ アプリを終了",
        "quit_title": "アプリを終了しました",
        "quit_body": "このタブを閉じてください",
        "loading": "読み込み中...",
        "loaded_n": "{n} バッチを読み込みました",
        "auto_loaded_toast": "ローカルデータを自動で読み込みました（{n} バッチ）",
        "no_data_info": "Roastimeのデータが見つかりません。",
        "chk_exclude_test": "テストバッチを除外",
        "input_exclude_kw": "除外キーワード（カンマ区切り）",
        "input_exclude_kw_help": "焙煎名にこれらのキーワードが含まれるバッチを除外します",
        "sidebar_filter_header": "フィルタ",
        "filter_beans": "豆を選択（空=全て）",
        "filter_batch_size": "バッチ量 (g)",
        "filter_date": "日付範囲",
        "sidebar_highlight_header": "バッチを指定してハイライト",
        "chk_use_latest": "最新バッチを自動選択",
        "use_latest_caption": "🟢 最新バッチをハイライト中",
        "latest_caption": "最新: {label}",
        "batch_select": "バッチ選択",
        "batch_none": "（なし）",
        "selected_batch": "選択バッチ",
        # tabs
        "tab_summary": "📊 サマリー",
        "tab_profile": "📈 プロファイル比較",
        "tab_weight": "⚖️ 重量",
        "tab_corr": "🔍 相関分析",
        "tab_color": "🎨 カラー分析",
        "tab_batch": "📋 バッチ一覧",
        "tab_export": "📥 エクスポート",
        # summary
        "metric_batches": "バッチ数",
        "metric_beans_kinds": "豆の種類",
        "metric_avg_time": "平均焙煎時間",
        "metric_avg_dtr": "平均DTR",
        "metric_avg_drop": "平均ドロップ温度",
        "chart_bean_count": "豆別 バッチ数",
        "chart_month_count": "月別 バッチ数",
        "col_bean": "豆",
        "col_batch_count": "バッチ数",
        "col_month": "月",
        # profile
        "profile_overlay": "プロファイル オーバーレイ",
        "profile_select_beans": "比較する豆を選択",
        "profile_left_y": "左Y軸（主軸）",
        "profile_right_y": "右Y軸（第2軸）",
        "profile_line_style": "センサーごとに色とラベルで区別されます",
        "profile_max_slider": "最大表示バッチ数（豆ごと）",
        "profile_tp": "中点 (TP)",
        "profile_yp": "イエローイング (YP)",
        "profile_fc": "1ハゼ (FC)",
        "profile_sc": "2ハゼ (SC)",
        "profile_no_sensor": "表示するセンサーを選択してください。",
        "profile_xaxis": "経過時間 (秒)",
        # weight
        "weight_header": "重量減少分析",
        "weight_avg_loss": "平均重量減少",
        "weight_median": "中央値 {v:.1f}%",
        "weight_sd": "SD",
        "weight_bean_avg_loss": "豆別 平均重量減少率",
        "weight_loss_dist": "重量減少率の分布",
        "weight_loss_trend": "同一豆の重量減少推移",
        "weight_select_bean": "豆を選択",
        "data_insufficient": "データが不足しています。",
        "col_avg": "平均",
        "col_sd": "SD",
        "col_n": "n",
        "label_date": "日付",
        "label_weight_loss_pct": "重量減少率 (%)",
        # correlation
        "corr_header": "指標間の相関",
        "corr_x": "X軸",
        "corr_y": "Y軸",
        "corr_coeff": "相関係数 (Pearson r)",
        "corr_help": "2つの指標がどれだけ連動するかを示す値です。"
                     "+1 に近い＝一方が増えると他方も増える、"
                     "-1 に近い＝一方が増えると他方は減る、"
                     "0 に近い＝関連が弱い。"
                     "目安: |0.7| 以上＝強い相関、|0.4〜0.7|＝中程度、|0.4| 未満＝弱い",
        "corr_matrix": "相関行列",
        "corr_matrix_caption": "すべての指標ペアの相関係数を一覧表示。赤＝正の相関、青＝負の相関、白＝関連が弱い。",
        "corr_filter_hint": "データが不足しています。フィルタを緩めてください。",
        "nc_weight_loss": "重量減少率 (%)",
        "nc_roast_time": "焙煎時間 (秒)",
        "nc_fc_temp": "FC温度 (°C)",
        "nc_drop_temp": "ドロップ温度 (°C)",
        "nc_dtr": "DTR (%)",
        "nc_color_whole": "カラー Whole",
        "nc_color_ground": "カラー Ground",
        "nc_fc_time": "FC時間 (秒)",
        "nc_ambient_temp": "室温 (°C)",
        "nc_humidity": "湿度 (%)",
        "nc_preheat_temp": "予熱温度 (°C)",
        "nc_charge_bt": "投入BT温度 (°C)",
        "nc_charge_ibts": "投入IBTS温度 (°C)",
        "nc_batch_size": "バッチ量 (g)",
        # color
        "color_header": "カラー分析",
        "color_no_data": "カラーデータがありません。",
        "color_batches": "バッチ数（カラーあり）",
        "color_avg_whole": "平均 Whole",
        "color_avg_ground": "平均 Ground",
        "color_avg_gap": "平均 Gap (Ground−Whole)",
        "color_avg_gap_help": "正の値 = Groundの方が明るい（典型的）",
        "color_gap_sd": "Gap 標準偏差",
        "color_gap_caption": "**Gap = Ground − Whole**：正の値はGroundが明るい（浅煎り側）。"
                             "Gap が大きいほど焙煎の表面と内部の色差が大きい。",
        "color_hl_missing": "選択バッチにカラー {fields} のデータがないため、ハイライトは表示されません。",
        "color_wvg": "Whole vs Ground（散布図）",
        "color_gap_dist": "Gap (Ground − Whole) の分布",
        "color_gap_box": "豆別 Gap 分布（箱ひげ図）",
        "color_gap_trend": "Gap の時系列推移",
        "color_gap_corr": "Gap と焙煎指標の相関",
        "color_select_all": "（全て）",
        "color_select_bean": "豆を選択（全て = 全バッチ）",
        "color_compare": "比較指標",
        "corr_coeff_label": "相関係数 ({a} vs {b})",
        # batch list
        "batch_header": "バッチ一覧 ({n}件)",
        "dc_date": "日付",
        "dc_bean": "豆",
        "dc_weight_in": "投入量(g)",
        "dc_weight_out": "排出量(g)",
        "dc_weight_loss": "重量減少(%)",
        "dc_fc_temp": "FC温度(°C)",
        "dc_drop_temp": "ドロップ温度(°C)",
        "dc_roast_time": "焙煎時間(秒)",
        "dc_dtr": "DTR(%)",
        "dc_color_whole": "カラー Whole",
        "dc_color_ground": "カラー Ground",
        "dc_ambient_temp": "室温(°C)",
        "dc_humidity": "湿度(%)",
        "dc_preheat": "予熱(°C)",
        "dc_roast_number": "焙煎番号",
        # export
        "export_header": "データのエクスポート",
        "export_desc": "フィルタ済みのデータをCSVまたはExcelでダウンロードします。",
        "export_csv": "📥 CSVダウンロード",
        "export_excel": "📥 Excelダウンロード",
        "export_excel_hint": "Excelエクスポートには `pip install openpyxl` が必要です。",
        "export_summary_header": "豆別サマリー統計",
        "export_summary_csv": "📥 サマリーCSV",
        "sum_batches": "バッチ数",
        "sum_avg_loss": "平均重量減少",
        "sum_sd_loss": "SD重量減少",
        "sum_avg_time": "平均焙煎時間",
        "sum_avg_dtr": "平均DTR",
        "sum_avg_drop": "平均ドロップ温度",
        "sum_avg_fc": "平均FC温度",
        # copyright / donate
        "copyright": "© 2026 SORAMAME LAB INC.\nAll rights reserved.",
        "donate_title": "☕ Roastime Analyzerを気に入っていただけましたか？",
        "donate_body": "株式会社宙豆ラボ（SORAMAME LAB INC.）が開発・維持しているこのアプリを気に入っていただけたなら、開発費へのご寄付をいただけると大変励みになります。",
        "donate_btn": "💛 PayPalで寄付する",
        "donate_skip": "また今度",
        "donate_donated": "もう寄付しました",
    },
    "en": {
        "page_title": "Roastime Roast Log Analysis",
        "app_title": "☕ Roastime Roast Log Analysis",
        "app_caption": "All data is processed locally on this PC. Nothing is sent externally.",
        "lang_label": "Language / 言語",
        "sidebar_load_header": "Load Data",
        "btn_load": "Load",
        "btn_quit": "⏹ Quit App",
        "quit_title": "App has been closed",
        "quit_body": "You can close this tab",
        "loading": "Loading...",
        "loaded_n": "Loaded {n} batches",
        "auto_loaded_toast": "Auto-loaded local data ({n} batches)",
        "no_data_info": "No Roastime data found.",
        "chk_exclude_test": "Exclude test batches",
        "input_exclude_kw": "Exclude keywords (comma-separated)",
        "input_exclude_kw_help": "Exclude batches whose name contains these keywords",
        "sidebar_filter_header": "Filter",
        "filter_beans": "Select beans (empty = all)",
        "filter_batch_size": "Batch size (g)",
        "filter_date": "Date range",
        "sidebar_highlight_header": "Highlight a Batch",
        "chk_use_latest": "Auto-select latest batch",
        "use_latest_caption": "🟢 Highlighting latest batch",
        "latest_caption": "Latest: {label}",
        "batch_select": "Batch",
        "batch_none": "(None)",
        "selected_batch": "Selected Batch",
        # tabs
        "tab_summary": "📊 Summary",
        "tab_profile": "📈 Profile Comparison",
        "tab_weight": "⚖️ Weight",
        "tab_corr": "🔍 Correlation",
        "tab_color": "🎨 Color Analysis",
        "tab_batch": "📋 Batch List",
        "tab_export": "📥 Export",
        # summary
        "metric_batches": "Batches",
        "metric_beans_kinds": "Bean Varieties",
        "metric_avg_time": "Avg Roast Time",
        "metric_avg_dtr": "Avg DTR",
        "metric_avg_drop": "Avg Drop Temp",
        "chart_bean_count": "Batches by Bean",
        "chart_month_count": "Batches by Month",
        "col_bean": "Bean",
        "col_batch_count": "Batches",
        "col_month": "Month",
        # profile
        "profile_overlay": "Profile Overlay",
        "profile_select_beans": "Select beans to compare",
        "profile_left_y": "Left Y-axis (primary)",
        "profile_right_y": "Right Y-axis (secondary)",
        "profile_line_style": "Sensors are distinguished by color and label",
        "profile_max_slider": "Max batches per bean",
        "profile_tp": "Turning Point (TP)",
        "profile_yp": "Yellowing (YP)",
        "profile_fc": "1st Crack (FC)",
        "profile_sc": "2nd Crack (SC)",
        "profile_no_sensor": "Select a sensor to display.",
        "profile_xaxis": "Elapsed Time (sec)",
        # weight
        "weight_header": "Weight Loss Analysis",
        "weight_avg_loss": "Avg Weight Loss",
        "weight_median": "Median {v:.1f}%",
        "weight_sd": "SD",
        "weight_bean_avg_loss": "Avg Weight Loss by Bean",
        "weight_loss_dist": "Weight Loss Distribution",
        "weight_loss_trend": "Weight Loss Trend (same bean)",
        "weight_select_bean": "Select bean",
        "data_insufficient": "Insufficient data.",
        "col_avg": "Avg",
        "col_sd": "SD",
        "col_n": "n",
        "label_date": "Date",
        "label_weight_loss_pct": "Weight Loss (%)",
        # correlation
        "corr_header": "Correlation Analysis",
        "corr_x": "X-axis",
        "corr_y": "Y-axis",
        "corr_coeff": "Correlation (Pearson r)",
        "corr_help": "Shows how closely two metrics move together. "
                     "+1 = both increase together, "
                     "-1 = one increases while the other decreases, "
                     "0 = weak relationship. "
                     "Guide: |0.7|+ = strong, |0.4–0.7| = moderate, <|0.4| = weak",
        "corr_matrix": "Correlation Matrix",
        "corr_matrix_caption": "Correlation coefficients for all metric pairs. Red = positive, Blue = negative, White = weak.",
        "corr_filter_hint": "Insufficient data. Try widening the filter.",
        "nc_weight_loss": "Weight Loss (%)",
        "nc_roast_time": "Roast Time (sec)",
        "nc_fc_temp": "FC Temp (°C)",
        "nc_drop_temp": "Drop Temp (°C)",
        "nc_dtr": "DTR (%)",
        "nc_color_whole": "Color Whole",
        "nc_color_ground": "Color Ground",
        "nc_fc_time": "FC Time (sec)",
        "nc_ambient_temp": "Ambient Temp (°C)",
        "nc_humidity": "Humidity (%)",
        "nc_preheat_temp": "Preheat Temp (°C)",
        "nc_charge_bt": "Charge BT (°C)",
        "nc_charge_ibts": "Charge IBTS (°C)",
        "nc_batch_size": "Batch Size (g)",
        # color
        "color_header": "Color Analysis",
        "color_no_data": "No color data available.",
        "color_batches": "Batches (with color)",
        "color_avg_whole": "Avg Whole",
        "color_avg_ground": "Avg Ground",
        "color_avg_gap": "Avg Gap (Ground−Whole)",
        "color_avg_gap_help": "Positive = Ground is lighter (typical)",
        "color_gap_sd": "Gap Std Dev",
        "color_gap_caption": "**Gap = Ground − Whole**: Positive means Ground is lighter. "
                             "A larger Gap indicates greater color difference between surface and interior.",
        "color_hl_missing": "Selected batch has no color {fields} data; highlight not shown.",
        "color_wvg": "Whole vs Ground (scatter)",
        "color_gap_dist": "Gap (Ground − Whole) Distribution",
        "color_gap_box": "Gap Distribution by Bean (box plot)",
        "color_gap_trend": "Gap Time Series",
        "color_gap_corr": "Gap vs Roast Metrics",
        "color_select_all": "(All)",
        "color_select_bean": "Select bean (All = all batches)",
        "color_compare": "Compare metric",
        "corr_coeff_label": "Correlation ({a} vs {b})",
        # batch list
        "batch_header": "Batch List ({n})",
        "dc_date": "Date",
        "dc_bean": "Bean",
        "dc_weight_in": "Weight In (g)",
        "dc_weight_out": "Weight Out (g)",
        "dc_weight_loss": "Weight Loss (%)",
        "dc_fc_temp": "FC Temp (°C)",
        "dc_drop_temp": "Drop Temp (°C)",
        "dc_roast_time": "Roast Time (sec)",
        "dc_dtr": "DTR (%)",
        "dc_color_whole": "Color Whole",
        "dc_color_ground": "Color Ground",
        "dc_ambient_temp": "Ambient Temp (°C)",
        "dc_humidity": "Humidity (%)",
        "dc_preheat": "Preheat (°C)",
        "dc_roast_number": "Roast #",
        # export
        "export_header": "Export Data",
        "export_desc": "Download filtered data as CSV or Excel.",
        "export_csv": "📥 Download CSV",
        "export_excel": "📥 Download Excel",
        "export_excel_hint": "Excel export requires `pip install openpyxl`.",
        "export_summary_header": "Summary Statistics by Bean",
        "export_summary_csv": "📥 Summary CSV",
        "sum_batches": "Batches",
        "sum_avg_loss": "Avg Weight Loss",
        "sum_sd_loss": "SD Weight Loss",
        "sum_avg_time": "Avg Roast Time",
        "sum_avg_dtr": "Avg DTR",
        "sum_avg_drop": "Avg Drop Temp",
        "sum_avg_fc": "Avg FC Temp",
        # copyright / donate
        "copyright": "© 2026 SORAMAME LAB INC.\nAll rights reserved.",
        "donate_title": "☕ Enjoying Roastime Analyzer?",
        "donate_body": "Roastime Analyzer is developed and maintained by SORAMAME LAB INC. (株式会社宙豆ラボ). If you find it useful, please consider supporting the development with a small donation.",
        "donate_btn": "💛 Donate via PayPal",
        "donate_skip": "Maybe later",
        "donate_donated": "I already donated",
    },
}

# ── 設定の永続化 ──────────────────────────────────────────────────────────────
_CONFIG_PATH = os.path.expanduser("~/.config/roastime-analyzer/config.json")
_ROAST_DIR = os.path.expanduser("~/Library/Application Support/roast-time/roasts")
_PAYPAL_URL = "https://paypal.me/soramamelab"
_DONATE_INTERVAL_DAYS = 30
_DONATED_INTERVAL_DAYS = 365


@st.dialog(" ")
def _show_donate_dialog(T: dict) -> None:
    st.markdown(f"### {T['donate_title']}")
    st.write(T["donate_body"])
    st.markdown(f"[{T['donate_btn']}]({_PAYPAL_URL})", unsafe_allow_html=False)
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(T["donate_skip"], use_container_width=True):
            st.session_state.last_donate_prompt = datetime.now().isoformat()
            st.session_state.donated = False
            _save_config()
            st.rerun()
    with col2:
        if st.button(T["donate_donated"], use_container_width=True, type="secondary"):
            st.session_state.last_donate_prompt = datetime.now().isoformat()
            st.session_state.donated = True
            _save_config()
            st.rerun()


def _maybe_show_donate(T: dict) -> None:
    last = st.session_state.get("last_donate_prompt", "")
    if last:
        try:
            days = (datetime.now() - datetime.fromisoformat(last)).days
            interval = _DONATED_INTERVAL_DAYS if st.session_state.get("donated", False) else _DONATE_INTERVAL_DAYS
            if days < interval:
                return
        except Exception:
            pass
    _show_donate_dialog(T)


def _get_roast_dir():
    import platform
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/roast-time/roasts")
    elif system == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "roast-time", "roasts")
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return os.path.join(xdg, "roast-time", "roasts")


def _load_config() -> dict:
    try:
        with open(_CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_config() -> None:
    cfg = {
        "exclude_test": st.session_state.get("exclude_test_val", True),
        "use_latest": st.session_state.get("use_latest", False),
        "exclude_keywords": st.session_state.get("exclude_keywords", "test, preheat, NG"),
        "lang": st.session_state.get("lang", "ja"),
        "last_donate_prompt": st.session_state.get("last_donate_prompt", ""),
        "donated": st.session_state.get("donated", False),
    }
    try:
        os.makedirs(os.path.dirname(_CONFIG_PATH), exist_ok=True)
        with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


st.set_page_config(page_title="Roastime Analyzer", page_icon="☕", layout="wide")

# ── セッション状態の初期化 ────────────────────────────────────────────────────
if "initialized" not in st.session_state:
    _cfg = _load_config()
    st.session_state.exclude_test_val = _cfg.get("exclude_test", True)
    st.session_state.use_latest = _cfg.get("use_latest", False)
    st.session_state.exclude_keywords = _cfg.get("exclude_keywords", "test, preheat, NG")
    st.session_state.lang = _cfg.get("lang", "ja")
    st.session_state.last_donate_prompt = _cfg.get("last_donate_prompt", "")
    st.session_state.donated = _cfg.get("donated", False)
    st.session_state.initialized = True

# ── 言語選択 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    _lang_options = ["ja", "en"]
    _lang_labels = {"ja": "日本語", "en": "English"}
    _prev_lang = st.session_state.get("lang", "ja")
    st.radio(
        _TEXTS[_prev_lang]["lang_label"],
        _lang_options,
        format_func=lambda x: _lang_labels[x],
        key="lang",
        horizontal=True,
    )
    if st.session_state.lang != _prev_lang:
        _save_config()
        st.rerun()

T = _TEXTS[st.session_state.get("lang", "ja")]

st.title(T["app_title"])
st.caption(T["app_caption"])

with st.sidebar:
    st.header(T["sidebar_load_header"])
    exclude_test = st.checkbox(T["chk_exclude_test"], key="exclude_test_val")
    if exclude_test:
        st.text_input(
            T["input_exclude_kw"],
            key="exclude_keywords",
            help=T["input_exclude_kw_help"],
        )
    load_btn = st.button(T["btn_load"], type="primary", use_container_width=True)

    st.divider()
    if st.button(T["btn_quit"], use_container_width=True):
        _save_config()
        import threading, signal
        def _shutdown():
            import time; time.sleep(2)
            os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=_shutdown, daemon=True).start()
        import streamlit.components.v1 as components
        _quit_title = T["quit_title"]
        _quit_body = T["quit_body"]
        components.html(f"""<script>
        document.querySelectorAll('header,[data-testid="stSidebar"],[data-testid="stAppViewBlockContainer"]')
            .forEach(function(e){{e.style.display='none';}});
        var d=window.parent.document;
        d.title='Roastime Analyzer';
        var b=d.body;b.innerHTML='';b.style.cssText='margin:0;background:#1a1a2e;display:flex;align-items:center;justify-content:center;height:100vh';
        var h=d.createElement('div');h.style.cssText='text-align:center;color:#aaa;font-family:sans-serif';
        h.innerHTML='<h2>☕ {_quit_title}</h2><p>{_quit_body}</p>';
        b.appendChild(h);
        </script>""", height=0)
        st.stop()

    st.divider()
    st.caption(T["copyright"])

# ── 寄付ダイアログ ─────────────────────────────────────────────────────────────
_maybe_show_donate(T)

# ── データ解析 ─────────────────────────────────────────────────────────────────

# ctrlType: 0=Power, 1=Fan, 2=Drum
_CTRL_NAMES = {0: "Power", 1: "Fan", 2: "Drum"}


def parse_roastime(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        try:
            d = json.load(f)
        except Exception:
            return None

    sample_rate = d.get("sampleRate", 2)
    start_idx = d.get("roastStartIndex", 0)
    end_idx = d.get("roastEndIndex", 0)
    if not end_idx:
        return None

    bean_temp = d.get("beanTemperature", [])
    drum_temp = d.get("drumTemperature", [])
    exit_temp = d.get("exitTemperature", [])
    bean_ror = d.get("beanDerivative", [])
    ibts_ror = d.get("ibtsDerivative", [])

    total_samples = end_idx - start_idx
    total_time_sec = total_samples / sample_rate if sample_rate else 0

    fc_idx = d.get("indexFirstCrackStart", 0)
    sc_idx = d.get("indexSecondCrackStart", 0)
    yp_idx = d.get("indexYellowingStart", 0)

    def temp_at(arr, idx):
        if idx and 0 < idx < len(arr):
            return round(arr[idx], 1)
        return None

    def time_at_idx(idx):
        if idx and idx > start_idx:
            return round((idx - start_idx) / sample_rate, 1)
        return None

    fc_time = time_at_idx(fc_idx)
    dtr = round((total_time_sec - fc_time) / total_time_sec * 100, 1) if (total_time_sec and fc_time and total_time_sec > 0) else None

    w_in = float(d.get("weightGreen", 0) or 0)
    w_out = float(d.get("weightRoasted", 0) or 0)
    loss_raw = round((w_in - w_out) / w_in * 100, 2) if w_in > 0 else None
    loss = loss_raw if loss_raw is not None and 0 <= loss_raw < 50 else None

    dt_ms = d.get("dateTime", 0)
    try:
        date = datetime.fromtimestamp(dt_ms / 1000)
        date_str = date.strftime("%Y-%m-%d")
        date_obj = date.date()
    except Exception:
        date_str = ""
        date_obj = None

    whole_color_raw = d.get("wholeColorLevel")
    ground_color_raw = d.get("groundColorLevel")
    whole_color = None
    ground_color = None
    if isinstance(whole_color_raw, dict):
        whole_color = whole_color_raw.get("value")
    elif isinstance(whole_color_raw, (int, float)):
        whole_color = whole_color_raw
    if isinstance(ground_color_raw, dict):
        ground_color = ground_color_raw.get("value")
    elif isinstance(ground_color_raw, (int, float)):
        ground_color = ground_color_raw

    if whole_color is not None and (whole_color <= 0 or whole_color > 120):
        whole_color = None
    if ground_color is not None and (ground_color <= 0 or ground_color > 120):
        ground_color = None

    return {
        "title": (d.get("roastName") or "").strip() or "Unknown",
        "date": date_obj,
        "date_str": date_str,
        "weight_in": w_in,
        "weight_out": w_out,
        "weight_loss_pct": loss,
        "charge_bt": d.get("beanChargeTemperature"),
        "drop_bt": d.get("beanDropTemperature"),
        "drum_charge": d.get("drumChargeTemperature"),
        "drum_drop": d.get("drumDropTemperature"),
        "fc_bt": temp_at(bean_temp, fc_idx),
        "fc_time_sec": fc_time,
        "yp_time_sec": time_at_idx(yp_idx),
        "total_time_sec": round(total_time_sec, 1),
        "dev_time_ratio": dtr,
        "whole_color": whole_color,
        "ground_color": ground_color,
        "preheat_temp": d.get("preheatTemperature") or d.get("preheatTemperature"),
        "ambient_temp": d.get("ambient") or None,
        "ambient_humidity": d.get("humidity") or None,
        "roast_number": d.get("roastNumber"),
        "sample_rate": sample_rate,
        "start_idx": start_idx,
        "end_idx": end_idx,
        "fc_idx": fc_idx,
        "sc_idx": sc_idx,
        "yp_idx": yp_idx,
        "bean_temp": bean_temp,
        "drum_temp": drum_temp,
        "exit_temp": exit_temp,
        "bean_ror": bean_ror,
        "ibts_ror": ibts_ror,
        "actions": d.get("actions", {}),
        "uid": d.get("uid", ""),
        "file": os.path.basename(path),
    }


@st.cache_data
def load_roasts(roast_dir, excl_test, exclude_keywords_str=""):
    if not os.path.isdir(roast_dir):
        return []
    files = sorted(os.listdir(roast_dir))
    keywords = [k.strip().lower() for k in exclude_keywords_str.split(",") if k.strip()] if excl_test else []
    records = []
    for fname in files:
        path = os.path.join(roast_dir, fname)
        if not os.path.isfile(path):
            continue
        r = parse_roastime(path)
        if r is None:
            continue
        if keywords:
            name_lower = r["title"].lower()
            if any(kw in name_lower for kw in keywords):
                continue
        records.append(r)
    return records


# ── 読み込み実行 ───────────────────────────────────────────────────────────────
roast_dir = _get_roast_dir()

if "records" not in st.session_state:
    st.session_state.records = []
    if os.path.isdir(roast_dir):
        st.session_state.records = load_roasts(
            roast_dir, st.session_state.exclude_test_val,
            st.session_state.get("exclude_keywords", ""),
        )
        st.session_state["_auto_loaded"] = True

if load_btn:
    with st.spinner(T["loading"]):
        load_roasts.clear()
        st.session_state.records = load_roasts(
            roast_dir, exclude_test,
            st.session_state.get("exclude_keywords", ""),
        )
    _save_config()
    st.success(T["loaded_n"].format(n=len(st.session_state.records)))

if st.session_state.pop("_auto_loaded", False):
    st.toast(T["auto_loaded_toast"].format(n=len(st.session_state.records)), icon="📂")

records = st.session_state.records

if not records:
    st.info(T["no_data_info"])
    st.stop()

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date_str"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# ── サイドバー フィルタ ────────────────────────────────────────────────────────
with st.sidebar:
    st.divider()
    st.header(T["sidebar_filter_header"])
    beans = sorted(df["title"].unique())
    selected_beans = st.multiselect(T["filter_beans"], beans)
    weight_vals = df["weight_in"].dropna()
    weight_vals = weight_vals[weight_vals > 0]
    if len(weight_vals):
        w_min = int(weight_vals.min())
        batch_size_range = st.slider(
            T["filter_batch_size"], w_min, 1200, (w_min, 1200),
            step=10, format="%dg",
        )
    else:
        batch_size_range = None
    if df["date"].notna().any():
        min_d = df["date"].min().date()
        max_d = df["date"].max().date()
        date_range = st.date_input(T["filter_date"], value=(min_d, max_d))
    else:
        date_range = None

filtered = df.copy()
if selected_beans:
    filtered = filtered[filtered["title"].isin(selected_beans)]
if batch_size_range:
    filtered = filtered[
        (filtered["weight_in"] >= batch_size_range[0]) &
        (filtered["weight_in"] <= batch_size_range[1])
    ]
if date_range and len(date_range) == 2:
    filtered = filtered[
        (filtered["date"].dt.date >= date_range[0]) &
        (filtered["date"].dt.date <= date_range[1])
    ]

# ── サイドバー バッチハイライト ────────────────────────────────────────────────
with st.sidebar:
    st.divider()
    st.header(T["sidebar_highlight_header"])
    use_latest = st.checkbox(T["chk_use_latest"], value=False, key="use_latest")
    if use_latest:
        st.caption(T["use_latest_caption"])
    batch_labels = [T["batch_none"]] + [
        f"{r['date_str']}  {r['title']}"
        for _, r in filtered.sort_values("date", ascending=False).iterrows()
    ]
    if use_latest and len(batch_labels) > 1:
        selected_label = batch_labels[1]
        st.caption(T["latest_caption"].format(label=selected_label))
    else:
        selected_label = st.selectbox(
            T["batch_select"], batch_labels, key="highlight_batch",
            disabled=use_latest,
        )

highlight_row = None
if selected_label != T["batch_none"]:
    date_part, title_part = selected_label.split("  ", 1)
    match = filtered[(filtered["date_str"] == date_part) & (filtered["title"] == title_part)]
    if not match.empty:
        highlight_row = match.iloc[0].copy()
        wc = highlight_row.get("whole_color")
        gc = highlight_row.get("ground_color")
        if pd.notna(wc) and pd.notna(gc):
            highlight_row["gap"] = round(gc - wc, 1)

_HL = T["selected_batch"]


def add_highlight(fig, x_col, y_col, label=None):
    if label is None:
        label = _HL
    if highlight_row is None:
        return fig
    xv = highlight_row.get(x_col)
    yv = highlight_row.get(y_col)
    if xv is None or yv is None or pd.isna(xv) or pd.isna(yv):
        return fig
    fig.add_trace(go.Scatter(
        x=[xv], y=[yv],
        mode="markers+text",
        marker=dict(symbol="star", size=18, color="#D85A30",
                    line=dict(color="white", width=1.5)),
        text=[label],
        textposition="top center",
        textfont=dict(size=11, color="#D85A30"),
        name=label,
        showlegend=True,
    ))
    return fig


def add_highlight_vline(fig, col, label=None):
    if label is None:
        label = _HL
    if highlight_row is None:
        return fig
    v = highlight_row.get(col)
    if v is None or pd.isna(v):
        return fig
    fig.add_vline(x=float(v), line_color="#D85A30", line_width=2, line_dash="solid",
                  annotation_text=f"▲ {label} ({v:.1f})",
                  annotation_position="top right",
                  annotation_font=dict(color="#D85A30", size=11))
    return fig


# ── タブ ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab_wt, tab3, tab4, tab5, tab6 = st.tabs(
    [T["tab_summary"], T["tab_profile"], T["tab_weight"], T["tab_corr"], T["tab_color"], T["tab_batch"], T["tab_export"]]
)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: サマリー
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    n = len(filtered)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(T["metric_batches"], n)
    col2.metric(T["metric_beans_kinds"], filtered["title"].nunique())

    time_vals = filtered["total_time_sec"].dropna()
    if len(time_vals):
        avg_min = int(time_vals.mean() // 60)
        avg_sec = int(time_vals.mean() % 60)
        col3.metric(T["metric_avg_time"], f"{avg_min}:{avg_sec:02d}")
    else:
        col3.metric(T["metric_avg_time"], "-")

    dtr_vals = filtered["dev_time_ratio"].dropna()
    col4.metric(T["metric_avg_dtr"], f"{dtr_vals.mean():.1f}%" if len(dtr_vals) else "-")

    drop_vals = filtered["drop_bt"].dropna()
    col5.metric(T["metric_avg_drop"], f"{drop_vals.mean():.1f}°C" if len(drop_vals) else "-")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(T["chart_bean_count"])
        bean_counts = filtered["title"].value_counts().reset_index()
        bean_counts.columns = [T["col_bean"], T["col_batch_count"]]
        fig = px.bar(bean_counts, x=T["col_batch_count"], y=T["col_bean"], orientation="h",
                     color_discrete_sequence=["#378ADD"])
        fig.update_layout(height=max(300, len(bean_counts) * 28), yaxis={"categoryorder": "total ascending"}, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader(T["chart_month_count"])
        month_counts = filtered.groupby("month").size().reset_index(name=T["col_batch_count"])
        fig = px.bar(month_counts, x="month", y=T["col_batch_count"], color_discrete_sequence=["#1D9E75"])
        fig.update_layout(xaxis_title=T["col_month"], margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: プロファイル比較
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader(T["profile_overlay"])

    profile_beans = sorted(filtered["title"].unique())
    selected_for_profile = st.multiselect(
        T["profile_select_beans"],
        profile_beans,
        default=profile_beans[:3] if len(profile_beans) >= 3 else profile_beans,
        key="profile_beans",
    )

    available_sensors = ["IBTS", "BT", "ET (Exhaust)", "IBTS RoR", "BT RoR"]
    sensor_styles = {
        "IBTS": None,
        "BT": None,
        "ET (Exhaust)": None,
        "IBTS RoR": None,
        "BT RoR": None,
    }
    sensor_data_key = {
        "IBTS": "drum_temp",
        "BT": "bean_temp",
        "ET (Exhaust)": "exit_temp",
        "IBTS RoR": "ibts_ror",
        "BT RoR": "bean_ror",
    }
    _ror_sensors = {"IBTS RoR", "BT RoR"}

    col_l, col_r = st.columns(2)
    with col_l:
        left_sensors = st.multiselect(
            T["profile_left_y"], available_sensors, default=["IBTS"], key="left_y_sensors",
        )
    with col_r:
        right_sensors = st.multiselect(
            T["profile_right_y"], available_sensors, default=[], key="right_y_sensors",
        )
    right_sensors = [s for s in right_sensors if s not in left_sensors]
    all_sensors = left_sensors + right_sensors

    st.caption(T["profile_line_style"])

    max_profiles = st.slider(T["profile_max_slider"], 1, 10, 3)
    col_tp, col_yp, col_fc, col_sc = st.columns(4)
    with col_tp:
        show_tp = st.checkbox(T["profile_tp"], value=False, key="show_tp")
    with col_yp:
        show_yp = st.checkbox(T["profile_yp"], value=False, key="show_yp")
    with col_fc:
        show_fc = st.checkbox(T["profile_fc"], value=True, key="show_fc")
    with col_sc:
        show_sc = st.checkbox(T["profile_sc"], value=False, key="show_sc")

    if not all_sensors:
        st.info(T["profile_no_sensor"])
    else:
        has_right = len(right_sensors) > 0
        if has_right:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
        else:
            fig = go.Figure()

        colors = px.colors.qualitative.Plotly
        shown = defaultdict(int)
        hl_file = highlight_row["file"] if highlight_row is not None else None
        tp_first = yp_first = fc_first = sc_first = True

        for _, row in filtered.iterrows():
            title = row["title"]
            is_highlight = (row["file"] == hl_file)
            if not is_highlight:
                if title not in selected_for_profile:
                    continue
                if shown[title] >= max_profiles:
                    continue

            sr = row["sample_rate"]
            si = row["start_idx"]
            ei = row["end_idx"]
            if not ei or ei <= si:
                continue

            for sensor in all_sensors:
                data_key = sensor_data_key[sensor]
                y_data = row.get(data_key, [])
                if not y_data or len(y_data) == 0:
                    continue

                y = y_data[si:ei]
                x = [i / sr for i in range(len(y))]

                if sensor in _ror_sensors:
                    y = [max(0, v) for v in y]
                min_len = min(len(x), len(y))
                color_idx = profile_beans.index(title) % len(colors) if title in profile_beans else 0
                dash = sensor_styles.get(sensor)
                suffix = f" [{sensor}]" if len(all_sensors) > 1 else ""
                secondary = sensor in right_sensors

                if is_highlight:
                    trace = go.Scatter(
                        x=x[:min_len], y=y[:min_len], mode="lines",
                        name=f"★ {title[:24]} ({row['date_str']}){suffix}",
                        line=dict(color="#D85A30", width=3, dash=dash),
                        opacity=1.0,
                    )
                else:
                    trace = go.Scatter(
                        x=x[:min_len], y=y[:min_len], mode="lines",
                        name=f"{title[:26]} ({row['date_str']}){suffix}",
                        line=dict(color=colors[color_idx], width=1.5, dash=dash),
                        opacity=0.5,
                    )

                if has_right:
                    fig.add_trace(trace, secondary_y=secondary)
                else:
                    fig.add_trace(trace)

                if sensor == "IBTS":
                    trace_color = "#D85A30" if is_highlight else colors[color_idx]

                    if show_tp and si < ei:
                        bt_slice = y_data[si:ei]
                        valid = [(i, v) for i, v in enumerate(bt_slice) if v and v > 0]
                        if valid:
                            tp_rel, tp_temp = min(valid, key=lambda iv: iv[1])
                            tp_x = tp_rel / sr
                            tp_trace = go.Scatter(
                                x=[tp_x], y=[tp_temp], mode="markers",
                                marker=dict(symbol="triangle-down", size=10, color=trace_color,
                                            line=dict(color="white", width=1.5)),
                                name=T["profile_tp"], showlegend=tp_first,
                                legendgroup="tp",
                                hovertext=f"{title} TP {tp_temp:.1f}°C @ {tp_x:.0f}s",
                                hoverinfo="text",
                            )
                            if has_right:
                                fig.add_trace(tp_trace, secondary_y=secondary)
                            else:
                                fig.add_trace(tp_trace)
                            tp_first = False

                    if show_yp and row["yp_idx"] and row["yp_idx"] > si:
                        yp_rel = row["yp_idx"] - si
                        if yp_rel < len(y_data[si:ei]):
                            yp_x = yp_rel / sr
                            yp_temp = y_data[row["yp_idx"]]
                            if yp_temp and yp_temp > 0:
                                yp_trace = go.Scatter(
                                    x=[yp_x], y=[yp_temp], mode="markers",
                                    marker=dict(symbol="circle", size=10, color=trace_color,
                                                line=dict(color="white", width=1.5)),
                                    name=T["profile_yp"], showlegend=yp_first,
                                    legendgroup="yp",
                                    hovertext=f"{title} YP {yp_temp:.1f}°C @ {yp_x:.0f}s",
                                    hoverinfo="text",
                                )
                                if has_right:
                                    fig.add_trace(yp_trace, secondary_y=secondary)
                                else:
                                    fig.add_trace(yp_trace)
                                yp_first = False

                    if show_fc and row["fc_idx"] and row["fc_idx"] > si:
                        fc_rel = row["fc_idx"] - si
                        if fc_rel < len(y_data[si:ei]):
                            fc_x = fc_rel / sr
                            fc_temp = y_data[row["fc_idx"]]
                            if fc_temp and fc_temp > 0:
                                fc_trace = go.Scatter(
                                    x=[fc_x], y=[fc_temp], mode="markers",
                                    marker=dict(symbol="diamond", size=10, color=trace_color,
                                                line=dict(color="white", width=1.5)),
                                    name=T["profile_fc"], showlegend=fc_first,
                                    legendgroup="fc",
                                    hovertext=f"{title} FC {fc_temp:.1f}°C @ {fc_x:.0f}s",
                                    hoverinfo="text",
                                )
                                if has_right:
                                    fig.add_trace(fc_trace, secondary_y=secondary)
                                else:
                                    fig.add_trace(fc_trace)
                                fc_first = False

                    if show_sc and row["sc_idx"] and row["sc_idx"] > si:
                        sc_rel = row["sc_idx"] - si
                        if sc_rel < len(y_data[si:ei]):
                            sc_x = sc_rel / sr
                            sc_temp = y_data[row["sc_idx"]]
                            if sc_temp and sc_temp > 0:
                                sc_trace = go.Scatter(
                                    x=[sc_x], y=[sc_temp], mode="markers",
                                    marker=dict(symbol="square", size=10, color=trace_color,
                                                line=dict(color="white", width=1.5)),
                                    name=T["profile_sc"], showlegend=sc_first,
                                    legendgroup="sc",
                                    hovertext=f"{title} SC {sc_temp:.1f}°C @ {sc_x:.0f}s",
                                    hoverinfo="text",
                                )
                                if has_right:
                                    fig.add_trace(sc_trace, secondary_y=secondary)
                                else:
                                    fig.add_trace(sc_trace)
                                sc_first = False

            if not is_highlight:
                shown[title] += 1

        left_label = " / ".join(left_sensors) + " (°C)" if left_sensors else ""
        right_label = " / ".join(right_sensors) + " (°C)" if right_sensors else ""

        fig.update_layout(
            xaxis_title=T["profile_xaxis"],
            height=520,
            legend=dict(font=dict(size=10)),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        left_has_ror = any(s in _ror_sensors for s in left_sensors)
        right_has_ror = any(s in _ror_sensors for s in right_sensors)
        if has_right:
            fig.update_yaxes(title_text=left_label, secondary_y=False,
                             rangemode="tozero" if left_has_ror else "normal")
            fig.update_yaxes(title_text=right_label, secondary_y=True,
                             rangemode="tozero" if right_has_ror else "normal")
        else:
            fig.update_yaxes(title_text=left_label,
                             rangemode="tozero" if left_has_ror else "normal")

        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB: 重量
# ══════════════════════════════════════════════════════════════════════════════
with tab_wt:
    st.subheader(T["weight_header"])

    loss_vals = filtered["weight_loss_pct"].dropna()

    c1, c2 = st.columns(2)
    c1.metric(T["weight_avg_loss"], f"{loss_vals.mean():.1f}%" if len(loss_vals) else "-",
              T["weight_median"].format(v=loss_vals.median()) if len(loss_vals) else "")
    c2.metric(T["weight_sd"], f"{loss_vals.std():.2f}%" if len(loss_vals) > 1 else "-")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"**{T['weight_bean_avg_loss']}**")
        bean_loss = (
            filtered.groupby("title")["weight_loss_pct"]
            .agg(["mean", "std", "count"])
            .reset_index()
        )
        bean_loss.columns = [T["col_bean"], T["col_avg"], T["col_sd"], T["col_n"]]
        bean_loss = bean_loss.sort_values(T["col_avg"])
        fig_wl = px.bar(bean_loss, x=T["col_avg"], y=T["col_bean"], orientation="h",
                        error_x=T["col_sd"],
                        color=T["col_avg"],
                        color_continuous_scale=["#378ADD", "#D85A30"],
                        range_color=[10, 32])
        fig_wl = add_highlight_vline(fig_wl, "weight_loss_pct")
        fig_wl.update_layout(height=max(300, len(bean_loss) * 28), yaxis={"categoryorder": "total ascending"}, margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False)
        st.plotly_chart(fig_wl, use_container_width=True)

    with col_b:
        st.markdown(f"**{T['weight_loss_dist']}**")
        fig_wd = px.histogram(filtered.dropna(subset=["weight_loss_pct"]),
                              x="weight_loss_pct", nbins=20,
                              color_discrete_sequence=["#BA7517"],
                              labels={"weight_loss_pct": T["label_weight_loss_pct"]})
        fig_wd = add_highlight_vline(fig_wd, "weight_loss_pct")
        fig_wd.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_wd, use_container_width=True)

    st.divider()
    st.markdown(f"**{T['weight_loss_trend']}**")
    wt_beans = sorted(filtered["title"].unique())
    wt_trend_bean = st.selectbox(T["weight_select_bean"], wt_beans, key="wt_trend_bean")
    wt_bean_df = filtered[filtered["title"] == wt_trend_bean].sort_values("date")
    if len(wt_bean_df):
        fig_wt = px.scatter(wt_bean_df, x="date", y="weight_loss_pct",
                            trendline="ols" if len(wt_bean_df) > 2 else None,
                            labels={"date": T["label_date"], "weight_loss_pct": T["label_weight_loss_pct"]},
                            color_discrete_sequence=["#378ADD"])
        fig_wt = add_highlight(fig_wt, "date", "weight_loss_pct")
        fig_wt.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_wt, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: 相関分析
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader(T["corr_header"])

    num_cols = {
        T["nc_weight_loss"]: "weight_loss_pct",
        T["nc_roast_time"]: "total_time_sec",
        T["nc_fc_temp"]: "fc_bt",
        T["nc_drop_temp"]: "drop_bt",
        T["nc_dtr"]: "dev_time_ratio",
        T["nc_color_whole"]: "whole_color",
        T["nc_color_ground"]: "ground_color",
        T["nc_fc_time"]: "fc_time_sec",
        T["nc_ambient_temp"]: "ambient_temp",
        T["nc_humidity"]: "ambient_humidity",
        T["nc_preheat_temp"]: "preheat_temp",
        T["nc_charge_bt"]: "charge_bt",
        T["nc_charge_ibts"]: "drum_charge",
        T["nc_batch_size"]: "weight_in",
    }

    col_x, col_y = st.columns(2)
    x_label = col_x.selectbox(T["corr_x"], list(num_cols.keys()), index=2)
    y_label = col_y.selectbox(T["corr_y"], list(num_cols.keys()), index=0)

    x_col = num_cols[x_label]
    y_col = num_cols[y_label]

    scatter_df = filtered.dropna(subset=[x_col, y_col])
    if len(scatter_df) > 1:
        fig = px.scatter(
            scatter_df,
            x=x_col, y=y_col,
            color="title",
            hover_data=["date_str", "weight_in"],
            trendline="ols",
            trendline_scope="overall",
            labels={x_col: x_label, y_col: y_label, "title": T["col_bean"]},
        )
        fig = add_highlight(fig, x_col, y_col)
        fig.update_layout(height=480, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

        corr = scatter_df[[x_col, y_col]].corr().iloc[0, 1]
        st.metric(T["corr_coeff"], f"{corr:.3f}", help=T["corr_help"])
    else:
        st.info(T["corr_filter_hint"])

    st.divider()
    st.subheader(T["corr_matrix"])
    st.caption(T["corr_matrix_caption"])
    corr_cols = [c for c in num_cols.values() if c in filtered.columns]
    corr_labels = [k for k, v in num_cols.items() if v in filtered.columns]
    corr_matrix = filtered[corr_cols].corr()
    corr_matrix.index = corr_labels
    corr_matrix.columns = corr_labels
    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1,
        text_auto=".2f",
    )
    fig_corr.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_corr, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: カラー分析
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader(T["color_header"])

    ag = filtered.dropna(subset=["whole_color", "ground_color"]).copy()
    ag = ag[(ag["whole_color"] > 0) & (ag["ground_color"] > 0)]
    ag["gap"] = (ag["ground_color"] - ag["whole_color"]).round(1)

    if ag.empty:
        st.info(T["color_no_data"])
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric(T["color_batches"], len(ag))
        c2.metric(T["color_avg_whole"], f"{ag['whole_color'].mean():.1f}")
        c3.metric(T["color_avg_ground"], f"{ag['ground_color'].mean():.1f}")
        gap_mean = ag["gap"].mean()
        gap_std = ag["gap"].std()
        c4.metric(T["color_avg_gap"], f"{gap_mean:.1f}", help=T["color_avg_gap_help"])
        c5.metric(T["color_gap_sd"], f"{gap_std:.1f}")

        st.caption(T["color_gap_caption"])
        st.divider()

        if highlight_row is not None:
            _hl_wc = highlight_row.get("whole_color")
            _hl_gc = highlight_row.get("ground_color")
            if pd.isna(_hl_wc) or pd.isna(_hl_gc):
                missing = []
                if pd.isna(_hl_wc):
                    missing.append("Whole")
                if pd.isna(_hl_gc):
                    missing.append("Ground")
                st.info(T["color_hl_missing"].format(fields=" / ".join(missing)))

        st.markdown(f"**{T['color_wvg']}**")
        fig = px.scatter(
            ag, x="whole_color", y="ground_color",
            color="title",
            hover_data=["date_str", "gap"],
            labels={"whole_color": T["nc_color_whole"], "ground_color": T["nc_color_ground"], "title": T["col_bean"]},
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )
        axis_min = min(ag["whole_color"].min(), ag["ground_color"].min()) - 3
        axis_max = max(ag["whole_color"].max(), ag["ground_color"].max()) + 3
        fig.add_shape(type="line", x0=axis_min, y0=axis_min, x1=axis_max, y1=axis_max,
                      line=dict(color="gray", dash="dot", width=1))
        fig = add_highlight(fig, "whole_color", "ground_color")
        fig.update_layout(height=480, margin=dict(l=0, r=0, t=10, b=0),
                          xaxis=dict(range=[axis_min, axis_max]),
                          yaxis=dict(range=[axis_min, axis_max]))
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.markdown(f"**{T['color_gap_dist']}**")
        fig2 = px.histogram(
            ag, x="gap", nbins=20,
            color_discrete_sequence=["#BA7517"],
            labels={"gap": "Gap (Ground − Whole)"},
        )
        fig2.add_vline(x=0, line_dash="dot", line_color="gray", annotation_text="±0", annotation_position="top right")
        fig2.add_vline(x=gap_mean, line_dash="dash", line_color="#888",
                       annotation_text=f"{'Avg' if st.session_state.lang == 'en' else '平均'} {gap_mean:.1f}", annotation_position="top left")
        if highlight_row is not None and not pd.isna(highlight_row.get("whole_color", float("nan"))) and not pd.isna(highlight_row.get("ground_color", float("nan"))):
            hl_gap = highlight_row["ground_color"] - highlight_row["whole_color"]
            fig2.add_vline(x=float(hl_gap), line_color="#D85A30", line_width=2,
                           annotation_text=f"▲ {_HL} ({hl_gap:.1f})",
                           annotation_position="top right",
                           annotation_font=dict(color="#D85A30", size=11))
        fig2.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        st.markdown(f"**{T['color_gap_box']}**")
        bean_order = ag.groupby("title")["gap"].median().sort_values().index.tolist()
        fig3 = px.box(
            ag, x="gap", y="title",
            orientation="h",
            category_orders={"title": bean_order},
            points="all",
            color="title",
            labels={"gap": "Gap (Ground − Whole)", "title": T["col_bean"]},
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )
        fig3.add_vline(x=0, line_dash="dot", line_color="gray")
        if highlight_row is not None and not pd.isna(highlight_row.get("whole_color", float("nan"))) and not pd.isna(highlight_row.get("ground_color", float("nan"))):
            hl_gap = highlight_row["ground_color"] - highlight_row["whole_color"]
            fig3.add_vline(x=float(hl_gap), line_color="#D85A30", line_width=2,
                           annotation_text=f"▲ {_HL} ({hl_gap:.1f})",
                           annotation_position="top right",
                           annotation_font=dict(color="#D85A30", size=11))
        fig3.update_layout(
            height=max(300, len(bean_order) * 38),
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        st.markdown(f"**{T['color_gap_trend']}**")
        gap_bean = st.selectbox(
            T["color_select_bean"],
            [T["color_select_all"]] + sorted(ag["title"].unique()),
            key="gap_trend_bean",
        )
        trend_df = ag if gap_bean == T["color_select_all"] else ag[ag["title"] == gap_bean]
        trend_df = trend_df.sort_values("date")
        fig4 = px.scatter(
            trend_df, x="date", y="gap",
            color="title",
            hover_data=["whole_color", "ground_color", "weight_loss_pct"],
            trendline="ols" if len(trend_df) > 2 else None,
            trendline_scope="overall",
            labels={"date": T["label_date"], "gap": "Gap (Ground − Whole)", "title": T["col_bean"]},
            color_discrete_sequence=px.colors.qualitative.Plotly,
        )
        fig4.add_hline(y=0, line_dash="dot", line_color="gray")
        fig4 = add_highlight(fig4, "date", "gap")
        fig4.update_layout(height=360, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig4, use_container_width=True)

        st.divider()

        st.markdown(f"**{T['color_gap_corr']}**")
        corr_targets = {
            T["nc_weight_loss"]: "weight_loss_pct",
            T["nc_roast_time"]: "total_time_sec",
            T["nc_dtr"]: "dev_time_ratio",
            T["nc_drop_temp"]: "drop_bt",
            T["nc_fc_temp"]: "fc_bt",
            T["nc_color_whole"]: "whole_color",
        }
        corr_col = st.selectbox(T["color_compare"], list(corr_targets.keys()), key="gap_corr")
        c_col = corr_targets[corr_col]
        corr_df = ag.dropna(subset=["gap", c_col])
        if len(corr_df) > 2:
            fig5 = px.scatter(
                corr_df, x=c_col, y="gap",
                color="title",
                trendline="ols",
                trendline_scope="overall",
                labels={c_col: corr_col, "gap": "Gap (Ground − Whole)", "title": T["col_bean"]},
                color_discrete_sequence=px.colors.qualitative.Plotly,
            )
            fig5.add_hline(y=0, line_dash="dot", line_color="gray")
            fig5 = add_highlight(fig5, c_col, "gap")
            fig5.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig5, use_container_width=True)
            r = corr_df[["gap", c_col]].corr().iloc[0, 1]
            st.metric(T["corr_coeff_label"].format(a="Gap", b=corr_col), f"{r:.3f}", help=T["corr_help"])
        else:
            st.info(T["data_insufficient"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: バッチ一覧
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader(T["batch_header"].format(n=len(filtered)))
    display_cols = {
        "date_str": T["dc_date"],
        "title": T["dc_bean"],
        "weight_in": T["dc_weight_in"],
        "weight_out": T["dc_weight_out"],
        "weight_loss_pct": T["dc_weight_loss"],
        "fc_bt": T["dc_fc_temp"],
        "drop_bt": T["dc_drop_temp"],
        "total_time_sec": T["dc_roast_time"],
        "dev_time_ratio": T["dc_dtr"],
        "whole_color": T["dc_color_whole"],
        "ground_color": T["dc_color_ground"],
        "ambient_temp": T["dc_ambient_temp"],
        "ambient_humidity": T["dc_humidity"],
        "preheat_temp": T["dc_preheat"],
        "roast_number": T["dc_roast_number"],
    }
    show_df = filtered[[c for c in display_cols if c in filtered.columns]].copy()
    show_df = show_df.rename(columns=display_cols)
    show_df = show_df.sort_values(T["dc_date"], ascending=False)
    st.dataframe(show_df, use_container_width=True, height=520)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6: エクスポート
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader(T["export_header"])
    st.write(T["export_desc"])

    _drop_cols = ["bean_temp", "drum_temp", "exit_temp", "bean_ror", "ibts_ror",
                  "actions", "file", "start_idx", "end_idx", "fc_idx", "sc_idx",
                  "yp_idx", "sample_rate", "uid"]
    export_df = filtered.drop(columns=[c for c in _drop_cols if c in filtered.columns], errors="ignore")

    csv = export_df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        T["export_csv"],
        data=csv,
        file_name="roastime_roast_data.csv",
        mime="text/csv",
    )

    try:
        import io
        buf = io.BytesIO()
        export_df.to_excel(buf, index=False, engine="openpyxl")
        st.download_button(
            T["export_excel"],
            data=buf.getvalue(),
            file_name="roastime_roast_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except ImportError:
        st.info(T["export_excel_hint"])

    st.divider()
    st.subheader(T["export_summary_header"])
    summary = (
        filtered.groupby("title")
        .agg(
            **{
                T["sum_batches"]: ("title", "count"),
                T["sum_avg_loss"]: ("weight_loss_pct", "mean"),
                T["sum_sd_loss"]: ("weight_loss_pct", "std"),
                T["sum_avg_time"]: ("total_time_sec", "mean"),
                T["sum_avg_dtr"]: ("dev_time_ratio", "mean"),
                T["sum_avg_drop"]: ("drop_bt", "mean"),
                T["sum_avg_fc"]: ("fc_bt", "mean"),
            }
        )
        .round(2)
        .reset_index()
        .rename(columns={"title": T["col_bean"]})
    )
    st.dataframe(summary, use_container_width=True)
    csv2 = summary.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(T["export_summary_csv"], data=csv2, file_name="roastime_summary.csv", mime="text/csv")
