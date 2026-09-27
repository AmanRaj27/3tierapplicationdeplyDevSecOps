import sys
import json
import os
from google import genai

def remediate_scan(report_file):
    if not os.path.exists(report_file):
        print(f"Report file {report_file} not found.")
        return

    with open(report_file, 'r') as f:
        scan_data = json.load(f)

    # Format security findings into a prompt
    prompt = f"""
    You are a DevSecOps AI Security Engineer.
    Analyze the following security scan report output and generate precise code or Dockerfile fix instructions/patches:
    
    Scan Data:
    {json.dumps(scan_data, indent=2)[:3000]} # Truncated for token safety
    
    Provide a clear breakdown:
    1. Identified Vulnerabilities & Severity
    2. Recommended Code / Dockerfile Fix
    3. Corrected Code Block
    """

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n--- AI AUTO-REMEDIATION SUGGESTION ---")
    print(response.text)
    
    # Save recommendation to a report file
    with open("remediation_report.md", "w") as out:
        out.write(response.text)

if __name__ == "__main__":
    report_path = sys.argv[1] if len(sys.argv) > 1 else "trivy-report.json"
    remediate_scan(report_path)
