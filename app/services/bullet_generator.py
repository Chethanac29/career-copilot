from langchain_openai import ChatOpenAI

from app.models.schemas import BulletOutput
from app.utils.logger import get_logger
from app.utils.promt_template import get_bullet_generator_prompt

logger = get_logger(__name__)

class BulletGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-oss:20b",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0.3
        )

        self.prompt = get_bullet_generator_prompt()

        self.chain = self.prompt | self.llm.with_structured_output(BulletOutput)

    async def generate(self, jd, parsed_jd, project):
        logger.info("Generating Resume Bullets")

        try:
            result = await self.chain.ainvoke(
                {
                    "jd": jd,
                    "skills": parsed_jd.programming_languages, #+ parsed_jd.frameworks + parsed_jd.tools + parsed_jd.databases + parsed_jd.other_relevant_technical_skills,
                    "project_title": project.title,
                    "technologies": project.technologies,
                    "description": project.description
                }
            )
            logger.info("Resume Bullets Generated successfully")
            return result
        except Exception as e:
            logger.error(f"Bullet Generation failed: {e}")
            return BulletOutput(project_title=project.title, bullets=[])
        