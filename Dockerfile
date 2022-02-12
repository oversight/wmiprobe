FROM python:3.8
ENV OS_CONFIG_FOLDER /data/config/OsWmiProbe/
ADD . /code
WORKDIR /code

# GitHub Personal Access Token
# Use: docker build --build-arg PAT={your_token} .
ARG PAT
RUN git clone https://${PAT}@github.com/cesbit/aiowmi.git && \
    cd aiowmi && \
    pip install --no-cache-dir -r requirements.txt && \
    python setup.py install
CMD ["python", "oswmi.py"]
