FROM python:3.7-alpine3.9
COPY /app /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
