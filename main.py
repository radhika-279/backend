import os
import sys
import models
from database import engine
import uvicorn


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from routers import user
from routers import address


print(os.path.dirname(os.path.dirname(os.path.abspath("__file__"))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("__file__"))))

app = FastAPI()
app.include_router(user.router)
app.include_router(address.router)


models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000)