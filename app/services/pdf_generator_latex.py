from pylatex import Document, Section, Subsection, Command
from pylatex.utils import bold
from datetime import datetime
from app.utils.logger import get_logger

logger = get_logger(__name__)

def clean_latex(text: str) -> str:
    replacements = {
        "“": '"',
        "”": '"',
        "’": "'",
        "–": "-",
        "—": "-",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

class PDFGenerator:

    def generate(self, user, projects, bullets):
        logger.info("Generating PDF Resume")

        doc = Document()

        # PERSONAL INFO
        
        with doc.create(Section(user.personal_info.name)):
            doc.append(clean_latex(user.personal_info.email + " | "))
            doc.append(clean_latex(user.personal_info.phone + " | "))
            doc.append(clean_latex(user.personal_info.location))
        
        # EDUCATION
        with doc.create(Section("Education")):
            for edu in user.education:
                doc.append(clean_latex(bold(edu.degree) + " - " + edu.institution + "\n"))
                doc.append(clean_latex(edu.duration + "\n"))

        # EXPERIENCE
        if user.experience:
            with doc.create(Section("Experience")):
                for exp in user.experience:
                    doc.append(clean_latex(bold(exp.role) + " - " + exp.company + "\n"))
                    for r in exp.responsibilities:
                        doc.append(clean_latex("- " + r + "\n"))
        
        # PROJECTS
        with doc.create(Section("Projects")):
            for proj,bullet in zip(projects, bullets):
                doc.append(clean_latex(bold(proj.title) + "\n"))

                for b in bullet["bullets"]:
                    doc.append(clean_latex("• " + clean_latex(b) + "\n"))
        
        # SKILLS
        with doc.create(Section("Skills")):
            skills = ", ".join(user.skills.programming_languages + user.skills.frameworks + user.skills.tools + user.skills.databases + user.skills.soft_skills + user.skills.other_relevant_technical_skills)
            doc.append(clean_latex(skills))
        
        now = datetime.now().strftime("%Y%m%d_%H%M")
        file_path = f"logs/{user.personal_info.name.replace(' ', '_')}_{now}_Resume"
        doc.generate_pdf(file_path, compiler="pdflatex", clean_tex=False)

        logger.info(f"PDF Resume Generated successfully: {file_path}")
        return file_path
