# Build
FROM node:20-alpine AS deps
WORKDIR /app
ARG NEXT_PUBLIC_API_URL=/api
ARG NEXT_PUBLIC_API_BASE=/api
ARG NEXT_PUBLIC_OFF_API_BASE_URL=https://world.openfoodfacts.org
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_BASE=$NEXT_PUBLIC_API_BASE
ENV NEXT_PUBLIC_OFF_API_BASE_URL=$NEXT_PUBLIC_OFF_API_BASE_URL
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
