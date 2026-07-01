Write-Host "Running Bandit Security Scan..."
cd ..\..\backend
.venv\Scripts\bandit.exe -r app\

Write-Host "Running NPM Audit..."
cd ..\frontend
npm audit

Write-Host "Running Pip Audit..."
cd ..\backend
.venv\Scripts\pip.exe install pip-audit
.venv\Scripts\pip-audit.exe

Write-Host "✅ Security Scan Complete."
