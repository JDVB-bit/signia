# 🏗️ Etapa 1: compila la SPA con la misma versión de pnpm que fija package.json
FROM node:24-alpine AS compilacion
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# 🚀 Etapa 2: sirve solo los estáticos compilados con nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=compilacion /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
