[![CI](https://github.com/oversight/wmiprobe/workflows/CI/badge.svg)](https://github.com/oversight/wmiprobe/actions)
[![Release Version](https://img.shields.io/github/release/oversight/wmiprobe)](https://github.com/oversight/wmiprobe/releases)

# Oversight WMI Probe

## Docker build

```
docker build -t wmiprobe . --no-cache
```

## Issues

### Access denied on SELECT * FROM Win32_Service

Run the following command in an administrative prompt:

```
sc sdset SCMANAGER D:(A;;CCLCRPRC;;;AU)(A;;CCLCRPWPRC;;;SY)(A;;KA;;;BA)S:(AU;FA;KA;;;WD)(AU;OIIOFA;GA;;;WD)
```

### Error 0x80041010

To fix error 0x80041010 (Performance Counter Class missing) the following command can be used:

```
%windir%\system32\wbem\wmiadap.exe /f
```


## WMI info

- https://docs.microsoft.com/en-us/openspecs/windows_protocols/

