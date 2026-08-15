from __future__ import annotations

import numpy as np


def obtain_conditions_for_setup_indicators(
    json_data_conditions,
    extra_indicators: list[str] | None = None,
    stage_name: str = "setup",
):
    if extra_indicators is None:
        extra_indicators = []
    if json_data_conditions is None:
        return [], {}, []
    setup_indicators = []
    condition_for_setup_indicators = {}
    for setup_indicator in json_data_conditions:
        if (
            setup_indicator["source"] == "indicator"
            and setup_indicator["stage"] == stage_name
        ):
            indicator_string = setup_indicator["fn"]
            for period in setup_indicator["args"].values():
                indicator_string += f"_{period}"
            setup_indicators.append(indicator_string)
            arr = []
            if (
                setup_indicator.get("is_dynamic_value") is not None
                and setup_indicator["is_dynamic_value"]
                and setup_indicator["dynamic_fn"]["source"] == "indicator"
            ):
                indicator_string_DYNAMIC: str = setup_indicator["dynamic_fn"]["fn"]
                for period in setup_indicator["dynamic_fn"]["args"].values():
                    indicator_string_DYNAMIC += f"_{period}"
                indicator_string_DYNAMIC = indicator_string_DYNAMIC.lower()
                setup_indicator["value"] = indicator_string_DYNAMIC
                extra_indicators.append(indicator_string_DYNAMIC)
            if condition_for_setup_indicators.get(indicator_string) is None:
                arr = [
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                ]
                # arr = ['<     ', '<=  ', '>     ', '>=  ', '==  ',  '!=  ',  'crosses_above', 'crosses_below', "ticks", "percent"]
                # - **Trends**: `increasing`, `decreasing`, `new_high`, `new_low` (the `value` field represents the N-bars lookback period)
                # - **Boolean States**: `is_true`, `is_false`
                # ADD HERE FIX HERE

            else:
                arr = condition_for_setup_indicators[indicator_string]
            if setup_indicator["op"] == "<":
                if not np.isnan(arr[0]) or not np.isnan(arr[1]):
                    return None, None, None
                arr[0] = setup_indicator["value"]
            elif setup_indicator["op"] == "<=":
                if not np.isnan(arr[0]) or not np.isnan(arr[1]):
                    return None, None, None
                arr[1] = setup_indicator["value"]
            elif setup_indicator["op"] == ">":
                if not np.isnan(arr[2]) or not np.isnan(arr[3]):
                    return None, None, None
                arr[2] = setup_indicator["value"]
            elif setup_indicator["op"] == ">=":
                if not np.isnan(arr[2]) or not np.isnan(arr[3]):
                    return None, None, None
                arr[3] = setup_indicator["value"]
            elif setup_indicator["op"] == "==":
                if (
                    not np.isnan(arr[4])
                    or not np.isnan(arr[5])
                    or not np.isnan(arr[3])
                    or not np.isnan(arr[2])
                    or not np.isnan(arr[1])
                    or not np.isnan(arr[0])
                ):
                    return None, None, None
                arr[4] = setup_indicator["value"]
            elif setup_indicator["op"] == "!=":
                if (
                    not np.isnan(arr[4])
                    or not np.isnan(arr[5])
                    or not np.isnan(arr[3])
                    or not np.isnan(arr[2])
                    or not np.isnan(arr[1])
                    or not np.isnan(arr[0])
                ):
                    return None, None, None
                arr[5] = setup_indicator["value"]
            elif setup_indicator["op"] == "crosses_above":
                # print(setup_indicator)
                arr[6] = setup_indicator["value"]
                # print(arr)
            elif setup_indicator["op"] == "crosses_below":
                arr[7] = setup_indicator["value"]
            elif setup_indicator["op"] == "between":
                if (
                    not np.isnan(arr[0])
                    or not np.isnan(arr[1])
                    or not np.isnan(arr[2])
                    or not np.isnan(arr[3])
                ):
                    return None, None, None
                arr[0] = setup_indicator["value"]
                arr[2] = setup_indicator["value2"]
                if arr[0] < arr[2]:
                    temp_arr_val = arr[2]
                    arr[2] = arr[0]
                    arr[0] = temp_arr_val
            elif setup_indicator["op"] == "within_ticks":
                arr[10] = setup_indicator["value2"]  # tick amount
                arr[8] = setup_indicator["value"]  # indicator/static
            elif setup_indicator["op"] == "within_pct":
                arr[10] = setup_indicator["value2"]  # % amount
                arr[9] = setup_indicator["value"]  # indicator/static
            condition_for_setup_indicators[indicator_string] = arr
    return setup_indicators, condition_for_setup_indicators, extra_indicators


