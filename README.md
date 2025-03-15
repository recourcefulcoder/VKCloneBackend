# VKCloneBackend
A backend for a social media application, written on python

_Current project's main goals are_:
- learning new, valuable concepts of backend development in practice
- demonstrating my current knowledge and skills

It **does not** make business sense, meaning it doesn't intend to crash all 
competitor on the market with some innovative feature (yet I don't rule out 
some new ideas may appear during development)

For seeing final goal head towards [final goal](#sketch-of-the-final-version-of-the-application) section,
for documentation see [Documentation](#documentation) section

Table of contents:
- [Final goal](#sketch-of-the-final-version-of-the-application)
- [Deployment guide](#deployment)
  - [Running in dev mode](#running-application-in-developer-mode) 
- [Documentation](#documentation)
  - [Code style conventions](#code-style-conventions)
  - [General documentation](#code-documentation)

## Sketch of the final version of the application

### Short intro
This section states an end goal for this application. This is by no means current state of an 
application - to see currently released functionality better see [start description](#vkclonebackend) or 
[documentation](#documentation) - but my outline for what do I want to see in the end and what are potential areas
for scaling of this application are.

### Sketch itself

Current application is supposed to be an API, written as a backend code for a social media platform.
It is supposed to be designed in microservices paradigm, implementing such services as:

| Service | Responsibilities |
| ------- | ----------- |
| User | authentication, registration, user profile management, etc. |
| Post | creation of posts, edition, main feed of the application |
| Notification | getting/marking notifications as read, websocket connection for live notifications |
| Media processing | CPU-intensive media operations + storage |
|||
| Analytics | user behaviour analytics (postponed indefinitely) |

Technologies to be used (meaning which _may be attached_):

| Technology | Goal |
| ------- | ----------- |
| DevOps | All list of possible DevOps practices, meaning CI/CD, Docker configuration, Kubernetes config files, etc. |
| FastAPI | As a base for an API |
| Celery | For executing background tasks (e.g., notifications, analytics) |
| Redis | For caching and storing test results |
| RabbitMQ | Message broker for task distribution |
| Apache Kafka | Event-driven communication between services |
| PostgreSQL | Database backend |


## Deployment
### Running single service in developer mode
1. Install dependencies

From root directory of the service execute in your system's CLI
```bash
pip install -r requirements.txt
```
2. Run FastAPI

From "src" directory of the service run
```bash
fastapi dev main.py
``` 
3. _Enjoy ^\_^_

## Documentation

Any documentation will appear there as code will appear in the project ^_^

### Code style conventions
It is crucial to state all development practices on the start - so here we are, stating _style conventions_!

Main judge of compliance with code agreements will be [flake8](https://flake8.pycqa.org/en/latest/) linting tool with following plugins installed:
- [flake8-print](https://pypi.org/project/flake8-print/)
- [flake8-import-order](https://pypi.org/project/flake8-import-order/)

All plugins are listed in **_linting-req.txt_** requirements file

Besides of obvious requirement for meeting PEP8 requirements, _import-order requirement_ is also introduced:

- Chosen import order rule - cryptography for [flake8-import-order plugin](https://pypi.org/project/flake8-import-order/)

### Code documentation
Code is documented per service in order not to overload this manual. Each service has it's own
README.md, where you can find its local design conventions and class/function docs.

However, current section is still usable as it will document integration between services, as well as 
some shared codebase. 

For now, since no shared codebase nor integration between services is not implemented, it is left intentionally blank