FROM openjdk:17.0.2

RUN groupadd spring && useradd spring -g spring
USER spring:spring

ARG DEPENDENCY=target/dependency

COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app

ENTRYPOINT ["java", "-cp", "app:app/lib/*", "gov.nist.e3.web.E3Application"]