def extract_risk_params(json_data, extra_indicators: list[str] | None = None):
    risk_params_4_1 = json_data.get("stop", {})
    adr_stop = risk_params_4_1.get("adrstop", [np.nan, np.nan, np.nan])
    atr_stop = risk_params_4_1.get("atrstop", [np.nan, np.nan])
    if not np.isnan(adr_stop[0]):
        extra_indicators.append(f"adr_{adr_stop[0]}_{int(adr_stop[1])}")
    if not np.isnan(atr_stop[0]):
        extra_indicators.append(f"atr_{int(atr_stop[0])}")

    fixed_percent_stop = risk_params_4_1.get("fixed_percent_stop", np.nan)
    fixed_dollar_stop = risk_params_4_1.get("fixed_dollar_stop", np.nan)
    volatility_sanity_cap_adr = risk_params_4_1.get(
        "volatility_sanity_cap_adr", [np.nan, np.nan, np.nan]
    )
    volatility_sanity_cap_atr = risk_params_4_1.get(
        "volatility_sanity_cap_atr", [np.nan, np.nan]
    )
    if not np.isnan(volatility_sanity_cap_adr[0]):
        extra_indicators.append(
            f"adr_{volatility_sanity_cap_adr[0]}_{int(volatility_sanity_cap_adr[1])}"
        )
    if not np.isnan(volatility_sanity_cap_atr[0]):
        extra_indicators.append(f"atr_{int(volatility_sanity_cap_atr[0])}")

    zonestopob = 1.0 if risk_params_4_1.get("zonestopob", 0.0) == True else 0.0
    zonestopfvg = 1.0 if risk_params_4_1.get("zonestopfvg", 0.0) == True else 0.0
    zonestopifvg = 1.0 if risk_params_4_1.get("zonestopifvg", 0.0) == True else 0.0
    zonestopsweep = 1.0 if risk_params_4_1.get("zonestopsweep", 0.0) == True else 0.0

    risk_4_1_params_numpy = [
        adr_stop[0],
        adr_stop[1],
        adr_stop[2],
        atr_stop[0],
        atr_stop[1],
        fixed_percent_stop,
        fixed_dollar_stop,
        volatility_sanity_cap_adr[0],
        volatility_sanity_cap_adr[1],
        volatility_sanity_cap_adr[2],
        volatility_sanity_cap_atr[0],
        volatility_sanity_cap_atr[1],
        zonestopob,
        zonestopfvg,
        zonestopifvg,
        zonestopsweep,
    ]

    risk_params_4_2 = json_data.get("risk", {})
    sizing = risk_params_4_2.get("sizing", "")
    percentage_risk = dollar_risk = fixed_quantity = np.nan
    if sizing == "fixed_fractional":
        percentage_risk = risk_params_4_2.get("quantity", np.nan)
    elif sizing == "fixed_dollar":
        dollar_risk = risk_params_4_2.get("quantity", np.nan)
    elif sizing == "fixed_quantity":
        fixed_quantity = risk_params_4_2.get("quantity", np.nan)
    max_risk_per_trade = risk_params_4_2.get("max_risk_per_trade", np.nan)

    # TODO V1.x
    # atr_multiplier = np.nan
    # volatility_normalized = risk_params_4_2.get("volatility_normalized", [False, 0, 0])
    # atr_param = volatility_normalized[1]
    # atr_multiplier = volatility_normalized[2]
    # if atr_param > 0 and f"atr_{atr_param}" not in (
    #     setup_indicators + entry_indicators + extra_indicators
    # ):
    #     extra_indicators.append(f"atr_{atr_param}")

    contract_rounding_rule = risk_params_4_2.get("contract_rounding_rule", False)
    if contract_rounding_rule:
        contract_rounding_rule = 1
    else:
        contract_rounding_rule = 0

    risk_4_2_params_numpy = np.array(
        [
            percentage_risk,
            dollar_risk,
            fixed_quantity,
            max_risk_per_trade,
            # atr_multiplier,
            contract_rounding_rule,
        ]
    )

    risk_params_4_3 = json_data.get("target", {})
    r_multiple_targets = risk_params_4_3.get(
        "rr_multiple_targets", [[np.nan, np.nan] for _ in range(5)]
    )  # [risk_multiple, % of position to exit], [risk_multiple, % of position to exit], ...)
    fixed_percent_target = risk_params_4_3.get("fixed_percent_target", np.nan)
    fixed_dollar_target = risk_params_4_3.get("fixed_dollar_target", np.nan)
    level_target = risk_params_4_3.get("level_target", np.nan)
    time_based_takes = risk_params_4_3.get(
        "time_based_takes", [[np.nan, np.nan] for _ in range(5)]
    )  #  (int # of timebasedtargets, [# of candles of time (int), % of position to exit], [# of candles of time, % of position to exit], ...)
    # trailing_only_mode = risk_params_4_3.get("trailing_only_mode", False)
    risk_params_4_4 = {}
    risk_params_4_4 = risk_params_4_3.get("then", {})
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
    if len(time_based_takes) > 5:
        return 220
    if len(time_based_takes) < 5:
        time_based_takes.extend(
            [np.nan, np.nan] for _ in range(5 - len(time_based_takes))
        )

    risk_4_3_params_lists_numpy = np.array(
        [
            np.asarray(r_multiple_targets, dtype=np.float64),
            np.asarray(time_based_takes, dtype=np.float64),
        ],
        dtype=np.float64,
    )
    risk_4_3_params_numpy = np.array(
        [
            fixed_percent_target,
            fixed_dollar_target,
            level_target,
        ]
    )

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
    structure_trail = risk_params_4_4.get("structure_trail", np.nan)
    if not np.isnan(structure_trail):
        extra_indicators.append(f"structuresllong_{int(structure_trail)}")
        extra_indicators.append(f"structureslshort_{int(structure_trail)}")

    runnerdisposition = 1.0 if risk_params_4_4.get("runnerdisposition", False) else 0.0
    ma_multiple = ma_trail[2]
    atr_multiple = atr_trail[1]
    sar_multiple = sar_trail[2]
    supertrend_multiple = supertrend_trail[2]

    risk_4_4_params_numpy = np.array(
        [
            rr_trigger_move_stop_breakeven,  # 0
            rr_target_lock_profit_ratchet,  # 1
            rr_stop_lock_profit_ratchet,  # 2
            ma_params[0],  # 3
            ma_params[1],  # 4
            ma_multiple,  # 5
            atr_params[0],  # 6
            atr_multiple,  # 7
            sar_params[0],  # 8
            sar_params[1],  # 9
            sar_multiple,  # 10
            supertrend_params[0],  # 11
            supertrend_params[1],  # 12
            supertrend_multiple,  # 13
            dollar_trail,  # 14
            percent_trail,  # 15
            bar_trail,  # 16
            never_widen_invariant,  # 17
            runnerdisposition,  # 18
            structure_trail,  # 19
        ]
    )

    risk_params_4_5 = json_data.get("session", {})
    close_on_session_close = (
        1.0 if risk_params_4_5.get("close_on_session_close", False) else 0.0
    )
    exit_n_minutes_before_close = risk_params_4_5.get(
        "exit_n_minutes_before_close", np.nan
    )
    if close_on_session_close and np.isnan(exit_n_minutes_before_close):
        exit_n_minutes_before_close = 1
    max_hold_n_bars = risk_params_4_5.get("max_hold_n_bars", np.nan)
    exit_before_earnings = (
        1.0 if risk_params_4_5.get("exit_before_earnings", False) else 0.0
    )
    close_before_weekend = (
        1.0 if risk_params_4_5.get("close_before_weekend", False) else 0.0
    )
    exit_on_no_trade_days = (
        1.0 if risk_params_4_5.get("exit_on_no_trade_days", False) else 0.0
    )
    risk_4_5_params_numpy = np.array(
        [
            exit_n_minutes_before_close,
            max_hold_n_bars,
            exit_before_earnings,
            close_before_weekend,
            exit_on_no_trade_days,
        ]
    )

    risk_params_4_6 = json_data.get("risk", {})
    max_trades_per_session = risk_params_4_6.get("max_trades_per_session", np.nan)
    max_loss_per_session_rr = risk_params_4_6.get("max_loss_per_session_rr", np.nan)
    max_loss_per_session_percent = risk_params_4_6.get(
        "max_loss_per_session_percent", np.nan
    )
    max_loss_per_session_dollar = risk_params_4_6.get(
        "max_loss_per_session_dollar", np.nan
    )

    max_consecutive_losses = risk_params_4_6.get(
        "max_consecutive_losses", [np.nan, np.nan]
    )  # [int # of losses, # candles to stop for]
    number_of_consecutive_losses = max_consecutive_losses[0]
    n_candles_to_stop_for = max_consecutive_losses[1]
    max_positions_per_symbol = risk_params_4_6.get("max_positions_per_symbol", 1)
    n_candles_wait_after_stop = risk_params_4_6.get("n_candles_wait_after_stop", 0)

    first_n_candle_session_excluded = risk_params_4_6.get(
        "first_n_candle_session_excluded", 0
    )
    last_n_candle_session_excluded = risk_params_4_6.get(
        "last_n_candle_session_excluded", 0
    )
    n_candles_wait_after_trade_entry = risk_params_4_6.get(
        "n_candles_wait_after_trade_entry", 0
    )
    n_candles_wait_after_trade_exit = risk_params_4_6.get(
        "n_candles_wait_after_trade_exit", 0
    )

    risk_4_6_params_numpy = np.array(
        [
            max_trades_per_session,  # 0
            max_loss_per_session_rr,  # 1
            max_loss_per_session_percent,  # 2
            max_loss_per_session_dollar,  # 3
            number_of_consecutive_losses,  # 4
            n_candles_to_stop_for,  # 5
            max_positions_per_symbol,  # 6
            n_candles_wait_after_stop,  # 7
            first_n_candle_session_excluded,  # 8
            last_n_candle_session_excluded,  # 9
            n_candles_wait_after_trade_entry,  # 10
            n_candles_wait_after_trade_exit,  # 11
        ]
    ).astype(np.float64)
    return (
        extra_indicators,
        risk_4_1_params_numpy,
        risk_4_2_params_numpy,
        risk_4_3_params_numpy,
        risk_4_3_params_lists_numpy,
        risk_4_4_params_numpy,
        risk_4_5_params_numpy,
        risk_4_6_params_numpy,
    )


def get_indicator_conditions_from_jsons(json_data):
    setup_indicators, condition_for_setup_indicators, extra_indicators = (
        obtain_conditions_for_setup_indicators(
            json_data.get("setup"), extra_indicators=[], stage_name="setup"
        )
    )

    entry_indicators, condition_for_entry_indicators, extra_indicators = (
        obtain_conditions_for_setup_indicators(
            json_data.get("entry", {}).get("conditions", []),
            extra_indicators=extra_indicators,
            stage_name="trigger",
        )
    )
    (
        universe_indicators,
        condition_for_universe_indicators,
        universe_extra_indicators,
    ) = obtain_conditions_for_setup_indicators(
        json_data.get("setup", {}),
        extra_indicators=[],
        stage_name="universe",
    )
    return (
        setup_indicators,
        condition_for_setup_indicators,
        entry_indicators,
        condition_for_entry_indicators,
        universe_indicators,
        condition_for_universe_indicators,
        extra_indicators,
        universe_extra_indicators,
    )
