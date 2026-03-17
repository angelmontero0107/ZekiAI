#!/bin/bash
set -e

CONFIG_DIR="/root/.openclaw"
CONFIG_FILE="$CONFIG_DIR/openclaw.json"
SELECTED_MODEL="${GEMINI_MODEL:-google/gemini-2.5-flash}"

echo "[+] Iniciando Zero-Touch Provisioning de ZekiAI..."
mkdir -p "$CONFIG_DIR"

# 1. Exportar la API Key al entorno del proceso
if [ -n "$GEMINI_API_KEY" ]; then
    export GOOGLE_API_KEY="$GEMINI_API_KEY"
fi

# 2. Generar el Golden Config JSON dinámicamente
echo "[+] Generando openclaw.json con la arquitectura 2026.3.13..."
cat <<EOF > "$CONFIG_FILE"
{
  "auth": {
    "profiles": {
      "google:default": {
        "provider": "google",
        "mode": "api_key"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "$SELECTED_MODEL"
      },
      "models": {
        "\$SELECTED_MODEL": {}
      },
      "compaction": {
        "mode": "safeguard"
      },
      "maxConcurrent": 4
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true
  },
  "gateway": {
    "mode": "local"
  }
}
EOF

# 3. Inyectar llave en el keystore seguro (por si acaso)
if [ -n "$GEMINI_API_KEY" ]; then
    echo "[+] Registrando API Key en el keystore..."
    openclaw auth add google --key "$GEMINI_API_KEY" || true
fi

# 4. Sincronizar Arsenal Cyber-Ops
if [ -f "/app/cyber_mcp/SKILL.md" ]; then
    echo "[+] Montando AgentSkill: cyber-ops..."
    openclaw skill register /app/cyber_mcp/SKILL.md --name "cyber-ops" || true
fi

# 5. Despliegue
echo "[+] ZekiAI Engine listo. Levantando Gateway en puerto 18789..."
exec openclaw gateway --allow-unconfigured