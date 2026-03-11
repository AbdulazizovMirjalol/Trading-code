import pandas as pd
from config import (
    STATUS_NO_TRADE,
    STATUS_WATCH,
    STATUS_PULLBACK_BUY,
    STATUS_SELL_WATCH,
    STATUS_BREAKOUT_WATCH,
    STATUS_BREAKDOWN_WATCH,
    SIGNAL_WEAK,
    SIGNAL_MEDIUM,
    SIGNAL_STRONG,
    FINAL_SIGNAL_BUY,
    FINAL_SIGNAL_SELL,
    FINAL_SIGNAL_WAIT,
)

def add_ema(df: pd.DataFrame, periods):
    """
    DataFramega ko'rsatilgan davrlar uchun EMA ustunlari qo'shadi.
    """
    for p in periods:
        df[f"EMA_{p}"] = df["close"].ewm(span=p, adjust=False).mean()
    return df

def detect_trend(df: pd.DataFrame, short: int, long: int) -> str:
    """
    EMA kesishlariga qarab trend holatini aniqlaydi.
    Qisqa EMA uzun EMAdan yuqori bo'lsa — Bullish, aks holda Bearish.
    """
    if df.empty:
        return "Unknown"

    if df[f"EMA_{short}"].iloc[-1] > df[f"EMA_{long}"].iloc[-1]:
        return "Bullish (Ko'tarilish)"
    elif df[f"EMA_{short}"].iloc[-1] < df[f"EMA_{long}"].iloc[-1]:
        return "Bearish (Tushish)"
    else:
        return "Sideways (Range)"
    
def add_rsi(df: pd.DataFrame, period: int = 14):
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

def interpret_rsi(rsi_value: float) -> str:
    if rsi_value >= 70:
        return "Overbought (bozor juda qizigan)"
    elif rsi_value <= 30:
        return "Oversold (bozor juda tushgan)"
    elif rsi_value > 50:
        return "Bullish momentum"
    elif rsi_value < 50:
        return "Bearish momentum"
    else:
        return "Neutral"
    
def generate_summary(
    h1_trend: str,
    m15_trend: str,
    rsi_value: float,
    macd_text: str,
    current_price: float,
    support: float,
    resistance: float
) -> str:
    distance_to_support = abs(current_price - support)
    distance_to_resistance = abs(resistance - current_price)

    bullish_rsi = rsi_value > 50
    bearish_rsi = rsi_value < 50
    bullish_macd = "Bullish" in macd_text
    bearish_macd = "Bearish" in macd_text

    bullish_alignment = "Bullish" in h1_trend and "Bullish" in m15_trend
    bearish_alignment = "Bearish" in h1_trend and "Bearish" in m15_trend
    mixed_bullish = "Bullish" in h1_trend and "Bearish" in m15_trend
    mixed_bearish = "Bearish" in h1_trend and "Bullish" in m15_trend

    if bullish_alignment and bullish_rsi and bullish_macd:
        if distance_to_resistance < distance_to_support:
            return "H1 va M15 bullish alignmentda. RSI va MACD ham bullish. Narx resistance ga yaqin, breakout kuzatish kerak."
        return "H1 va M15 bullish alignmentda. RSI va MACD ham bullish. Bozor yuqoriga bosim ko'rsatmoqda."

    elif bearish_alignment and bearish_rsi and bearish_macd:
        if distance_to_support < distance_to_resistance:
            return "H1 va M15 bearish alignmentda. RSI va MACD ham bearish. Narx support ga yaqin, breakdown xavfi bor."
        return "H1 va M15 bearish alignmentda. RSI va MACD ham bearish. Bozor pastga bosim ko'rsatmoqda."

    elif bullish_alignment and bullish_rsi and bearish_macd:
        return "H1 va M15 bullish alignmentda, RSI bullish, lekin MACD zaiflashishni ko'rsatmoqda."

    elif bearish_alignment and bearish_rsi and bullish_macd:
        return "H1 va M15 bearish alignmentda, RSI bearish, lekin MACD tiklanishga urinmoqda."

    elif mixed_bullish:
        return "H1 bullish, lekin M15 zaiflashgan. Bu pullback yoki vaqtinchalik tuzatish bo'lishi mumkin."

    elif mixed_bearish:
        return "H1 bearish, lekin M15 tiklanmoqda. Bu counter-trend rebound bo'lishi mumkin."

    elif "Bullish" in m15_trend and bearish_rsi:
        return "M15 trend bullish, lekin momentum zaiflashgan."

    elif "Bearish" in m15_trend and bullish_rsi:
        return "M15 trend bearish, lekin momentum tiklanishga urinmoqda."

    else:
        return "Bozor noaniq yoki range holatda."
    
