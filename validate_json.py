import json
from classes import CandleSize
from functions import obtain_conditions_for_setup_indicators


def validate_json(json_data):
    # ensure if equity >= 15min  timeframe
    if type(json_data["instrument"]) is str and json_data["instrument"] == "equity":
        if CandleSize(json_data["timeframe"]) < CandleSize.MINUTE_15:
            return 201

    setup_indicators, condition_for_setup_indicators, extra_indicators = (
        obtain_conditions_for_setup_indicators(
            json_data.get("setup", {}), extra_indicators=[]
        )
    )
    entry_indicators, condition_for_entry_indicators, extra_indicators = (
        obtain_conditions_for_setup_indicators(
            json_data.get("entry", {}).get("conditions", []),
            extra_indicators=extra_indicators,
        )
    )
    if setup_indicators is None or condition_for_setup_indicators is None:
        return 203  # Invalid setup indicators
    if entry_indicators is None or condition_for_entry_indicators is None:
        return 204  # Invalid entry indicators
    try:
        CandleSize(json_data["timeframe"])
    except ValueError:
        return 202

    return 200


if __name__ == "__main__":
    json_data = json.load(open("json/exampleJSONFile.json"))
    response = validate_json(json_data)

    if response == 200:
        print("Valid JSON file")
    else:
        print("Invalid JSON file")
