from fastapi import FastAPI
from app.routes import resume
from app.services.github_service import GitHubService
app =FastAPI()

# register the routes

app.include_router(resume.router)
@app.get("/")
def home():
    return {"message": "Career Copilot is Running!"}

def main():
    print("Hello from career-copilot!")


if __name__ == "__main__":
    main()
