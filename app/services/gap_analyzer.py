from app.utils.logger import get_logger

logger = get_logger(__name__)

class GapAnalyzer:

    def _normalize(self, skills):
        return set(skill.lower().strip() for skill in skills)
    
    def _safe_list(self, x):
        return x if x else []

    def analyze(self, parsed_jd, user_skills):

        # flatten JD Skills
        jd_skills_raw = set(
            self._safe_list(parsed_jd.programming_languages) +
            self._safe_list(parsed_jd.frameworks) +
            self._safe_list(parsed_jd.tools) +
            self._safe_list(parsed_jd.databases) +
            self._safe_list(parsed_jd.other_relevant_technical_skills)
        )
        jd_skills = self._normalize(jd_skills_raw)

        #flatten user skills
        user_skill_set_raw = set(
            self._safe_list(user_skills.programming_languages) +
            self._safe_list(user_skills.frameworks) +
            self._safe_list(user_skills.tools) +
            self._safe_list(user_skills.databases) + 
            self._safe_list(user_skills.other_relevant_technical_skills)
        )
        user_skill_set = self._normalize(user_skill_set_raw)


        matched_skills = jd_skills.intersection(user_skill_set)
        missing_skills = jd_skills.difference(user_skill_set)

        score = 0

        if jd_skills:
            score = round(len(matched_skills) / len(jd_skills) * 100, 2)
        
        logger.info(f"Gap Analysis Score: {score}% - Matched: {len(matched_skills)}, Missing: {len(missing_skills)}")

        return {
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills),
            "match_score": score
        }