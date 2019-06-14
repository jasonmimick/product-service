FROM python:3.7-alpine3.9 as base

FROM base as builder
RUN mkdir /app
COPY /app/requirements.txt /app
WORKDIR /app
RUN python -m pip install -r requirements.txt

FROM builder as runtime-image
COPY /app /app
ENTRYPOINT ["python"]
CMD ["app.py"]
