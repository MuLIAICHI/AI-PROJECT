from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import Dict, Any
from io import BytesIO


class ReportGenerator:
    def generate_pdf(self, data: Dict[str, Any]) -> bytes:
        """Generate a PDF report from the analysis results."""
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("SEO Analysis Report")

        # Title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "SEO Analysis Report")

        pdf.setFont("Helvetica", 12)

        # Moz Metrics
        pdf.drawString(50, 720, "Moz Metrics:")
        pdf.setFont("Helvetica", 10)
        moz_data = data.get("moz_data", {}).get("metrics", {})
        y = 700
        for key, value in moz_data.items():
            pdf.drawString(60, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        # Scraped Data
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y - 20, "Scraped Data:")
        pdf.setFont("Helvetica", 10)
        scraped_data = data.get("scraped_data", {})
        y -= 40

        # Meta Tags
        pdf.drawString(60, y, "Meta Tags:")
        y -= 20
        meta_tags = scraped_data.get("meta_tags", {})
        for key, value in meta_tags.items():
            pdf.drawString(70, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        # Headings
        pdf.drawString(60, y - 20, "Headings:")
        y -= 40
        headings = scraped_data.get("headings", {})
        for key, value in headings.items():
            pdf.drawString(70, y, f"{key}: {value}")
            y -= 20

        # Images
        pdf.drawString(60, y - 20, "Images:")
        y -= 40
        images = scraped_data.get("images", {})
        for key, value in images.items():
            pdf.drawString(70, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        # Links
        pdf.drawString(60, y - 20, "Links:")
        y -= 40
        links = scraped_data.get("links", {})
        for key, value in links.items():
            pdf.drawString(70, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        # Content Quality
        pdf.drawString(60, y - 20, "Content Quality:")
        y -= 40
        content = scraped_data.get("content", {})
        for key, value in content.items():
            pdf.drawString(70, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        # Technical Elements
        pdf.drawString(60, y - 20, "Technical Elements:")
        y -= 40
        technical = scraped_data.get("technical", {})
        for key, value in technical.items():
            pdf.drawString(70, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        # Footer
        pdf.setFont("Helvetica", 8)
        pdf.drawString(50, 50, "Generated by SEO Analysis Tool")

        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
