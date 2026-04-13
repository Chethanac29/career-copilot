from langchain_core.prompts import ChatPromptTemplate
def get_jd_parser_prompt():
    return ChatPromptTemplate.from_template("""
    You are an expert job description analyzer.

    Extract structured information from the job description.

    Return structured output with:
    - programming_languages
    - frameworks
    - tools
    - databases
    - other_relevant_technical_skills
    - domain
    - seniority
    - key_responsibilities
    - keywords

    IMPORTANT:
    - Only extract relevant technical skills
    - Do not hallucinate
    - Keep lists concise

    Job Description:
    {jd}
    """)    

def get_project_generator_prompt():
    return ChatPromptTemplate.from_template("""
    You are an expert career coach.

    Generate 2–3 high-impact projects that will help a candidate get shortlisted.

    Context:
    - Job Description: {jd}
    - Missing Skills: {missing_skills}
    - Domain: {domain}

    Requirements:
    - Projects must be real-world and resume-worthy
    - Focus on missing skills
    - Use modern tools/tech
    - Avoid generic projects

    For each project provide:
    - title
    - description
    - technologies
    - github_query (short keyword-based search query for GitHub)

    Rules:
    - Use action verbs
    - Include measurable impact (if possible)
    - Keep output concise
                                            
    GitHub query rules:
    - Use 3–5 concise, common keywords
    - Prioritize primary technologies and core functionality
    - Avoid rare, overly specific, or niche terms
    - Do not include special characters or long phrases
    - Ensure the query is broad enough to return results
    - Prefer simple, commonly used developer search terms
    - Combine keywords using implicit AND (space-separated terms)
    - Use OR only when suggesting clear alternatives (e.g., "react OR vue")
    """
    )

def get_bullet_generator_prompt():
    return ChatPromptTemplate.from_template(
        """
        You are an expert resume writer.

        Generate ATS-friendly resume bullet points.

        Context:
        - Job Description: {jd}
        - Skills Required: {skills}
        - Project: {project_title}
        - Technologies: {technologies}
        - Description: {description}

        Requirements:
        - Each bullet must start with a strong action verb
        - Include relevant technologies
        - Include measurable impact if possible
        - Be concise (3-4 lines max)
        - Tailor towards the job description

        Generate 2–3 bullet points.
        """
    )