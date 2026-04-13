# Career Copilot

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)
![License](https://img.shields.io/badge/License-MIT-green)

A FastAPI-powered AI backend that tailors resumes to a job description by running a multi-step pipeline:

1. Parse the job description into structured technical signals.
2. Analyze skill gaps against the user profile.
3. Generate high-impact project ideas to close gaps.
4. Find related GitHub repositories for inspiration.
5. Generate ATS-friendly project bullet points.
6. Export a resume file (currently DOCX in the active API route).

The project is designed for local, private execution with an Ollama-compatible OpenAI API endpoint and integrates with GitHub Search API for project recommendations.

## Table of Contents

- [What It Does](#what-it-does)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Pipeline Overview](#pipeline-overview)
- [Service Matrix](#service-matrix)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Run the API](#run-the-api)
- [API Endpoints](#api-endpoints)
- [Logging and Outputs](#logging-and-outputs)
- [Common Issues](#common-issues)
- [Development Notes](#development-notes)
- [License](#license)

---

## What It Does

- Accepts user profile + job description as JSON.
- Extracts structured JD fields such as:
	- programming languages
	- frameworks
	- tools
	- databases
	- domain, seniority, responsibilities, keywords
- Computes matched and missing skills with a match score.
- Generates 2-3 targeted projects based on missing skills.
- Searches top GitHub repositories for each generated project idea.
- Generates resume bullets per project aligned to the JD.
- Produces a resume file under `generated_resumes/<timestamp>/resume.docx`.

---

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic / pydantic-settings
- LangChain + langchain-openai
- Ollama-compatible chat endpoint (`http://localhost:11434/v1`)
- httpx (GitHub API calls)
- python-docx (active resume output)
- Optional generators included in codebase:
	- `pdfkit` + Jinja2 HTML template
	- `pylatex` PDF flow

---

## Project Structure

```text
career-copilot/
	app/
		main.py                  # FastAPI app entrypoint
		core/
			config.py              # Environment settings (GITHUB_TOKEN)
		models/
			schemas.py             # Request/response schema models
		routes/
			resume.py              # Main pipeline endpoint: POST /generate
		services/
			jd_parser.py           # JD structuring via LLM
			gap_analyzer.py        # Skill gap scoring
			project_generator.py   # Targeted project generation
			github_service.py      # GitHub repository search
			bullet_generator.py    # Resume bullet generation
			docx_generator.py      # Active resume file generation
			pdf_generator.py       # Optional HTML->PDF generator
			pdf_generator_latex.py # Optional LaTeX PDF generator
		templates/
			resume.html            # HTML template for pdf_generator.py
		utils/
			logger.py              # Console + file logging
			promt_template.py      # Prompt templates used by services
	logs/                      # Runtime logs and optional latex artifacts
	generated_resumes/         # Generated resume outputs
	pyproject.toml
	uv.lock
```

---

## Pipeline Overview

`POST /generate` orchestrates these stages in sequence:

1. **JD Parsing** (`JDParser`)
	 - LLM structured extraction into `JDParsed` model.
2. **Gap Analysis** (`GapAnalyzer`)
	 - Normalizes and compares JD vs user skills.
	 - Returns matched skills, missing skills, match score.
3. **Project Generation** (`ProjectGenerator`)
	 - Produces 2-3 resume-worthy project ideas for missing skills.
4. **GitHub Recommendations** (`GitHubService`)
	 - Searches top repositories (`per_page=3`) for each project query.
5. **Bullet Generation** (`BulletGenerator`)
	 - Generates ATS-focused project bullets.
6. **Resume Export** (`DocxGenerator`)
	 - Saves timestamped DOCX in `generated_resumes/`.

---

## Service Matrix

| Component | Purpose | Input | Output |
| --- | --- | --- | --- |
| `JDParser` | Extract structured technical requirements from JD | Raw JD text | `JDParsed` model |
| `GapAnalyzer` | Compare candidate skills vs JD skills | Parsed JD + user skills | Matched/missing skills + score |
| `ProjectGenerator` | Suggest targeted projects for skill gaps | JD + missing skills + domain | 2-3 generated projects |
| `GitHubService` | Recommend real repositories for each project idea | Search query | Top repo list (name/url/stars/etc.) |
| `BulletGenerator` | Create ATS-friendly project bullets | JD + project context | Bullet list per project |
| `DocxGenerator` | Export tailored resume file | User profile + projects + bullets | Timestamped `.docx` |

---

## Prerequisites

- Python `>=3.12`
- Local Ollama/OpenAI-compatible server reachable at `http://localhost:11434/v1`
- Model available: `gpt-oss:20b` (as configured in services)
- GitHub personal access token (for repository search)

---

## Environment Variables

Create `.env` in the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

Notes:
- `app/core/config.py` requires `GITHUB_TOKEN`.
- `.env` is loaded via `pydantic-settings`.

---

## Installation

### Option A: Using `uv` (recommended)

```bash
uv sync
```

### Option B: Using `pip`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

---

## Run the API

```bash
uv run uvicorn app.main:app --reload
```

Or with active virtual environment:

```bash
uvicorn app.main:app --reload
```

Default URL: `http://127.0.0.1:8000`

---

## API Endpoints

### `GET /`

Health message endpoint.

### `POST /generate`

Runs the full resume generation pipeline.

#### Request Body (example)

```json
{
	"user_profile": {
		"personal_info": {
			"name": "John Doe",
			"email": "john@example.com",
			"phone": "+1-555-000-1234",
			"location": "Bangalore, India",
			"linkedin": "https://linkedin.com/in/johndoe",
			"github": "https://github.com/johndoe"
		},
		"education": [
			{
				"degree": "B.Tech in Computer Science",
				"institution": "ABC University",
				"duration": "2019-2023",
				"score": "8.4 CGPA"
			}
		],
		"experience": [
			{
				"role": "Software Engineer Intern",
				"company": "Acme Labs",
				"duration": "Jan 2023 - Jun 2023",
				"location": "Remote",
				"responsibilities": [
					"Built internal REST APIs in FastAPI",
					"Improved CI pipeline duration by 20%"
				]
			}
		],
		"projects": [],
		"skills": {
			"programming_languages": ["Python", "SQL"],
			"frameworks": ["FastAPI"],
			"tools": ["Docker", "Git"],
			"databases": ["PostgreSQL"],
			"soft_skills": ["Communication"],
			"other_relevant_technical_skills": ["REST APIs"]
		},
		"achievements": [],
		"extracurriculars": [],
		"languages": ["English"],
		"hobbies": [],
		"raw_resume_text": "Optional raw text"
	},
	"job_description": {
		"raw_text": "Paste full JD text here (min length 50 chars)",
		"target_role": "Backend Engineer"
	}
}
```

#### Response (high-level)

```json
{
	"parsed_jd": {},
	"gap_analysis": {
		"matched_skills": [],
		"missing_skills": [],
		"match_score": 0
	},
	"projects": [],
	"github_recommendations": [],
	"generated_bullets": [],
	"pdf_path": "generated_resumes/20260413_010203/resume.docx"
}
```

Note: the response key is currently named `pdf_path`, but the active generator returns a `.docx` file path.

---

## Logging and Outputs

- App logs: `logs/app.log`
- Generated resumes: `generated_resumes/<timestamp>/resume.docx`
- Optional LaTeX flow may emit `.tex` and aux artifacts under `logs/`

---

## Common Issues

1. **`GITHUB_TOKEN` missing**
	 - Add token to `.env`.

2. **LLM connection errors**
	 - Ensure Ollama/OpenAI-compatible server is running at `http://localhost:11434/v1`.
	 - Confirm model `gpt-oss:20b` is available locally.

3. **GitHub API non-200 response**
	 - Validate token scopes and rate limits.

4. **No projects/bullets generated**
	 - Services are fail-safe and may return empty outputs on exceptions.
	 - Check `logs/app.log` for root cause.

---

## Development Notes

- Current route uses `DocxGenerator` for export.
- `pdf_generator.py` and `pdf_generator_latex.py` are available but not wired into the main `/generate` endpoint.
- `tests/test.py` currently includes a simple service test route stub and can be expanded into full automated tests.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

