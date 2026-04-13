import httpx
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.utils.promt_template import get_jd_parser_prompt
from app.models.schemas import JDParsed
from app.utils.logger import get_logger

logger = get_logger(__name__)

class JDParser:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-oss:20b",
            api_key="ollama",
            base_url="http://localhost:11434/v1"
        )

        self.prompt = get_jd_parser_prompt()

        self.chain = self.prompt | self.llm.with_structured_output(JDParsed)

    async def extract_structured(self, jd_text:str) -> JDParsed:
        logger.info("calling LLM for structured JD parsing")

        try:
            result = await self.chain.ainvoke(
                {
                    "jd": jd_text
                }
            )
            logger.info("JD parsing successful")
            return result
        except Exception as e:
            logger.error(f"Error during JD parsing: {e}")
            return JDParsed()
            
        
    