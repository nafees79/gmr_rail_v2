import uvicorn
# from dotenv import load_dotenv

if __name__ == "__main__":
    # load_dotenv()
    uvicorn.run("api:app", reload=True, host="192.168.1.14", port=7022)
    # uvicorn.run("api:app", reload=True, host="10.10.10.31", port=7026)
    