def generate_trade_comment(
    h1_trend: str,
    m15_trend: str,
    rsi_text: str,
    macd_text: str,
    price_location: str,
    entry_zone_text: str,
    setup_status: str
) -> str:
    if setup_status == STATUS_PULLBACK_BUY:
        return "Asosiy trend bullish. Pullback buy setup mavjud. Entry tasdiqlari kuzatilishi mumkin."

    elif setup_status == STATUS_BREAKOUT_WATCH:
        return "Narx resistance yaqinida. Breakout bo‘lishi mumkin, tasdiqni kutish kerak."

    elif setup_status == STATUS_SELL_WATCH:
        return "Asosiy trend bearish. Sell setup shakllanishi mumkin, entry tasdiqlari kuzatilishi kerak."

    elif setup_status == STATUS_BREAKDOWN_WATCH:
        return "Narx support yaqinida. Breakdown ehtimoli bor, pastga yorib o‘tishni kuzatish kerak."

    elif setup_status == STATUS_WATCH:
        return "Trend mavjud, lekin signal hali to‘liq tasdiqlanmagan. Kuzatish tavsiya qilinadi."

    else:
        return "Hozircha aniq trade setup yo‘q. Shoshilmasdan kutish kerak."
    
def detect_setup_status(
    h1_trend: str,
    m15_trend: str,
    rsi_text: str,
    macd_text: str,
    price_location: str,
    entry_zone_text: str,
    candle_confirmation: str,
) -> str:
        if "Bullish" in h1_trend and "Bullish" in m15_trend:
            if (
                "Bullish" in rsi_text
                and "Bullish" in macd_text
                and "Bullish candle confirmation" in candle_confirmation
            ):
                return STATUS_PULLBACK_BUY

            elif (
                "support" in entry_zone_text.lower()
                and (
                    "Weak bullish candle" in candle_confirmation
                    or "Bullish candle confirmation" in candle_confirmation
                )
            ):
                return STATUS_WATCH

            else:
                return STATUS_NO_TRADE

        elif "Bearish" in h1_trend and "Bearish" in m15_trend:
            if (
                "Bearish" in rsi_text
                and "Bearish" in macd_text
                and "Bearish candle confirmation" in candle_confirmation
            ):
                return STATUS_SELL_WATCH

            elif (
                "resistance" in entry_zone_text.lower()
                and (
                    "Weak bearish candle" in candle_confirmation
                    or "Bearish candle confirmation" in candle_confirmation
                )
            ):
                return STATUS_WATCH

            else:
                return STATUS_NO_TRADE

        else:
            return STATUS_NO_TRADE
            
def detect_signal_strength(
    h1_trend: str,
    m15_trend: str,
    rsi_text: str,
    macd_text: str,
    setup_status: str,
    candle_confirmation: str,
) -> str:
    if setup_status == STATUS_NO_TRADE:
        return "WEAK"

    bullish_count = 0
    bearish_count = 0

    if "Bullish" in h1_trend:
        bullish_count += 1
    if "Bullish" in m15_trend:
        bullish_count += 1
    if "Bullish" in rsi_text:
        bullish_count += 1
    if "Bullish" in macd_text:
        bullish_count += 1
    if "Bullish candle confirmation" in candle_confirmation:
        bullish_count += 1
    elif "Weak bullish candle" in candle_confirmation:
        bullish_count += 0.5

    if "Bearish" in h1_trend:
        bearish_count += 1
    if "Bearish" in m15_trend:
        bearish_count += 1
    if "Bearish" in rsi_text:
        bearish_count += 1
    if "Bearish" in macd_text:
        bearish_count += 1
    if "Bearish candle confirmation" in candle_confirmation:
        bearish_count += 1
    elif "Weak bearish candle" in candle_confirmation:
        bearish_count += 0.5

    max_score = max(bullish_count, bearish_count)

    if max_score >= 4:
        return "STRONG"
    elif max_score >= 2.5:
        return "MEDIUM"
    else:
        return "WEAK"

def generate_trade_plan(
    setup_status: str,
    signal_strength: str,
    price_location: str
) -> str:
    if setup_status == STATUS_PULLBACK_BUY:
        return "Buy setup mavjud. Entry trigger va candle tasdig‘ini kuting."

    elif setup_status == STATUS_BREAKOUT_WATCH:
        return "Narx resistance yaqinida. Breakout bo‘lsa entry imkoniyati paydo bo‘lishi mumkin."

    elif setup_status == STATUS_SELL_WATCH:
        return "Sell setup kuzatilmoqda. Bearish tasdiq bo‘lsa entry qidirish mumkin."

    elif setup_status == STATUS_BREAKDOWN_WATCH:
        return "Narx support yaqinida. Breakdown bo‘lsa sell imkoniyati paydo bo‘lishi mumkin."

    elif setup_status == STATUS_WATCH:
        return "Signal hali to‘liq emas. Kuzatish va qo‘shimcha tasdiq kutish kerak."

    return "Hozircha trade ochish tavsiya etilmaydi."
    
