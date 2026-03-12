from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database.db import init_db, get_all_leads

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    init_db()
    leads = get_all_leads()
    
    rows = ""
    for lead in leads:
        rows += f"""
        <tr>
            <td>{lead[1]}</td>
            <td>{lead[2]}</td>
            <td>{lead[3]}</td>
            <td><a href="{lead[4]}" target="_blank">{lead[4]}</a></td>
            <td>{lead[5]}</td>
            <td>{lead[6]}</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Lead Generation Dashboard</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 30px; }}
            h1 {{ color: #38bdf8; margin-bottom: 10px; }}
            .stats {{ background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 30px; display: flex; gap: 20px; }}
            .stat-card {{ background: #0f172a; padding: 15px 25px; border-radius: 8px; border: 1px solid #38bdf8; }}
            .stat-card h2 {{ color: #38bdf8; font-size: 32px; }}
            .stat-card p {{ color: #94a3b8; }}
            table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 10px; overflow: hidden; }}
            th {{ background: #38bdf8; color: #0f172a; padding: 12px 15px; text-align: left; }}
            td {{ padding: 12px 15px; border-bottom: 1px solid #334155; font-size: 14px; }}
            tr:hover {{ background: #334155; }}
            a {{ color: #38bdf8; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>🤖 AI Lead Generation Dashboard</h1>
        <br>
        <div class="stats">
            <div class="stat-card">
                <h2>{len(leads)}</h2>
                <p>Total Leads</p>
            </div>
            <div class="stat-card">
                <h2>{len([l for l in leads if l[2] != 'N/A'])}</h2>
                <p>Emails Found</p>
            </div>
            <div class="stat-card">
                <h2>{len(set([l[4] for l in leads]))}</h2>
                <p>Companies</p>
            </div>
        </div>
        
        <table>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Website</th>
                <th>Description</th>
                <th>Date</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html