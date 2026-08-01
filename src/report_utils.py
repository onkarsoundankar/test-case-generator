import json


def generate_report(story_title, manual_test_cases, generated_test_cases):
    """
    Generate evaluation report for AI generated test cases.
    Returns a Python dictionary.
    """

    generated_scenarios = generated_test_cases.count("Scenario:")

    manual_count = len(manual_test_cases)


    # Coverage calculation
    # If generated scenarios are equal or more than
    # the provided acceptance criteria/manual cases,
    # consider coverage complete.

    if manual_count > 0:

        coverage_percent = min(
            round(
                (generated_scenarios / manual_count) * 100,
                2
            ),
            100
        )

    else:

        coverage_percent = 0



    report = {

        "story": story_title,

        "manual_test_cases": manual_count,

        "generated_scenarios": generated_scenarios,

        "coverage_percent": coverage_percent,

        "generated_test_cases": generated_test_cases

    }


    return report



def report_to_json(report):
    """
    Convert report dictionary into formatted JSON.
    """

    return json.dumps(
        report,
        indent=4
    )