# Этап сборки (build stage)
FROM node:16-alpine AS builder

WORKDIR /app

# Копируем package.json и package-lock.json для кэширования
COPY package*.json ./

# Устанавливаем зависимости (включая devDependencies)
RUN npm install

# Копируем все файлы проекта
COPY . .

# Собираем приложение
RUN npm run build

# Этап запуска (production stage)
FROM nginx:alpine

# Копируем собранные файлы из builder в nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Копируем конфиг nginx (если нужны кастомные настройки)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80 (стандартный для nginx)
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]