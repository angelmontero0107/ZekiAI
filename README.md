# Server MCP de Ciberseguridad

Este proyecto implementa un servidor basado en el estándar **Model Context Protocol (MCP)**, diseñado específicamente para proporcionar herramientas de ciberseguridad a agentes y LLMs. El servidor opera bajo el principio de menor privilegio, ofreciendo exclusivamente herramientas de solo lectura y cero permisos de escritura para garantizar un entorno seguro.

## Herramientas Incluidas

El servidor expone las siguientes capacidades (tools):

- **`analyze_ip`**: Permite analizar direcciones IP en busca de reputación maliciosa, geolocalización o datos de inteligencia de amenazas.
- **`lookup_cve`**: Permite la consulta de vulnerabilidades conocidas (CVE) para obtener detalles, severidad (CVSS) y recomendaciones.

## Arquitectura y Tecnologías

- **Lenguaje**: Python 3.10+
- **Estándar**: Model Context Protocol (MCP)
- **Despliegue**: Docker y Docker Compose
- **Integración Compatible**: OpenClaw, Antigravity u otros clientes MCP.

## Requisitos Previos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) instalados.
- Archivo `.env` configurado con las claves API necesarias (ej. VirusTotal, NVD, etc., según aplique). **Nota: Por razones de seguridad, el archivo `.env` nunca debe subirse al control de versiones.**

## Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/nombre-de-tu-repositorio.git
   cd nombre-de-tu-repositorio
   ```

2. **Configurar Variables de Entorno:**
   Crea un archivo `.env` en la raíz del proyecto basándote en un archivo de plantilla (si existe) y añade las claves de las APIs necesarias.
   ```bash
   touch .env
   # Añadir tus claves y configuraciones en el archivo .env
   ```

3. **Ejecutar el Servidor con Docker Compose:**
   Levanta la infraestructura local utilizando Docker:
   ```bash
   docker-compose up -d --build
   ```
   El contenedor `openclaw_cyber_mcp` se levantará e iniciará el gateway en el puerto `18789` (o el configurado).

## Integración (SKILL.md)

Este proyecto incluye un archivo `SKILL.md` con las instrucciones necesarias para que sistemas como OpenClaw u otras plataformas de IA reconozcan e integren este servidor como una habilidad de ciberseguridad. Revisa el archivo para conocer la configuración en formato JSON para clientes MCP.

## Seguridad

- **Solo lectura (Read-Only)**: Todas las herramientas son pasivas, evitando que el servidor modifique archivos o el estado del sistema.
- **Principio de Menor Privilegio**: El contenedor donde se ejecuta está limitado para no comprometer el host subyacente.

## Licencia

Este proyecto es privado/público según se defina en las configuraciones del repositorio.
