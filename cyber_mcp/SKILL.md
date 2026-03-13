---
name: Cybersecurity Pentesting
description: A comprehensive suite of cybersecurity tools for reconnaissance, vulnerability scanning, fuzzing, access control, and exploitation parsing.
command: uv run /home/luiscastillo/ZekiAI/cyber_mcp/cyber_mcp.py
---

# Cybersecurity Pentesting Skill

This skill provides an MCP server equipped with active and passive tools designed to perform professional penetration testing and security reconnaissance tasks.

## Available Tools

1. `scan_vulnerabilities`: Executes an Nmap target scan using the `vuln` script category and version detection to find common vulnerabilities.
2. `run_fuzzer`: Runs `ffuf` to brute-force directories or endpoints on a web server using a specified wordlist.
3. `test_access_control`: Sends custom HTTP requests to verify if specific endpoints lack proper authentication or authorization checks.
4. `search_exploits`: Queries Exploit-DB's `searchsploit` for known vulnerabilities related to a specific software version.

## Instructions for the Agent
- **DO NOT hallucinate or invent data.** Always rely strictly on the output provided by these tools.
- When using `run_fuzzer`, you MUST place the exact string `FUZZ` in the `target_url` where you want the brute-forcing to occur (e.g., `http://example.com/FUZZ`). Use the correct path to the downloaded wordlist container (e.g., `/opt/seclists/Discovery/Web-Content/common.txt`).
- When using `test_access_control`, carefully construct the `headers` and `data` objects.
- All subprocess tools have timeouts. If a timeout error is returned, adjust your scan parameters or inform the user.
