# Apache Jena Fuseki with both ontology versions baked in (read-only).
# Render builds it from the repo root (Dockerfile path deploy/Dockerfile); locally: podman build -f deploy/Dockerfile -t peruvian-food-fuseki .
FROM docker.io/library/eclipse-temurin:21-jre

ARG JENA_VERSION=5.2.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -fsSL https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-${JENA_VERSION}.tar.gz \
       | tar -xz -C /opt \
    && mv /opt/apache-jena-fuseki-${JENA_VERSION} /opt/fuseki \
    && apt-get purge -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY ontology/peruvian_food_base.ttl ontology/peruvian_food_refined.ttl /data/
COPY deploy/config.ttl /opt/fuseki/config.ttl
# FUSEKI_BASE is /opt/fuseki/run; this replaces the default localhost-only admin rule
COPY deploy/shiro.ini /opt/fuseki/run/shiro.ini

WORKDIR /opt/fuseki
ENV JVM_ARGS="-Xmx384m"
# Render sets PORT; 8080 locally
CMD ["sh", "-c", "exec ./fuseki-server --port=${PORT:-8080} --config=/opt/fuseki/config.ttl"]
