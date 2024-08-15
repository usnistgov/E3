FROM eclipse-temurin:21.0.2_13-jre

RUN mkdir -p /app/plugins

RUN groupadd spring && useradd spring -g spring
USER spring:spring

ARG DEPENDENCY=target/dependency
ARG PLUGINS=plugins

COPY ${PLUGINS} /app/plugins

COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app

ENTRYPOINT ["java", "-cp", "app:app/lib/*", "gov.nist.eee.web.E3Application"]