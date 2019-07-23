FROM python:2.7-slim
MAINTAINER Adam Converse <adam.converse@gmail.com>
COPY app /app
WORKDIR "/app"
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
