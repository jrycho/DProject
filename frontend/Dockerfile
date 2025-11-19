# Build
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/.next ./.next
COPY --from=deps /app/public ./public
COPY --from=deps /app/package*.json ./
RUN npm ci --omit=dev
EXPOSE 3000
CMD ["npm","run","start"]