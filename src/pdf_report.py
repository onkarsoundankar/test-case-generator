from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet



def create_pdf_report(
    evaluation_result,
    output_path
):

    doc = SimpleDocTemplate(
        output_path
    )


    styles = getSampleStyleSheet()


    story = []


    # Title

    story.append(
        Paragraph(
            "AI Test Case Evaluation Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,20)
    )


    # Story

    story.append(
        Paragraph(
            f"<b>User Story:</b> {evaluation_result.get('story_title','')}",
            styles["Normal"]
        )
    )


    story.append(
        Spacer(1,15)
    )


    # Metrics Table

    data = [

        ["Metric","Value"],

        [
            "Manual Test Cases",
            str(evaluation_result.get("manual_test_cases",0))
        ],

        [
            "Generated Scenarios",
            str(evaluation_result.get("generated_scenarios",0))
        ],

        [
            "Coverage",
            str(evaluation_result.get("coverage_percent",0))+"%"
        ]

    ]


    table = Table(data)


    table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None),
                ("VALIGN",(0,0),(-1,-1),"TOP")
            ]
        )
    )


    story.append(
        table
    )


    story.append(
        Spacer(1,20)
    )


    # Generated Tests

    story.append(
        Paragraph(
            "Generated BDD Test Cases",
            styles["Heading2"]
        )
    )


    gherkin = evaluation_result.get(
        "generated_test_cases",
        ""
    )


    for line in gherkin.split("\n"):


        if line.strip():


            story.append(

                Paragraph(
                    line.replace(
                        "<",
                        "&lt;"
                    ),
                    styles["Code"]
                )

            )

            story.append(
                Spacer(1,5)
            )


    doc.build(
        story
    )