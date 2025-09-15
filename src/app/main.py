from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from config import settings
from schemas import Post, EventPost, Resource

app = FastAPI(
    title='PyData Norwich',
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

templates = Jinja2Templates(settings.TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.get('/', name='home')
def home(request: Request) -> HTMLResponse:

    posts = Post.load_list(settings.DATA_DIR / 'posts_home.json')

    return templates.TemplateResponse(
        request=request,
        name='pages/index.html',
        context={
            'posts': posts
        }
    )

@app.get('/events', name='events')
def events(request: Request) -> HTMLResponse:

    files = settings.EVENTS_DIR.glob('*.md')

    events = [EventPost.load(file, settings.IMAGES_DIR) for file in files]
    events.sort(key=lambda event: event.event_number, reverse=True)

    return templates.TemplateResponse(
        request=request,
        name='pages/events.html',
        context={
            'page_header': {
                'title': 'Events',
                'sub_title': 'Information regarding upcoming and past events.',
                'icon': 'icons/calendar.svg'
            },
            'events': events
        }
    )

@app.get('/resources', name='resources')
def about(request: Request) -> HTMLResponse:

    resources = Resource.load_list(settings.DATA_DIR / 'resources.json')
    
    return templates.TemplateResponse(
        request=request,
        name='pages/resources.html',
        context={
            'page_header': {
                'title': 'Resources',
                'sub_title': 'Useful resources for Python, Data Science, AI, ML and more.',
                'icon': 'icons/books.svg'
            },
            'resources': resources
        }
    )

@app.get('/jobs', name='jobs')
def jobs(request: Request) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name='pages/jobs.html',
        context={
            'page_header': {
                'title': 'Jobs and Careers',
                'sub_title': 'Information and advice for Python and Data Science jobs in Norwich area.',
                'icon': 'icons/suitcase.svg'
            }
        }
    )

@app.get('/about', name='about')
def about(request: Request) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name='pages/about.html',
        context={
            'page_header': {
                'title': 'About us',
                'sub_title': 'Details about the PyData Norwich group.',
                'icon': 'icons/information.svg'
            }
        }
    )

