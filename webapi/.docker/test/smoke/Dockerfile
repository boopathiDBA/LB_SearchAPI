FROM node:16-alpine

# Install bruno cli tool to run API test, Pin version to be deterministic, should upgrade if possible
RUN npm install -g @usebruno/cli@^1

COPY tests/smoke /app/tests/smoke

WORKDIR /app/tests/smoke/Webapi
