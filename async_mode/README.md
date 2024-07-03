To download ca-certificate use this command:

```bash
mkdir -p .env/ca-certificates/Yandex && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
    --output-document .env/ca-certificates/Yandex/YandexInternalRootCA.crt && \
chmod 0655 .env/ca-certificates/Yandex/YandexInternalRootCA.crt
```