# Server MCP de Ciberseguridad & vCISO

Este proyecto implementa un servidor basado en el estándar **Model Context Protocol (MCP)**, diseñado para proporcionar a agentes y LLMs tanto herramientas tácticas de ciberseguridad (pentesting) como capacidades estratégicas de gestión de riesgos y comunicación ejecutiva (vCISO).

## Herramientas Incluidas

### 🔴 Capa Táctica — Pentesting

- **`scan_vulnerabilities`**: Ejecuta escaneos de vulnerabilidad y detección de versiones utilizando Nmap.
- **`run_fuzzer`**: Realiza *fuzzing* de directorios o endpoints en servidores web mediante `ffuf` y diccionarios provistos (SecLists).
- **`test_access_control`**: Verifica fallos de autenticación o autorización enviando peticiones HTTP personalizadas a endpoints específicos.
- **`search_exploits`**: Consulta la base de datos de Exploit-DB (`searchsploit`) para encontrar vulnerabilidades conocidas basadas en versiones de software.

### 🟠 Capa vCISO — Gestión de Vulnerabilidades y Riesgos

- **`get_cve_details`**: Consulta la API pública del NVD de NIST para obtener el score CVSS, la severidad y el resumen de un CVE específico.
- **`save_risk_assessment`**: Guarda una matriz de riesgos generada por el LLM en formato JSON ordenado en `/app/reports/risk_assessments/`.

### 🟡 Capa vCISO — Políticas y Capacitación

- **`publish_security_policy`**: Inyecta el contenido redactado por el LLM en una plantilla corporativa (membrete, fecha de emisión, audiencia) y guarda el documento formal en `/app/policies/`.

### 🟢 Capa vCISO — Comunicación Ejecutiva

- **`export_executive_summary`**: Genera una presentación tipo "board deck" con 3 slides (Resumen Ejecutivo, Impacto Financiero, Plan de Acción) lista para juntas directivas. Se guarda en `/app/reports/executive/`.

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
   git clone https://github.com/angelmontero0107/ZekiAI.git
   cd ZekiAI
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
