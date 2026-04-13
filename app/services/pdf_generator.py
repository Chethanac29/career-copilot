import pdfkit
from jinja2 import Environment, FileSystemLoader
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFGenerator:

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("app/templates"))

    def generate(self, user, projects, bullets):

        logger.info("Generating PDF using HTML")

        template = self.env.get_template("resume.html")

        html_content = template.render(
            name=user.personal_info.name,
            email=user.personal_info.email,
            phone=user.personal_info.phone,
            location=user.personal_info.location,
            education=user.education,
            experience=user.experience,
            projects=list(zip(projects, bullets)),
            skills=", ".join(user.skills.programming_languages)
        )

        file_path = "resume.pdf"

        pdfkit.from_string(html_content, file_path)

        return file_path