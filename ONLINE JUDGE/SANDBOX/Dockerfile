FROM python:3.11-slim
WORKDIR /app
COPY runner.py .
# Run as a non-root user for security hardening
RUN useradd -m judgeuser
USER judgeuser
CMD ["python", "runner.py"]
