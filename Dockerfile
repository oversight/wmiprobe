FROM transceptortechnology/oswmicprobe:latest
ENV OS_CONFIG_FOLDER /data/config/OsWmicProbe/
WORKDIR /code
CMD ["python", "wmicProbe.py"]
