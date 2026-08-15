import json

import numpy as np

from .classes import CandleSize
from .functions import get_indicator_conditions_from_jsons


def validate_json_file(json_data):
    # ensure if equity >= 15min  timeframe
    if (
        type(json_data["instrument"]) is str
        and json_data["instrument"] == "equity"
        and CandleSize(json_data["timeframe"]) < CandleSize.MINUTE_15
    ):
        return 201
    if (
        json_data.get("check_universe_frequency", None)
        and CandleSize(json_data["check_universe_frequency"])
    ) < CandleSize.WEEK_1:
        return 211

    (
        setup_indicators,
        condition_for_setup_indicators,
        entry_indicators,
        condition_for_entry_indicators,
        universe_indicators,
        condition_for_universe_indicators,
        extra_indicators,
        _,
    ) = get_indicator_conditions_from_jsons(json_data)

    if setup_indicators is None or condition_for_setup_indicators is None:
        return 203  # Invalid setup indicators
    if entry_indicators is None or condition_for_entry_indicators is None:
        return 204  # Invalid entry indicators
    if universe_indicators is None or condition_for_universe_indicators is None:
        return 205  # Invalid universe indicators
    try:
        CandleSize(json_data["timeframe"])
    except ValueError:
        return 202

    risk_params_4_3 = json_data.get("target", {})
    risk_params_4_4 = risk_params_4_3.get("then", {})
    rr_trigger_move_stop_breakeven = risk_params_4_4.get(
        "move_stop_breakeven", np.nan
    )  # rr_trigger
    lock_profit_ratchet = risk_params_4_4.get(
        "lock_profit_ratchet", [np.nan, np.nan]
    )  # [rr_target, rr_stop]
    rr_target_lock_profit_ratchet = lock_profit_ratchet[0]
    rr_stop_lock_profit_ratchet = lock_profit_ratchet[1]
    ma_trail = risk_params_4_4.get(
        "ma_trail", [np.nan, np.nan, np.nan]
    )  # [ma_period, ma_type, ma_multiplier]
    ma_params = ma_trail[0:2]
    if not np.isnan(ma_trail[0]):
        extra_indicators.append(f"ma_{int(ma_params[0])}_{int(ma_params[1])}")
    atr_trail = risk_params_4_4.get("atr_trail", [np.nan, np.nan])
    atr_params = atr_trail[0:1]
    if not np.isnan(atr_trail[0]):
        extra_indicators.append(f"atr_{int(atr_params[0])}")
    sar_trail = risk_params_4_4.get("parabolicsar_trail", [np.nan, np.nan, np.nan])
    sar_params = sar_trail[0:2]
    if not np.isnan(sar_trail[0]):
        extra_indicators.append(
            f"parabolicsar_{int(sar_params[0])}_{int(sar_params[1])}"
        )
    supertrend_trail = risk_params_4_4.get("supertrend_trail", [np.nan, np.nan, np.nan])
    supertrend_params = supertrend_trail[0:2]
    if not np.isnan(supertrend_trail[0]):
        extra_indicators.append(
            f"supertrendline_{int(supertrend_params[0])}_{int(supertrend_params[1])}"
        )
    dollar_trail = risk_params_4_4.get("dollar_trail", np.nan)
    percent_trail = risk_params_4_4.get("percent_trail", np.nan)
    bar_trail = 1.0 if risk_params_4_4.get("barbybar_trail", False) else 0.0
    never_widen_invariant = (
        1.0 if risk_params_4_4.get("never_widen_invariant", True) else 0.0
    )
    if never_widen_invariant == 0.0:
        return 205  # Invalid never_widen_invariant value
    structure_trail = risk_params_4_4.get("structure_trail", np.nan)
    if not np.isnan(structure_trail):
        extra_indicators.append(f"structuresllong_{int(structure_trail)}")
        extra_indicators.append(f"structureslshort_{int(structure_trail)}")

    ma_multiple = ma_trail[2]
    atr_multiple = atr_trail[1]
    sar_multiple = sar_trail[2]
    supertrend_multiple = supertrend_trail[2]
    if (
        ma_multiple < 0.0
        or atr_multiple < 0.0
        or sar_multiple < 0.0
        or supertrend_multiple < 0.0
    ):
        return 206  # Invalid multiple value
    if rr_trigger_move_stop_breakeven < 0.0:
        return 207  # Invalid rr_trigger_move_stop_breakeven value
    if rr_stop_lock_profit_ratchet < 0.0 or rr_target_lock_profit_ratchet < 0.0:
        return 208  # Invalid rr_lock_profit_ratchet value
    if rr_stop_lock_profit_ratchet >= rr_target_lock_profit_ratchet:
        return 209  # Invalid rr_lock_profit_ratchet value
    if (
        dollar_trail < 0.0
        or percent_trail < 0.0
        or bar_trail < 0.0
        or structure_trail < 2.0
    ):
        return 210  # Invalid trail value
    risk_params_4_3 = json_data.get("target", {})

    r_multiple_targets = risk_params_4_3.get(
        "rr_multiple_targets", [[np.nan, np.nan] for _ in range(5)]
    )  # [risk_multiple, % of position to exit], [risk_multiple, % of position to exit], ...)
    arr = np.array(r_multiple_targets)
    if not np.isnan(arr).all():
        total_risk_multiple = sum(
            t[1] for t in r_multiple_targets if not np.isnan(t[1])
        )
        if round(total_risk_multiple) < 100:
            if round(total_risk_multiple) == 0:
                r_multiple_targets[0] = [float("9" * 10), 100 - total_risk_multiple]
            else:
                r_multiple_targets.append([float("9" * 10), 100 - total_risk_multiple])
        if len(r_multiple_targets) > 5:
            return 220
        if len(r_multiple_targets) < 5:
            r_multiple_targets.extend(
                [np.nan, np.nan] for _ in range(5 - len(r_multiple_targets))
            )
    time_based_takes = risk_params_4_3.get(
        "time_based_takes", [[np.nan, np.nan] for _ in range(5)]
    )
    if len(time_based_takes) > 5:
        return 220
    if len(time_based_takes) < 5:
        time_based_takes.extend(
            [np.nan, np.nan] for _ in range(5 - len(time_based_takes))
        )

    return 200


if __name__ == "__main__":
    with open("ref-1-bullflag-tech.json", "r") as f:
        json_data = json.load(f)
    response = validate_json_file(json_data)

    if response == 200:
        print("Valid JSON file")
    else:
        print("Invalid JSON file")
