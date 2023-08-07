FROM python:3.11

ARG VERSION=0.0.1
ARG LABEL=${VERSION}

RUN python3 -m pip install --extra-index-url https://test.pypi.org/simple/ gpyt_openai==${VERSION}
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
