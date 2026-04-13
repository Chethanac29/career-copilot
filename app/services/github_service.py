import httpx
from datetime import datetime, timedelta
from app.utils.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com/search/repositories"
        self.headers = {
            "Authorization": f"token {settings.github_token}",
            "Accept": "application/vnd.github.v3+json"
            }

    async def search_projects(self, query: str):
        logger.info(f"Searching GitHub with query: {query}")

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(
                    self.base_url,
                    headers=self.headers,
                    params={
                        'q': query,
                        'sort': 'stars',
                        'order': 'desc',
                        'per_page': 3
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                    return []
                
                data = response.json()

                results = []
                for item in data.get("items", []):
                    results.append(
                        {
                            "name": item["name"],
                            "url": item["html_url"],
                            "stars": item["stargazers_count"],
                            "description": item["description"],
                            "language": item["language"]
                        }
                    )
                
                logger.info(f"GitHub search successful, found {len(results)} projects")

                return results
        except Exception as e:
            logger.error(f"GitHub search failed: {e}")
            return []
            
            