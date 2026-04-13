from fastapi import APIRouter, HTTPException
from app.utils.logger import get_logger

from app.services.jd_parser import JDParser
from app.models.schemas import ResumeRequest
from app.services.gap_analyzer import GapAnalyzer
from app.services.project_generator import ProjectGenerator
from app.services.github_service import GitHubService
from app.services.bullet_generator import BulletGenerator
# from app.services.pdf_generator import PDFGenerator
from app.services.docx_generator import DocxGenerator

import re

logger = get_logger(__name__)

router = APIRouter()

# initialise th Services
parser = JDParser()
gap_analyzer = GapAnalyzer()
project_generator = ProjectGenerator()
github_service = GitHubService()
bullet_generator = BulletGenerator()
# pdf_generator = PDFGenerator()
docx_generator = DocxGenerator()

def build_github_query(project):
    raw = f"{project.title} {' '.join(project.technologies)}"

    clean = re.sub(r"[^a-zA-Z0-9\s]", " ", raw).lower()
    words = clean.split()
    
    stop_words = {"platform", "system", "service", "application", "project"}
    filtered = [word for word in words if word not in stop_words]

    if len(filtered) > 6:
        return " ".join(filtered[:6])
    else:
        return " ".join(filtered)

@router.post("/generate")
async def generate_resume(request: ResumeRequest):

    jd = request.job_description
    user = request.user_profile

    if not jd.raw_text:
        raise HTTPException(status_code=400, detail="Job description text is required")
    

    #Step 1: Parse the JD to extract structured info
    parsed = await parser.extract_structured(jd.raw_text)

    #Sttep 2: Gap Analysis
    gap = gap_analyzer.analyze(parsed, user.skills)

    #Step 3: Generate Projects to fill the gap
    projects = await project_generator.generate(
        jd.raw_text,
        parsed,
        gap
    )

    github_results = []
    for project in projects:
        query = project.github_query or build_github_query(project)
        repos = await github_service.search_projects(query)
        github_results.append(
            {
                "project_title": project.title,
                "query": query,
                "repo": repos
            }
        )

    logger.info(f"Pipeline completed successfully for target role: {jd.target_role}")

    # Generate resume bullets for each project
    bullet_results = []
    for project in projects:
        bullets = await bullet_generator.generate(
            jd.raw_text,
            parsed,
            project
        )
        bullet_results.append(bullets.model_dump())
    
    pdf_path = docx_generator.generate(
        user,
        projects,
        bullet_results
    )

    return {
        "parsed_jd": parsed,
        "gap_analysis": gap,
        "projects": [project.dict() for project in projects],
        "github_recommendations": github_results,
        "generated_bullets": bullet_results,
        "pdf_path": pdf_path
    }