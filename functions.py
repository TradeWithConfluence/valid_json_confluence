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
