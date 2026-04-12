from fastapi import FastAPI

app =FastAPI()


@app.get("/")
def home():
    return {"message": "Career Copilot is Running!"}

def main():
    print("Hello from career-copilot!")


if __name__ == "__main__":
    main()
