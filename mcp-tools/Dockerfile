FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*
# oc CLI
RUN curl -sL https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz  | tar -xz -C /usr/local/bin oc && chmod +x /usr/local/bin/oc
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py /app/server.py
ENV PYTHONUNBUFFERED=1
CMD ["python", "/app/server.py"]
