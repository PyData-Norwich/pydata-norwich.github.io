from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from config import settings

def construct_handler(file: Path):

    def handler(request: Request) -> HTMLResponse:
        
        with open(file, 'r') as html_file:
            html = html_file.read()

        return HTMLResponse(
            content=html
        )
    
    return handler

pages = settings.SITE_DIR.glob('**/index.html')

app = FastAPI(
    title='Static app'
)

app.mount("/static", StaticFiles(directory=settings.SITE_STATIC_DIR), name="static")

for page in pages:

    name = page.parent.name

    if name == 'site':
        name = ''
        
    endpoint = f'/{name}'
    
    app.get(endpoint)(construct_handler(file=page))