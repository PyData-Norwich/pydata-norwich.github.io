from main import app
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from config import settings
import os
import shutil

if __name__ == '__main__':

    with TestClient(app=app) as client:

        for r in app.routes:
                
            if isinstance(r, APIRoute):
                
                url = r.path

                response = client.get(url=url)

                html = response.text

                local_path = settings.SITE_DIR / url.strip('/') / 'index.html'
                
                os.makedirs(local_path.parent, exist_ok=True)
                
                print(f'Rendering route {r.name} to {local_path}')

                with open(local_path, 'w') as f:
                    f.write(html)

    print('Copying static files')

    if settings.SITE_STATIC_DIR.exists():
        shutil.rmtree(settings.SITE_STATIC_DIR)

    shutil.copytree(settings.STATIC_DIR, settings.SITE_STATIC_DIR)