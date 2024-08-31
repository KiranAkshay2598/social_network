FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_network.wsgi:application"]
