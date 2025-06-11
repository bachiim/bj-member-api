<p align='center'><a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a></p>

<p align="center"><em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em></p>

<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank"><img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&amp;branch=master" alt="Test"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage"></a>
<a href="https://pypi.org/project/fastapi" target="_blank"><img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&amp;label=pypi%20package" alt="Package version"></a>
<a href="https://pypi.org/project/fastapi" target="_blank"><img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions"></a>
</p>

## Installation
### 1. Create Virtual Environment
```bash
python -m venv venv
```
### 2. Activate Virtual Environment
```bash
source venv/Scripts/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run Database Migration
```bash
alembic upgrade head
```
### 5. Run Application
```bash
fastapi dev app/main.py
```
