from pydantic import BaseModel, HttpUrl, AnyUrl
from typing import Union
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from markdown import markdown
from datetime import date, datetime
import json
import os
from bs4 import BeautifulSoup
import re
from pathlib import Path

def validate_url(url: str) -> str:
    # If it's a relative URL starting with '/', return as is
    if url.startswith('/'):
        return url
    # If it's a relative URL without leading slash, add it
    if not url.startswith(('http://', 'https://', '/')):
        return f'/{url}'
    # If it's an absolute URL, let pydantic validate it
    if url.startswith(('http://', 'https://')):
        return str(HttpUrl(url))
    return url

# Custom URL type that accepts both relative and absolute URLs
RelativeOrHttpUrl = Annotated[str, BeforeValidator(validate_url)]

class DataModel(BaseModel):

    @classmethod
    def load(cls, file: os.PathLike) -> 'DataModel':

        with open(file) as f:
            data = json.load(f)

        return cls(**data)
    
    @classmethod
    def load_list(cls, file: os.PathLike) -> list['DataModel']:

        with open(file) as f:
            data = json.load(f)
        
        return [cls(**el) for el in data]


class Button(BaseModel):

    text: str
    href: RelativeOrHttpUrl

class Post(DataModel):

    title: str
    image: str
    contents: list[str]
    button: Button

    @property
    def content(self) -> str:
        return '\n'.join([f'<p>\n{paragraph}</p>' for paragraph in self.contents])
    
class EventPost(DataModel):

    event_number: int
    title: str
    image: str = 'ds_02.jpg'
    event_date: date
    content: str
    button: Button | None = None
    
    @classmethod
    def load(
        cls,
        file: os.PathLike,
        images_dir: os.PathLike
    ):
        
        # Get event number
        file_path = Path(file)
        match = re.match(r'^event_([0-9]+).md$', file_path.name)
        event_number = int(match.group(1))

        # Load file and convert to soup
        with open(file_path) as cf:
            md = cf.read()

        html = markdown(md, extensions=['md_in_html'])
        soup = BeautifulSoup(html, features='html.parser')
        
        # Get title and date
        title = soup.h1.text
        event_date = datetime.strptime(soup.p.text, '%Y-%m-%d').date()

        # Remove top of html
        soup.h1.decompose()
        soup.h2.decompose()
        soup.p.decompose()

        # Find button if it exists
        button = None
        headers = soup.find_all('h2')
        
        for header in headers:

            if header.text == 'Meetup':

                link = header.find_next_sibling('p').a

                button = Button(
                    text=link.text,
                    href=link.attrs['href']
                )

                header.decompose()
                link.decompose()

        # Clean up content
        content = soup.encode_contents().decode('utf-8').strip('\n')

        # Get image if it exists in the images directory
        image_file = images_dir / f'event_{str(event_number).zfill(3)}.jpg'
        if image_file.exists():
            image = image_file.name
        else:
            image = 'ds_02.jpg'

        return cls(
            event_number=event_number,
            title=title,
            event_date=event_date,
            content=content,
            button=button,
            image=image
        )

class Resource(DataModel):

    title: str
    url: RelativeOrHttpUrl
    description: str
    image: str = 'ds_02.jpg'