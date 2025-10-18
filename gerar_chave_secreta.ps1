# Script PowerShell para gerar chave secreta segura
# Execute: .\gerar_chave_secreta.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "GERADOR DE CHAVES SECRETAS SEGURAS" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detectado: $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "ERRO: Python nao encontrado!" -ForegroundColor Red
    Write-Host "Instale Python em: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Gerar chave usando Python
Write-Host "Gerando chave secreta..." -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ""

$chave = python -c "import secrets; print(secrets.token_urlsafe(32))"

if ($LASTEXITCODE -eq 0) {
    Write-Host "CHAVE SECRETA GERADA COM SUCESSO:" -ForegroundColor Green
    Write-Host ""
    Write-Host $chave -ForegroundColor Yellow
    Write-Host ""
    Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host ""
    
    # Copiar para clipboard se possível
    try {
        Set-Clipboard -Value $chave
        Write-Host "[OK] Chave copiada para a area de transferencia!" -ForegroundColor Green
    } catch {
        Write-Host "[INFO] Nao foi possivel copiar automaticamente." -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "INSTRUCOES:" -ForegroundColor Cyan
    Write-Host "1. A chave foi copiada para sua area de transferencia" -ForegroundColor White
    Write-Host "2. Cole no Render: Environment -> CHAVE_SECRETA" -ForegroundColor White
    Write-Host "3. Ou cole no arquivo .env: CHAVE_SECRETA=$chave" -ForegroundColor White
    Write-Host ""
    Write-Host "AVISO DE SEGURANCA:" -ForegroundColor Red
    Write-Host "- NUNCA commite esta chave no Git!" -ForegroundColor Yellow
    Write-Host "- Use chaves diferentes para cada ambiente" -ForegroundColor Yellow
    Write-Host "- Guarde em local seguro (gerenciador de senhas)" -ForegroundColor Yellow
    Write-Host ""
    
} else {
    Write-Host "ERRO ao gerar chave!" -ForegroundColor Red
    Write-Host "Execute manualmente: python -c `"import secrets; print(secrets.token_urlsafe(32))`"" -ForegroundColor Yellow
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Pausar para o usuário ler
Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


