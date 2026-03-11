from rich.console import Console
from rich.table import Table
from datetime import datetime
from pathlib import Path
import pandas as pd

console = Console()

def show_analysis_report(
    h1_timeframe_name: str,
    m15_timeframe_name: str,
    h1_trend: str,
    m15_trend: str,
    alignment_text: str,
    rsi_value: float,
    rsi_text: str,
    macd_text: str,
    candle_confirmation: str,
    support: float,
    resistance: float,
    atr_value: float,
    price_location: str,
    entry_zone_text: str,
    summary: str,
    trade_comment: str,
    setup_status: str,
    signal_strength: str,
    trade_plan: str,
    final_signal: str,
    alert_message: str,
    reason: str,
    suggested_entry,
    suggested_sl,
    suggested_tp,
    risk_reward_ratio,
):
    table = Table(title="GOLD TRADING ANALYSIS REPORT")

    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Higher Timeframe", h1_timeframe_name)
    table.add_row("Entry Timeframe", m15_timeframe_name)
    table.add_row("H1 Trend", h1_trend)
    table.add_row("M15 Trend", m15_trend)
    table.add_row("Timeframe Alignment", alignment_text)
    table.add_row("RSI", f"{rsi_value:.2f}")
    table.add_row("RSI Status", rsi_text)
    table.add_row("MACD Status", macd_text)
    table.add_row("Candle Confirmation", candle_confirmation)
    table.add_row("Support", f"{support:.2f}")
    table.add_row("Resistance", f"{resistance:.2f}")
    table.add_row("ATR", f"{atr_value:.2f}")
    table.add_row("Price Location", price_location)
    table.add_row("Entry Zone", entry_zone_text)
    table.add_row("Summary", summary)
    table.add_row("Trade Comment", trade_comment)
    table.add_row("Setup Status", setup_status)
    table.add_row("Signal Strength", signal_strength)
    table.add_row("Trade Plan", trade_plan)
    table.add_row("Final Signal", final_signal)
    table.add_row("Alert Message", alert_message)
    table.add_row("Reason", reason)

    if suggested_entry is not None:
        table.add_row("Suggested Entry", f"{suggested_entry:.2f}")
    else:
        table.add_row("Suggested Entry", "N/A")

    if suggested_sl is not None:
        table.add_row("Suggested Stop Loss", f"{suggested_sl:.2f}")
    else:
        table.add_row("Suggested Stop Loss", "N/A")

    if suggested_tp is not None:
        table.add_row("Suggested Take Profit", f"{suggested_tp:.2f}")
    else:
        table.add_row("Suggested Take Profit", "N/A")

    if risk_reward_ratio is not None:
        table.add_row("Risk/Reward Ratio", f"{risk_reward_ratio:.2f}")
    else:
        table.add_row("Risk/Reward Ratio", "N/A")

    console.print(table)

def show_price_table(df):
    table = Table(title="XAUUSD M15 - Last 5 Bars")

    columns = ["time", "open", "high", "low", "close", "EMA_20", "EMA_50", "RSI", "MACD", "MACD_signal"]

    for col in columns:
        table.add_column(col, style="cyan")

    last_rows = df.tail(5)

    for _, row in last_rows.iterrows():
        table.add_row(
            str(row["time"]),
            f"{row['open']:.2f}",
            f"{row['high']:.2f}",
            f"{row['low']:.2f}",
            f"{row['close']:.2f}",
            f"{row['EMA_20']:.2f}",
            f"{row['EMA_50']:.2f}",
            f"{row['RSI']:.2f}",
            f"{row['MACD']:.2f}",
            f"{row['MACD_signal']:.2f}",
        )

    console.print(table)

from datetime import datetime
from pathlib import Path


from datetime import datetime
from pathlib import Path


