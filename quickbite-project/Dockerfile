# Nhiem vu 1: runtime Java 17 JRE Alpine, copy file JAR da build voi Gradle
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY build/libs/app.jar ./app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
