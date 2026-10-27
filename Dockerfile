# Serve only the public, self-contained PatchProbe UI. No repository tests or private notes
# are copied into the running web container.
FROM python:3.13-alpine
WORKDIR /srv
COPY index.html /srv/index.html
RUN addgroup -S patchprobe && adduser -S patchprobe -G patchprobe
USER patchprobe
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["sh", "-c", "python -m http.server ${PORT:-8080} --bind 0.0.0.0 --directory /srv"]
