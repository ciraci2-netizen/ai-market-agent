# Interactive script to create a .env file for this project
# Usage: Run in PowerShell in the project folder: .\create_env.ps1

Write-Host "This will create a .env file in the current directory."

$openai = Read-Host -Prompt "OPENAI_API_KEY (paste your key)"
$tavily = Read-Host -Prompt "TAVILY_API_KEY (optional, press Enter to skip)"
$pine_api = Read-Host -Prompt "PINECONE_API_KEY (optional, press Enter to skip)"
$pine_index = Read-Host -Prompt "PINECONE_INDEX (optional, press Enter to skip)"

$envContent = @"
OPENAI_API_KEY=$openai
TAVILY_API_KEY=$tavily
PINECONE_API_KEY=$pine_api
PINECONE_INDEX=$pine_index
"@

$envPath = Join-Path -Path (Get-Location) -ChildPath ".env"
if (Test-Path $envPath) {
    $confirm = Read-Host -Prompt ".env already exists. Overwrite? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "Aborted. .env not changed."
        exit 0
    }
}

$envContent | Out-File -FilePath $envPath -Encoding UTF8
Write-Host ".env created at $envPath"
Write-Host "Remember: do NOT paste secrets in public chats."
