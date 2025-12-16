FROM node:20-alpine

WORKDIR /app

# Copiar archivos de package
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de archivos
COPY . .

# Exponer puerto
EXPOSE 5173

# Comando para desarrollo
CMD ["npm", "run", "dev"]
