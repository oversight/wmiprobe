# Oversight WMI Probe

## Local requirements

Package `aiowmi` is required.

Activate your Python environment (e.g. conda activate wmiprobe) and then install `aiowmi`

```bash
git clone git@github.com:cesbit/aiowmi.git
cd aiowmi
python setup.py install
```

## Docker build

A Personal Access Token is required to build this Docker image.
*(Go to GitHub > Settings > Personal access tokens and generate a personal access token with repo scope enabled)*

```
docker build -t cesbit/oswmiprobe:v0.1.0 -t cesbit/oswmiprobe:latest . --no-cache --build-arg PAT={your_token}
```

## Issues

### Access denied on SELECT * FROM Win32_Service

Run the following command in an administrative prompt:

```
sc sdset SCMANAGER D:(A;;CCLCRPRC;;;AU)(A;;CCLCRPWPRC;;;SY)(A;;KA;;;BA)S:(AU;FA;KA;;;WD)(AU;OIIOFA;GA;;;WD)
```
