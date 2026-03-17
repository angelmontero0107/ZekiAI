# Dockerfile for custom OpenClaw with Python and uv

# Using the official OpenClaw image as base
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Install Python, venv, curl, and Pentesting Tools (nmap, whois, dnsutils, etc)
# We support both apt (Debian/Ubuntu) and apk (Alpine) just in case the base image uses either.
RUN if command -v apt-get >/dev/null; then \
    apt-get update && apt-get install -y python3 python3-venv curl nmap dnsutils whois ffuf sqlmap wget git && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null; then \
    apk add --no-cache python3 curl nmap bind-tools whois ffuf sqlmap wget git; \
    else \
    echo "Package manager not found"; exit 1; \
    fi

# Install exploitdb
RUN git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb && \
    ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit && \
    cp -n /opt/exploitdb/.searchsploit_rc ~/ || true

# Install seclists
RUN git clone --depth 1 https://github.com/danielmiessler/SecLists.git /opt/seclists

# Create output directories for vCISO reports and policies
RUN mkdir -p /app/reports/risk_assessments /app/reports/executive /app/policies

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to the PATH globally
ENV PATH="/root/.local/bin:$PATH"

# Depending on the original base image, you may need to switch back to the original non-root user.
# e.g., USER node or USER openclaw. Kept as root for now to ensure uv works globally unless overridden.

RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages -r /tmp/requirements.txt

# Copy entrypoint script and set permissions
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
