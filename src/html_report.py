import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORT = PROJECT_ROOT / "evaluation" / "reports" / "semantic_report.json"
OUTPUT = PROJECT_ROOT / "evaluation" / "reports" / "evaluation_report.html"

with open(REPORT) as f:
    data = json.load(f)

avg_cov = sum(x["coverage_percent"] for x in data) / len(data)
avg_sim = sum(x["average_similarity"] for x in data) / len(data)

html = f"""
<html>
<head>
<title>AI Test Case Generator Evaluation</title>

<style>

body {{

font-family: Arial;

margin:40px;

}}

table {{

border-collapse: collapse;

width:100%;

}}

th,td {{

border:1px solid #ddd;

padding:10px;

text-align:center;

}}

th {{

background:#007ACC;

color:white;

}}

</style>

</head>

<body>

<h1>AI Test Case Generator Evaluation Report</h1>

<h2>Overall Summary</h2>

<p><b>Total Stories:</b> {len(data)}</p>

<p><b>Average Coverage:</b> {avg_cov:.2f}%</p>

<p><b>Average Similarity:</b> {avg_sim:.3f}</p>

<table>

<tr>

<th>Story</th>

<th>Coverage</th>

<th>Similarity</th>

<th>Manual TC</th>

<th>Generated</th>

<th>Covered</th>

<th>Missing</th>

</tr>
"""

for row in data:

    html += f"""
<tr>

<td>{row['story']}</td>

<td>{row['coverage_percent']}%</td>

<td>{row['average_similarity']}</td>

<td>{row['manual_test_cases']}</td>

<td>{row['generated_scenarios']}</td>

<td>{row['covered']}</td>

<td>{row['missing']}</td>

</tr>
"""

html += """
</table>

</body>

</html>
"""

with open(OUTPUT, "w") as f:
    f.write(html)

print(f"HTML report generated:\n{OUTPUT}")