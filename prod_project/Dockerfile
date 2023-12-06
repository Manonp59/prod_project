FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt /app


   # mettre à jour pip
RUN pip install --upgrade pip && \
   # installer les requirements (dans lesquels se trouve django)
   pip install -r requirements.txt


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# définit une variable d'environnement


COPY . .
# == . /app


EXPOSE 8000 

# gunicorn est un serveur de production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "prod_project.wsgi:application"]
