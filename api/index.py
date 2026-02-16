import subprocess
import os
import sys

# Vercel provides PORT env var
port = os.environ.get("PORT", "3000")

# Launch Streamlit on that port
cmd = [
    "streamlit", "run", "../app.py",  # adjust if your file is main.py etc.
    f"--server.port={port}",
    "--server.headless=true",
    "--server.enableCORS=false",
    "--server.enableXsrfProtection=false"
]

# Run it (this is blocking, which Vercel likes for serverless-ish)
subprocess.run(cmd, check=True)
