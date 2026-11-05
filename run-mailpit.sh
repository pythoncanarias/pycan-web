docker run -d \
  --name mailpit \
  -p 1025:1025 \
  -p 8025:8025 \
  -v $(pwd)/mailpit-data:/data \
  axllent/mailpit
