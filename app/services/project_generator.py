from langchain_openai import ChatOpenAI

from app.models.schemas import ProjectList
from app.utils.logger import get_logger
from app.utils.promt_template import get_project_generator_prompt

logger = get_logger(__name__)

class ProjectGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-oss:20b",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0.3
        )

        self.prompt = get_project_generator_prompt()

        self.chain = self.prompt | self.llm.with_structured_output(ProjectList)

    async def generate(self, jd, parsed_jd, gap_analysis):
        logger.info("Generating Projects")

        try:
            result = await self.chain.ainvoke(
                {
                    "jd" : jd,
                    "missing_skills": gap_analysis["missing_skills"],
                    "domain": parsed_jd.domain
                }
            )
            logger.info("Projects Generated successfully")

            return result.projects
        except Exception as e:
            logger.error(f"Project Generation failed: {e}")
            return []
        

        

