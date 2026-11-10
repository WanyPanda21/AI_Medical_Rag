
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.units import inch
from xml.sax.saxutils import escape

from src.disease_data import DISEASES


def generate_pdf():
    os.makedirs("output", exist_ok=True)

    pdf_path = "output/diseases_symptoms_medicines.pdf"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        textColor=colors.darkblue,
        fontSize=20,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "DiseaseHeading",
        parent=styles["Heading2"],
        textColor=colors.darkblue,
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        leading=15,
        spaceAfter=8
    )

    story = []

    story.append(
        Paragraph(
            "Medical Knowledge Base",
            title_style
        )
    )

    story.append(
        Paragraph(
            "50 Diseases, Symptoms, Common Medicines and Precautions",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Educational reference only:</b> This document is "
            "not a diagnostic or prescribing guide. Medicine examples "
            "require professional assessment before use.",
            body_style
        )
    )

    story.append(Spacer(1, 15))

    for index, disease in enumerate(DISEASES, 1):

        story.append(
            Paragraph(
                f"{index}. {escape(disease['name'])}",
                heading_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Category:</b> {escape(disease['category'])}",
                body_style
            )
        )

        symptoms = ", ".join(disease["symptoms"])
        medicines = ", ".join(disease["medicines"])

        story.append(
            Paragraph(
                f"<b>Symptoms:</b> {escape(symptoms)}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Common medicines or treatment classes:</b> "
                f"{escape(medicines)}",
                body_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Precautions:</b> "
                f"{escape(disease['precautions'])}",
                body_style
            )
        )

        story.append(Spacer(1, 12))

    doc.build(story)

    print(f"PDF generated successfully: {pdf_path}")
    print(f"Total diseases: {len(DISEASES)}")

    return pdf_path


if __name__ == "__main__":
    generate_pdf()
