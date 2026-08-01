from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch


def create_pdf_report(evaluation_result, output_path):
    """
    Creates a PDF evaluation report.
    """

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Test Case Evaluation Report</b>", styles["Title"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    for key, value in evaluation_result.items():

        if isinstance(value, list):

            story.append(Paragraph(f"<b>{key}</b>", styles["Heading2"]))

            for item in value:
                story.append(Paragraph(f"• {item}", styles["Normal"]))

        else:

            story.append(
                Paragraph(
                    f"<b>{key}</b>: {value}",
                    styles["BodyText"]
                )
            )

    doc.build(story)