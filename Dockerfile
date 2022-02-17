FROM python:3.8
ENV OS_CONFIG_FOLDER /data/config/OsWmiProbe/
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "oswmi.py"]
