#!/usr/bin/env python3
import sys
import os
import readline
import subprocess
import json

# --- Configuration ---
CONTAINER_NAME = "openclaw_cyber_mcp"
AGENT_ID = "main"
SESSION_ID = "zeki_session"

# --- Colors (ANSI) ---
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"
GREY = "\033[90m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
RESET = "\033[0m"

BANNER = """
    ███████╗███████╗██╗  ██╗██╗    █████╗ ██╗
    ╚══███╔╝██╔════╝██║ ██╔╝██║   ██╔══██╗██║
      ███╔╝ █████╗  █████╔╝ ██║   ███████║██║
     ███╔╝  ██╔══╝  ██╔═██╗ ██║   ██╔══██╗██║
    ███████╗███████╗██║  ██╗██║   ██║  ██║██║
    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝  ╚═╝╚═╝
        --- Advanced DevSecOps Console ---
                  v1.0 (Powered by Gemini)
"""

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    print(f"{GREEN}{BANNER}{RESET}")
    print(f"{GREY}Escribe 'exit' o 'quit' para salir.{RESET}\n")

def send_message(user_input):
    """
    Executes the OpenClaw agent via docker exec with --json flag
    to capture the full AI response.
    """
    try:
        print(f"{GREY}[+] Procesando con Gemini...{RESET}")

        cmd = [
            "sudo", "docker", "exec", "-i", CONTAINER_NAME,
            "openclaw", "agent",
            "--agent", AGENT_ID,
            "--session-id", SESSION_ID,
            "--message", user_input,
            "--json"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            stderr = result.stderr.strip()
            print(f"\n{RED}[!] Error del agente:\n{stderr}{RESET}\n")
            return

        raw = result.stdout.strip()
        if not raw:
            print(f"\n{RED}[!] El agente no devolvió ninguna respuesta.{RESET}\n")
            return

        # Parse JSON and extract the response text using the correct path
        try:
            data = json.loads(raw)
            # OpenClaw JSON structure: result.payloads[0].text
            payloads = data.get("result", {}).get("payloads", [])
            if payloads and payloads[0].get("text"):
                response_text = payloads[0]["text"]
            else:
                # Fallback: print raw JSON if structure changes
                response_text = raw
            print(f"\n{WHITE}{response_text.strip()}{RESET}\n")
        except json.JSONDecodeError:
            # Not valid JSON — print raw output as-is
            print(f"\n{WHITE}{raw}{RESET}\n")

    except FileNotFoundError:
        print(f"\n{RED}[!] Error: 'docker' no encontrado. Asegúrate de que Docker esté instalado.{RESET}\n")
    except Exception as e:
        print(f"\n{RED}[!] Error inesperado: {str(e)}{RESET}\n")

def main():
    clear_screen()
    print_banner()

    while True:
        try:
            user_input = input(f"{CYAN}ZekiAI > {RESET}").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print(f"\n{YELLOW}Apagando sistemas... ¡Hasta pronto!{RESET}")
                break

            send_message(user_input)

        except KeyboardInterrupt:
            print(f"\n{YELLOW}Apagando sistemas... ¡Hasta pronto!{RESET}")
            break
        except EOFError:
            print(f"\n{YELLOW}Apagando sistemas... ¡Hasta pronto!{RESET}")
            break

if __name__ == "__main__":
    main()
