from pydantic import BaseModel, HttpUrl
from markdown import markdown
from datetime import date, datetime
import json
import os
from bs4 import BeautifulSoup
import re
from pathlib import Path

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
    href: HttpUrl

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
    def load(cls, file: os.PathLike):
        
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

        return cls(
            event_number=event_number,
            title=title,
            event_date=event_date,
            content=content,
            button=button
        )