# prometheus/Dockerfile
FROM prom/prometheus:latest

COPY prometheus.yml prometheus/prometheus.yml

EXPOSE 9090

CMD ["--config.file=prometheus/prometheus.yml"]