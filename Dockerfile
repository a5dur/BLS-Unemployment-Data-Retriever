# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY stateUnemployment.py .
COPY countyUnemployment.py .
COPY placeUnemployment.py .
COPY merger.py .
COPY series_ids_states.json .
COPY state_abbreviations.json .
COPY series_ids_county_master.json .
COPY series_ids_city.json .



RUN pip install requests pandas

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
