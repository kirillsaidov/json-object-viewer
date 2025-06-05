# module main

# system
import os

# web
import aiofiles
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

# app
app = FastAPI()
fdir = os.path.dirname(__file__) # file directory

@app.get('/favicon.ico')
def favicon():
    return FileResponse(os.path.join(fdir, '..', 'imgs', 'favicon.ico'))


@app.get("/", response_class=HTMLResponse)
async def serve_html():
    async with aiofiles.open(os.path.join(fdir, 'templates', 'index.html'), mode='r') as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)
