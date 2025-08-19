# Stage 1 – Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN npm i -g pnpm && pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build

# Stage 2 – Serve
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
