# ── risk_4_1 stop-section vector layout ────────────────────────────
# Shared by valid_json_confluence/functions.py (extraction from the strategy
# JSON "stop" section), ConfluenceEngine.get_dynamic_stop_levels (consumption),
# and the fixed-length NaN defaults sprinkled across run_backtest /
# runtime_constants / inspect_data. Slots 0-15 predate this spec; 16+ are the
# dynamic stop references added for sharedcfg §4.1.
R41_ADR_PERIOD = 0
R41_STRUCT_LOW_CANDLES = 16  # structurelowstop: N-bar low (long-side ref)
R41_STRUCT_HIGH_CANDLES = 17  # structurehighstop: N-bar high (short-side ref)
R41_PIVOT_LOW_STRENGTH = 18  # structurepivotlowstop: fractal strength
R41_PIVOT_HIGH_STRENGTH = 19  # structurepivothighstop: fractal strength
R41_LEVELSTOP_TICKS = 20  # signed tick buffer applied to enabled levels
R41_LEVEL_FLAGS_START = 21
R41_ZONE_OB = 12  # zonestopob / fvg / ifvg / sweep live in 12-15
R41_ZONE_FVG = 13
R41_ZONE_IFVG = 14
R41_ZONE_SWEEP = 15

# (json key under "stop", indicator id the level resolves to)
LEVEL_STOP_FIELDS: list[tuple[str, str]] = [
    ("levelstop_pdl", "low1d"),
    ("levelstop_pdh", "high1d"),
    ("levelstop_vwap", "vwap"),
    ("levelstop_priordayvwap", "priordayvwap"),
    ("levelstop_priorweekvwap", "priorweekvwap"),
    ("levelstop_poc", "poc"),
    ("levelstop_vah", "vah"),
    ("levelstop_val", "val"),
    ("levelstop_ivblow", "ivblow"),
    ("levelstop_ivbhigh", "ivbhigh"),
    ("levelstop_low1h", "low1h"),
    ("levelstop_high1h", "high1h"),
    ("levelstop_low4h", "low4h"),
    ("levelstop_high4h", "high4h"),
]

# Pattern-invalidation stop: appended AFTER the level flags, so these slots
# must be DERIVED from the level count — hardcoding them would silently
# misalign the moment LEVEL_STOP_FIELDS grows.
R41_PATTERN_FLAGLOW = R41_LEVEL_FLAGS_START + len(LEVEL_STOP_FIELDS)
R41_PATTERN_RANGELOW = R41_PATTERN_FLAGLOW + 1
R41_PATTERN_NECKLINE = R41_PATTERN_FLAGLOW + 2
RISK_4_1_PARAMS_LEN = R41_PATTERN_NECKLINE + 1

# ── dynamic-stop engine defaults ───────────────────────────────────
# Zone stops carry no params on the wire (plain bools), so the underlying
# detectors run at these canonical arguments; retune here, one place.
ZONE_STOP_FVG_ATR_MULT = 0.5
ZONE_STOP_IFVG_ATR_MULT = 0.5
ZONE_STOP_SWEEP_ATR_MULT = 0.5
ZONE_STOP_OB_DISPLACEMENT = 2.0
ZONE_STOP_OB_MEAN_THRESHOLD = 0.5

# Pattern-invalidation stop: each enabled key aggregates across its whole
# pattern family at these canonical default args (id suffix strings).
PATTERN_STOP_LOOKBACK = 20
PATTERN_FLAG_FAMILY: tuple[tuple[str, str], ...] = (
    ("bullbearflag", "5_10_14_14_1.5"),
    ("hightightflag", "20_25_60_5_4.0"),
    ("pennant", "5_21_5_0.5_1.5"),
)
PATTERN_RANGE_FAMILY: tuple[tuple[str, str], ...] = (
    ("withinrangepercent", "20_5.0"),
    ("flatbase", "6_15_2"),
    ("darvasbox", "20_2.0"),
    ("horizontalchannel", "20_1.0_10.0"),
)
PATTERN_NECKLINE_FAMILY: tuple[tuple[str, str], ...] = (
    ("headandshoulders", "40_3.0_2.0_1.0"),
    ("doubletopbottom", "40_3.0_5_2.0"),
    ("tripletopbottom", "40_3.0_5"),
)
