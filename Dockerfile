FROM python:3.7.2 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.7.2-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY main_predictor/ .

ENV PATH=/root/.local:$PATH

CMD [ "python3", "dream_team/dream_team.py" ]