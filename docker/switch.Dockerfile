FROM python:3.11-slim
WORKDIR /opt
COPY src/libs /opt/useless_machine/libs
COPY src/services/switch /opt/useless_machine/services/switch
RUN pip install --no-cache-dir -r /opt/useless_machine/services/switch/requirements.txt
EXPOSE 80
ENV ROOT_PATH=/
CMD ["/bin/bash", "-c", "uvicorn useless_machine.services.switch.app:app --host 0.0.0.0 --port 80 --root-path ${ROOT_PATH}"]
