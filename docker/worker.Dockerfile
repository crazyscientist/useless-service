FROM python:3.11-slim
WORKDIR /opt
COPY src/libs /opt/useless_machine/libs
COPY src/services/worker /opt/useless_machine/services/worker
RUN pip install --no-cache-dir -r /opt/useless_machine/services/worker/requirements.txt
CMD ["python", "-m", "useless_machine.services.worker"]