def save_analysis_to_file(result: dict):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = logs_dir / f"analysis_{timestamp}.txt"

    m15_df = result["m15_df"].tail(5)

    lines = []
    lines.append("GOLD TRADING ANALYSIS REPORT")
    lines.append("=" * 50)
    lines.append("")
    lines.append("XAUUSD M15 - Last 5 Bars")
    lines.append("-" * 50)
    lines.append(m15_df.to_string(index=False))
    lines.append("")
    lines.append("FINAL ANALYSIS")
    lines.append("-" * 50)
    lines.append(f"Higher Timeframe: {result['h1_timeframe_name']}")
    lines.append(f"Entry Timeframe: {result['m15_timeframe_name']}")
    lines.append(f"H1 Trend: {result['h1_trend']}")
    lines.append(f"M15 Trend: {result['m15_trend']}")
    lines.append(f"Timeframe Alignment: {result['alignment_text']}")
    lines.append(f"RSI: {result['last_rsi']:.2f}")
    lines.append(f"RSI Status: {result['rsi_text']}")
    lines.append(f"MACD Status: {result['macd_text']}")
    lines.append(f"Support: {result['support']:.2f}")
    lines.append(f"Resistance: {result['resistance']:.2f}")
    lines.append(f"ATR: {result['atr_value']:.2f}")
    lines.append(f"Price Location: {result['price_location']}")
    lines.append(f"Entry Zone: {result['entry_zone_text']}")
    lines.append(f"Summary: {result['summary']}")
    lines.append(f"Trade Comment: {result['trade_comment']}")
    lines.append(f"Setup Status: {result['setup_status']}")
    lines.append(f"Signal Strength: {result['signal_strength']}")
    lines.append(f"Trade Plan: {result['trade_plan']}")
    lines.append(f"Final Signal: {result['final_signal']}")
    lines.append(f"Alert Message: {result['alert_message']}")
    lines.append(
    f"Suggested Entry: {result['suggested_entry'] if result['suggested_entry'] is not None else 'N/A'}"
    )
    lines.append(
        f"Suggested Stop Loss: {result['suggested_sl'] if result['suggested_sl'] is not None else 'N/A'}"
    )
    lines.append(
        f"Suggested Take Profit: {result['suggested_tp'] if result['suggested_tp'] is not None else 'N/A'}"
    )
    lines.append(
        f"Risk/Reward Ratio: {result['risk_reward_ratio'] if result['risk_reward_ratio'] is not None else 'N/A'}"
    )
    lines.append(
        f"Risk/Reward Ratio: {result['risk_reward_ratio'] if result['risk_reward_ratio'] is not None else 'N/A'}"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    cleanup_old_logs(max_files=30)

    print(f"\nAnalysis faylga saqlandi: {file_path}")


def cleanup_old_logs(max_files: int = 30):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_files = sorted(logs_dir.glob("analysis_*.txt"), key=lambda f: f.stat().st_mtime)

    while len(log_files) > max_files:
        oldest_file = log_files.pop(0)
        oldest_file.unlink()

def save_bars_to_csv(result: dict):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = logs_dir / f"bars_{timestamp}.csv"

    result["m15_df"].tail(5).to_csv(file_path, index=False)

    cleanup_old_logs(max_files=30)
    print(f"Bars CSV faylga saqlandi: {file_path}")

def save_signal_journal(result: dict):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    file_path = logs_dir / "signal_journal.csv"

    row = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": result["symbol"],
        "higher_tf": result["h1_timeframe_name"],
        "entry_tf": result["m15_timeframe_name"],
        "h1_trend": result["h1_trend"],
        "m15_trend": result["m15_trend"],
        "alignment": result["alignment_text"],
        "rsi": round(result["last_rsi"], 2),
        "rsi_status": result["rsi_text"],
        "macd_status": result["macd_text"],
        "candle_confirmation": result["candle_confirmation"],
        "support": round(result["support"], 2),
        "resistance": round(result["resistance"], 2),
        "atr": round(result["atr_value"], 2),
        "price_location": result["price_location"],
        "entry_zone": result["entry_zone_text"],
        "setup_status": result["setup_status"],
        "signal_strength": result["signal_strength"],
        "final_signal": result["final_signal"],
        "trade_plan": result["trade_plan"],
        "alert_message": result["alert_message"],
        "reason": result["reason"],
        "suggested_entry": result["suggested_entry"],
        "suggested_sl": result["suggested_sl"],
        "suggested_tp": result["suggested_tp"],
        "risk_reward_ratio": result["risk_reward_ratio"],
    }

    df = pd.DataFrame([row])

    try:
        if file_path.exists():
            df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8")
        else:
            df.to_csv(file_path, index=False, encoding="utf-8")

        print(f"Signal jurnal saqlandi: {file_path}")

    except PermissionError:
        print(f"Xatolik: {file_path} fayli ochiq turibdi. Avval faylni yoping.")

def show_signal_stats():
    file_path = Path("logs") / "signal_journal.csv"

    if not file_path.exists():
        print("Signal jurnal topilmadi.")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Signal statistikani o‘qishda xatolik: {e}")
        print("Ehtimol signal_journal.csv eski va yangi format aralashib ketgan.")
        print("logs/signal_journal.csv faylini o‘chirib, qayta yaratib ko‘ring.")
        return

    if df.empty:
        print("Signal jurnal bo‘sh.")
        return

    print("\nSIGNAL STATISTICS")
    print("-----------------")
    print(f"Jami signal yozuvlari: {len(df)}")

    if "final_signal" in df.columns:
        print("\nFinal Signal statistikasi:")
        print(df["final_signal"].value_counts().to_string())

    if "setup_status" in df.columns:
        print("\nSetup Status statistikasi:")
        print(df["setup_status"].value_counts().to_string())

    if "signal_strength" in df.columns:
        print("\nSignal Strength statistikasi:")
        print(df["signal_strength"].value_counts().to_string())

def show_final_decision(
    h1_timeframe_name: str,
    m15_timeframe_name: str,
    final_signal: str,
    setup_status: str,
    signal_strength: str,
    trade_plan: str,
    alert_message: str,
):
    print("\nFINAL DECISION")
    print("-" * 14)
    print(f"Higher TF: {h1_timeframe_name}")
    print(f"Entry TF: {m15_timeframe_name}")
    print(f"Signal: {final_signal}")
    print(f"Setup: {setup_status}")
    print(f"Strength: {signal_strength}")
    print(f"Plan: {trade_plan}")
    print(f"Alert: {alert_message}")

def show_run_context(symbol: str, h1_timeframe_name: str, m15_timeframe_name: str):
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"SYMBOL: {symbol}")
    print(f"HIGHER TF: {h1_timeframe_name}")
    print(f"ENTRY TF: {m15_timeframe_name}")
    print(f"TIME: {now_text}\n")