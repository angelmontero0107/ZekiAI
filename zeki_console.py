#!/usr/bin/env python3
import subprocess
import sys
import os
import readline

# --- Configuration & Aesthetics ---
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"
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
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Prints the ZekiAI banner with hacker green color."""
    print(f"{GREEN}{BANNER}{RESET}")
    print(f"\033[90mEscribe 'exit' o 'quit' para salir.\033[0m\n")

def run_agent_command(user_input):
    """
    Executes the OpenClaw agent in headless mode and captures the output.
    """
    try:
        print("\033[90m[+] Procesando con Gemini...\033[0m")
        
        # Construct the command (Running inside Docker with agent and session)
        cmd = ["sudo", "docker", "exec", "-i", "openclaw_cyber_mcp", "openclaw", "agent", "--agent", "main", "--session-id", "zeki_session", "--message", user_input]
        
        # Execute and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            if result.stdout:
                # White color for output as per snippet
                print(f"\n\033[97m{result.stdout.strip()}\033[0m\n")
        else:
            # Red color for error as per snippet
            print(f"\n\033[91m[!] Error del agente:\n{result.stderr.strip()}\033[0m\n")
                
    except FileNotFoundError:
        print(f"\033[91m[!] Error: 'openclaw' command not found.\033[0m\n")
    except Exception as e:
        print(f"\033[91m[!] Unexpected error: {str(e)}\033[0m\n")

def main():
    clear_screen()
    print_banner()
    
    while True:
        try:
            # Get user input with Cyan prompt
            prompt = f"{CYAN}ZekiAI > {RESET}"
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("\n\033[93mApagando sistemas... ¡Hasta pronto!\033[0m")
                break
            
            run_agent_command(user_input)
            
        except KeyboardInterrupt:
            print("\n\033[93mApagando sistemas... ¡Hasta pronto!\033[0m")
            break
        except EOFError:
            print("\n\033[93mApagando sistemas... ¡Hasta pronto!\033[0m")
            break

if __name__ == "__main__":
    main()
