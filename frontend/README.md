# Sistema de Documentos Contables - Frontend

Frontend desarrollado con React + Vite + Tailwind CSS.

## Requisitos

- Node.js 18+
- npm o yarn

## Instalación

```bash
npm install
```

## Configuración

Copia el archivo `.env.example` a `.env` y ajusta las variables según tu entorno:

```bash
cp .env.example .env
```

## Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## Construcción

```bash
npm run build
```

## Docker

El proyecto incluye configuración Docker. Para ejecutar:

```bash
docker build -t frontend .
docker run -p 80:80 frontend
```

O usando docker-compose desde la raíz del proyecto:

```bash
docker-compose up
```

## Estructura del Proyecto

```
src/
├── components/     # Componentes reutilizables
├── pages/          # Páginas de la aplicación
├── services/       # Servicios de API
├── App.jsx         # Componente principal
└── main.jsx        # Punto de entrada
```

## Características

- CRUD completo de documentos
- Visualización de empresas
- Dashboard con estadísticas
- Paginación de datos
- Diseño responsivo con Tailwind CSS
- Modales para crear y editar