def add_macd(df: pd.DataFrame):
    ema_12 = df["close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema_12 - ema_26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

def add_atr(df: pd.DataFrame, period: int = 14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = true_range.rolling(window=period).mean()

    return df


def interpret_macd(df: pd.DataFrame) -> str:
    macd_value = df["MACD"].iloc[-1]
    signal_value = df["MACD_signal"].iloc[-1]

    if macd_value > signal_value:
        return "Bullish MACD momentum"
    elif macd_value < signal_value:
        return "Bearish MACD momentum"
    else:
        return "Neutral MACD"
    
def find_support_resistance(df: pd.DataFrame):
    recent_support = df["low"].tail(20).min()
    recent_resistance = df["high"].tail(20).max()

    return recent_support, recent_resistance

def analyze_timeframe_alignment(h1_trend: str, m15_trend: str) -> str:
    if "Bullish" in h1_trend and "Bullish" in m15_trend:
        return "H1 va M15 bir tomonda. Bullish alignment kuchli."
    elif "Bearish" in h1_trend and "Bearish" in m15_trend:
        return "H1 va M15 bir tomonda. Bearish alignment kuchli."
    elif "Bullish" in h1_trend and "Bearish" in m15_trend:
        return "H1 bullish, M15 bearish. Bu pullback yoki vaqtinchalik tuzatish bo'lishi mumkin."
    elif "Bearish" in h1_trend and "Bullish" in m15_trend:
        return "H1 bearish, M15 bullish. Bu counter-trend rebound bo'lishi mumkin."
    else:
        return "Timeframe alignment noaniq."
    
def detect_price_location(current_price: float, support: float, resistance: float) -> str:
    distance_to_support = abs(current_price - support)
    distance_to_resistance = abs(resistance - current_price)
    total_range = resistance - support

    if total_range == 0:
        return "Narx diapazoni aniqlanmadi."

    support_ratio = distance_to_support / total_range
    resistance_ratio = distance_to_resistance / total_range

    if support_ratio < 0.25:
        return "Narx support ga yaqin."
    elif resistance_ratio < 0.25:
        return "Narx resistance ga yaqin."
    else:
        return "Narx support va resistance oralig'ida."
    
def detect_entry_zone(
    trend: str,
    current_price: float,
    ema20: float,
    support: float,
    resistance: float,
    atr: float
) -> str:
    distance_to_ema20 = abs(current_price - ema20)
    distance_to_support = abs(current_price - support)
    distance_to_resistance = abs(resistance - current_price)

    threshold = atr if atr > 0 else 5

    if "Bullish" in trend:
        if distance_to_ema20 < threshold or distance_to_support < threshold:
            return "Bullish setup: narx EMA20/support zonasiga yaqin."
        else:
            return "Bullish trend bor, lekin narx entry zonasidan uzoq."

    elif "Bearish" in trend:
        if distance_to_ema20 < threshold or distance_to_resistance < threshold:
            return "Bearish setup: narx EMA20/resistance zonasiga yaqin."
        else:
            return "Bearish trend bor, lekin narx entry zonasidan uzoq."

    return "Aniq entry zona topilmadi."

def generate_risk_levels(
    h1_trend: str,
    m15_trend: str,
    support: float,
    resistance: float,
    atr_value: float,
    setup_status: str
):
    if setup_status in [STATUS_PULLBACK_BUY, STATUS_BREAKOUT_WATCH]:
        stop_loss = support - (atr_value * 0.5)
        take_profit = resistance
        return round(stop_loss, 2), round(take_profit, 2)

    elif setup_status in [STATUS_SELL_WATCH, STATUS_BREAKDOWN_WATCH]:
        stop_loss = resistance + (atr_value * 0.5)
        take_profit = support
        return round(stop_loss, 2), round(take_profit, 2)

    elif setup_status == STATUS_WATCH:
        if "Bullish" in h1_trend:
            stop_loss = support - (atr_value * 0.5)
            take_profit = resistance
            return round(stop_loss, 2), round(take_profit, 2)

        elif "Bearish" in h1_trend:
            stop_loss = resistance + (atr_value * 0.5)
            take_profit = support
            return round(stop_loss, 2), round(take_profit, 2)

    return None, None

def calculate_risk_reward(
    current_price: float,
    suggested_sl,
    suggested_tp
):
    if suggested_sl is None or suggested_tp is None:
        return None

    risk = abs(current_price - suggested_sl)
    reward = abs(suggested_tp - current_price)

    if risk == 0:
        return None

    rr = reward / risk
    return round(rr, 2)

def generate_final_signal(
    setup_status: str,
    signal_strength: str
) -> str:
    if setup_status == STATUS_PULLBACK_BUY and signal_strength in [SIGNAL_STRONG, SIGNAL_MEDIUM]:
        return FINAL_SIGNAL_BUY

    elif setup_status in [STATUS_SELL_WATCH, STATUS_BREAKDOWN_WATCH] and signal_strength in [SIGNAL_STRONG, SIGNAL_MEDIUM]:
        return FINAL_SIGNAL_SELL

    return FINAL_SIGNAL_WAIT

def generate_entry_price(
    setup_status: str,
    current_price: float,
    ema20_value: float,
    support: float,
    resistance: float
):
    if setup_status == "PULLBACK_BUY":
        return round(min(current_price, ema20_value, support + 1.0), 2)

    elif setup_status == "SELL_WATCH":
        return round(max(current_price, ema20_value, resistance - 1.0), 2)

    elif setup_status == "BREAKOUT_WATCH":
        return round(resistance + 1.0, 2)

    elif setup_status == "BREAKDOWN_WATCH":
        return round(support - 1.0, 2)

    return None

def generate_alert_message(
    final_signal: str,
    setup_status: str,
    signal_strength: str
) -> str:
    if final_signal == "BUY":
        return "ALERT: Buy signal tayyor."
    elif final_signal == "SELL":
        return "ALERT: Sell signal tayyor."
    elif setup_status == "WATCH" and signal_strength in ["MEDIUM", "STRONG"]:
        return "ALERT: Kuzatishga arziydigan setup mavjud."
    elif setup_status == "NO TRADE":
        return "ALERT: Hozircha signal kuchsiz."
    else:
        return "ALERT: Bozorni kuzatishda davom eting."
    
def generate_reason(
    h1_trend: str,
    m15_trend: str,
    rsi_text: str,
    macd_text: str,
    price_location: str,
    setup_status: str,
    final_signal: str
) -> str:
    if final_signal == "BUY":
        return "BUY signali bor: trend mos, momentum yetarli va setup tasdiqlangan."

    elif final_signal == "SELL":
        return "SELL signali bor: trend mos, momentum yetarli va setup tasdiqlangan."

    elif setup_status == "WATCH":
        return "Setup kuzatishda: trend mavjud, lekin signal hali to‘liq tasdiqlanmagan."

    elif setup_status == "NO TRADE":
        return "Trade ochish uchun yetarli tasdiq yo‘q. Trend va momentum bir tomonda emas."

    elif "Bullish" in h1_trend and "Bearish" in m15_trend:
        return "Higher timeframe bullish, lekin entry timeframe pullback yoki vaqtinchalik tushishda."

    elif "Bearish" in h1_trend and "Bullish" in m15_trend:
        return "Higher timeframe bearish, lekin entry timeframe pullback yoki vaqtinchalik ko‘tarilishda."

    return "Bozor holati aralash, qo‘shimcha tasdiq kerak."

def calculate_risk_reward(
    setup_status: str,
    entry_price: float,
    stop_loss: float,
    take_profit: float
):
    if entry_price is None or stop_loss is None or take_profit is None:
        return None

    if setup_status in ["PULLBACK_BUY", "BREAKOUT_WATCH"]:
        risk = entry_price - stop_loss
        reward = take_profit - entry_price

    elif setup_status in ["SELL_WATCH", "BREAKDOWN_WATCH"]:
        risk = stop_loss - entry_price
        reward = entry_price - take_profit

    else:
        return None

    if risk <= 0:
        return None

    return round(reward / risk, 2)


def detect_candle_confirmation(df) -> str:
    if len(df) < 2:
        return "No candle confirmation"

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Kuchli bullish tasdiq
    if last["close"] > last["open"] and last["close"] > prev["high"]:
        return "Bullish candle confirmation"

    # Kuchli bearish tasdiq
    if last["close"] < last["open"] and last["close"] < prev["low"]:
        return "Bearish candle confirmation"

    # Oddiy bullish candle
    if last["close"] > last["open"]:
        return "Weak bullish candle"

    # Oddiy bearish candle
    if last["close"] < last["open"]:
        return "Weak bearish candle"

    return "No clear candle confirmation"