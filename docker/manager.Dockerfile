FROM python:3.11-slim
WORKDIR /opt
COPY src/libs /opt/useless_machine/libs
COPY src/services/manager /opt/useless_machine/services/manager
RUN pip install --no-cache-dir -r /opt/useless_machine/services/manager/requirements.txt
CMD ["python", "-m", "useless_machine.services.manager"]
