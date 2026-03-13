import subprocess
import requests
import json
import os
import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("CyberSecurityMCP")

@mcp.tool()
def scan_vulnerabilities(target: str) -> str:
    """
    Vulnerability Testing: Run an nmap scan with version detection and vuln scripts against a target.
    """
    try:
        # Ejecutando nmap con timeout de 300s
        result = subprocess.run(
            ['nmap', '-sV', '--script=vuln', target],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0 and not result.stdout:
            return f"Error executing nmap scan:\n{result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: nmap scan timed out after 300 seconds."
    except Exception as e:
        return f"Exception occurred during scan: {str(e)}"

@mcp.tool()
def run_fuzzer(target_url: str, wordlist_path: str) -> str:
    """
    Fuzz Testing: Use ffuf to fuzz a target URL relying on a specified wordlist.
    """
    if "FUZZ" not in target_url:
        return "Error: target_url must contain the 'FUZZ' keyword."
    try:
        # Ejecutando ffuf con timeout de 120s
        result = subprocess.run(
            ['ffuf', '-u', target_url, '-w', wordlist_path],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout
        
        # Limitar la salida para no agotar el contexto del LLM
        if len(output) > 4000:
            output = output[:4000] + "\n...[OUTPUT TRUNCATED]..."
        
        if result.returncode != 0 and not output:
            return f"Error executing ffuf:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: ffuf scan timed out after 120 seconds."
    except Exception as e:
        return f"Exception occurred during fuzzing: {str(e)}"

@mcp.tool()
def test_access_control(url: str, method: str, headers: dict, data: dict) -> str:
    """
    Access Control Testing: Check endpoints for authorization flaws using custom HTTP requests.
    """
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Uso estricto de la librería requests como fue solicitado, sin CLI
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=data if data else None,
            timeout=15,
            verify=False
        )
        return f"Status Code: {response.status_code}\nHeaders: {dict(response.headers)}\nBody Snippet: {response.text[:1000]}"
    except requests.Timeout:
        return f"Error: Request to {url} timed out."
    except Exception as e:
        return f"Exception occurred during access control test: {str(e)}"

@mcp.tool()
def search_exploits(software_version: str) -> str:
    """
    Search for known vulnerabilities and exploits using Exploit-DB's searchsploit.
    """
    try:
        # Ejecutando searchsploit con timeout de 60s
        result = subprocess.run(
            ['searchsploit', software_version],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout
        
        # Limitar la salida
        if len(output) > 4000:
            output = output[:4000] + "\n...[OUTPUT TRUNCATED]..."
            
        if result.returncode != 0 and not output:
             return f"Error executing searchsploit:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: searchsploit timed out after 60 seconds."
    except Exception as e:
        return f"Exception occurred during exploit search: {str(e)}"

@mcp.tool()
def get_cve_details(cve_id: str) -> str:
    """
    Gestión de Vulnerabilidades (vCISO): Consulta la API del NVD de NIST para obtener el score CVSS, la severidad y el resumen de un CVE.
    """
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("vulnerabilities"):
            return f"CVE {cve_id} no encontrado o sin detalles disponibles en NVD."
            
        cve_data = data["vulnerabilities"][0]["cve"]
        
        summary = "Sin descripción disponible."
        for desc in cve_data.get("descriptions", []):
            if desc.get("lang") == "en":
                summary = desc.get("value")
                break
                
        metrics = cve_data.get("metrics", {})
        cvss_score = "N/A"
        severity = "N/A"
        
        if "cvssMetricV31" in metrics:
            metric = metrics["cvssMetricV31"][0]["cvssData"]
            cvss_score = metric.get("baseScore", "N/A")
            severity = metric.get("baseSeverity", "N/A")
        elif "cvssMetricV30" in metrics:
            metric = metrics["cvssMetricV30"][0]["cvssData"]
            cvss_score = metric.get("baseScore", "N/A")
            severity = metric.get("baseSeverity", "N/A")
        elif "cvssMetricV2" in metrics:
            cvss_score = metrics["cvssMetricV2"][0]["cvssData"].get("baseScore", "N/A")
            severity = metrics["cvssMetricV2"][0].get("baseSeverity", "N/A")
            
        return f"CVE: {cve_id}\nCVSS Score: {cvss_score}\nSeverity: {severity}\nSummary: {summary}"
    except requests.Timeout:
        return f"Error: La solicitud a la API de NVD superó el tiempo de espera para {cve_id}."
    except requests.RequestException as e:
        return f"Error en la petición a la API: {str(e)}"
    except Exception as e:
        return f"Ocurrió un error al procesar el CVE: {str(e)}"

@mcp.tool()
def save_risk_assessment(project_name: str, risk_matrix_json: str) -> str:
    """
    Gestión de Riesgos (vCISO): Guarda la matriz de riesgos en formato JSON en /app/reports/risk_assessments/.
    """
    try:
        reports_dir = "/app/reports/risk_assessments/"
        try:
            os.makedirs(reports_dir, exist_ok=True)
        except PermissionError:
            # Fallback a directorio local si no hay permisos en /app
            reports_dir = "./app/reports/risk_assessments/"
            os.makedirs(reports_dir, exist_ok=True)
            
        safe_project_name = "".join([c for c in project_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        safe_project_name = safe_project_name.replace(' ', '_')
        
        file_path = os.path.join(reports_dir, f"{safe_project_name}_risk_assessment.json")
        
        parsed_json = json.loads(risk_matrix_json)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=4, ensure_ascii=False)
            
        return f"Matriz de riesgos guardada con éxito en {file_path}"
    except json.JSONDecodeError:
        return "Error: El parámetro risk_matrix_json no es un JSON válido."
    except Exception as e:
        return f"Ocurrió un error al guardar la evaluación de riesgos: {str(e)}"

@mcp.tool()
def publish_security_policy(title: str, target_audience: str, markdown_content: str) -> str:
    """
    Creación de Políticas (vCISO): Genera un documento formal de política de seguridad inyectando el contenido en una plantilla corporativa.
    """
    try:
        policies_dir = "/app/policies/"
        try:
            os.makedirs(policies_dir, exist_ok=True)
        except PermissionError:
            policies_dir = "./app/policies/"
            os.makedirs(policies_dir, exist_ok=True)
            
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        template = f"""# DOCUMENTO CONFIDENCIAL - POLÍTICA DE SEGURIDAD
**Título:** {title}
**Fecha de Emisión:** {current_date}
**Audiencia:** {target_audience}

---

{markdown_content}

---
*Este documento ha sido autogenerado y revisado por el equipo vCISO.*
"""
        
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        safe_title = safe_title.replace(' ', '_').lower()
        
        filename = f"{current_date}_{safe_title}.md"
        file_path = os.path.join(policies_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
            
        return f"Política de seguridad publicada exitosamente en: {os.path.abspath(file_path)}"
        
    except Exception as e:
        return f"Error al publicar la política de seguridad: {str(e)}"

@mcp.tool()
def export_executive_summary(client_name: str, critical_risks_count: int, estimated_financial_impact: str, executive_summary_text: str) -> str:
    """
    Comunicación Ejecutiva (vCISO): Genera una presentación para la junta directiva resumiendo el impacto financiero y los hallazgos críticos.
    """
    try:
        report_dir = "/app/reports/executive/"
        try:
            os.makedirs(report_dir, exist_ok=True)
        except PermissionError:
            # Fallback a directorio local si no hay permisos en /app
            report_dir = "./app/reports/executive/"
            os.makedirs(report_dir, exist_ok=True)
            
        safe_client_name = "".join([c for c in client_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        safe_client_name = safe_client_name.replace(' ', '_').lower()
        
        filename = f"{safe_client_name}_board_presentation.md"
        file_path = os.path.join(report_dir, filename)
        
        markdown_content = f"""# Presentación Ejecutiva de Ciberseguridad: {client_name}

## Slide 1: Resumen Ejecutivo
{executive_summary_text}

---

## Slide 2: Impacto Financiero y Riesgos
- **Riesgos Críticos Identificados:** {critical_risks_count}
- **Impacto Financiero Estimado:** {estimated_financial_impact}

---

## Slide 3: Plan de Acción Propuesto
1. Contención inmediata de los {critical_risks_count} riesgos críticos.
2. Despliegue de controles compensatorios para reducir la exposición financiera ({estimated_financial_impact}).
3. Revisión estratégica y aprobación del presupuesto de remediación por la junta directiva.
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        preview = markdown_content[:200].replace('\\n', ' ')
        if len(markdown_content) > 200:
            preview += "..."
            
        return f"Presentación ejecutiva creada exitosamente en: {os.path.abspath(file_path)}\n\nVista previa:\n{preview}"
        
    except Exception as e:
        return f"Error al generar la presentación ejecutiva: {str(e)}"

if __name__ == "__main__":
    mcp.run()
