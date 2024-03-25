# Assistant


### Description: 
The gpt-3.5-turbo-based assistant allows users to upload pdf documents and ask questions related to those documents.


## Installation:

Clone the project and then go to the root directory and create .env file like in .env.example 
(You might want to change the credentials). Then you can install app in tho ways:


### 1. Installation with docker:

Go to the root dir and build the image:

```commandline
docker build -t docs_assistant .
```
then run container:
```commandline
docker run -p 127.0.0.1:8000:8000 -v .:/app docs_assistant
```

### 2. Manual installation:

First install the dependencies from the pyproject.toml file (you will need poetry, so if you don't have it, install 
it using the 'pip install poetry' command):


```commandline
poetry install
```

Then run command:

```commandline
uvicorn app.main:app
```

## Usage:

To upload document you have to send post request to http://127.0.0.1:8000/api/v1/assistant/upload-file

To ask question you have to send post request to http://127.0.0.1:8000/api/v1/assistant/send-question

with request body parameter {"question": "your question"}

Swagger documentation is available at http://127.0.0.1:8000/docs#/
