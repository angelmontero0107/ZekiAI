---
name: Cybersecurity Pentesting & vCISO
description: A comprehensive suite of cybersecurity tools covering tactical pentesting (reconnaissance, vulnerability scanning, fuzzing, access control, exploitation) and vCISO strategic management (CVE intelligence, risk assessments, security policies, and executive reporting).
command: uv run /app/cyber_mcp/cyber_mcp.py
---

# Cybersecurity Pentesting & vCISO Skill

This skill provides an MCP server equipped with active, passive, and strategic tools designed to perform professional penetration testing, security reconnaissance, and virtual CISO (vCISO) management tasks.

## Available Tools

### 🔴 Tactical Layer — Pentesting

1. `scan_vulnerabilities(target)`: Executes an Nmap target scan using the `vuln` script category and version detection to find common vulnerabilities.
2. `run_fuzzer(target_url, wordlist_path)`: Runs `ffuf` to brute-force directories or endpoints on a web server using a specified wordlist.
3. `test_access_control(url, method, headers, data)`: Sends custom HTTP requests to verify if specific endpoints lack proper authentication or authorization checks.
4. `search_exploits(software_version)`: Queries Exploit-DB's `searchsploit` for known vulnerabilities related to a specific software version.

### 🟠 vCISO Layer — Vulnerability & Risk Management

5. `get_cve_details(cve_id)`: Queries the NVD NIST public API to retrieve the CVSS score, severity, and English summary for a given CVE ID.
6. `save_risk_assessment(project_name, risk_matrix_json)`: Saves an LLM-generated risk matrix in JSON format to `/app/reports/risk_assessments/`.

### 🟡 vCISO Layer — Policy & Training

7. `publish_security_policy(title, target_audience, markdown_content)`: Injects LLM-generated content into a formal corporate policy template (with confidentiality header, issuance date, and audience) and saves it to `/app/policies/`.

### 🟢 vCISO Layer — Executive Communication

8. `export_executive_summary(client_name, critical_risks_count, estimated_financial_impact, executive_summary_text)`: Generates a board-ready presentation with 3 structured slides (Executive Summary, Financial Impact, Action Plan) and saves it to `/app/reports/executive/`.

## Instructions for the Agent

- **DO NOT hallucinate or invent data.** Always rely strictly on the output provided by these tools.
- When using `run_fuzzer`, you MUST place the exact string `FUZZ` in the `target_url` where you want the brute-forcing to occur (e.g., `http://example.com/FUZZ`). Use the correct path to the downloaded wordlist inside the container (e.g., `/opt/seclists/Discovery/Web-Content/common.txt`).
- When using `test_access_control`, carefully construct the `headers` and `data` objects.
- All subprocess tools have timeouts. If a timeout error is returned, adjust your scan parameters or inform the user.
- When using `get_cve_details`, always pass the full CVE ID format, e.g., `CVE-2021-44228`.
- When using `save_risk_assessment`, the `risk_matrix_json` parameter must be a valid JSON string.
- When using `publish_security_policy`, write the full policy content in Markdown format using `markdown_content`.
- The `export_executive_summary` tool returns the absolute file path and a 200-character preview for immediate confirmation.
