# upload-github.ps1
$version = "v1.0.0"
$message = "v1.0.0 - Lançamento inicial da Suíte PolyMath Educacional"

Write-Host "🚀 Enviando para o GitHub..." -ForegroundColor Cyan

# Verificar se Git está instalado
try {
    $gitVersion = git --version
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não encontrado! Instale o Git primeiro." -ForegroundColor Red
    exit 1
}

# Inicializar se necessário
if (!(Test-Path ".git")) {
    Write-Host "📁 Inicializando repositório..." -ForegroundColor Yellow
    git init
}

# Adicionar arquivos
Write-Host "📦 Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "📝 Criando commit..." -ForegroundColor Yellow
git commit -m $message

# Verificar se o remoto existe
$remote = git remote get-url origin 2>$null
if (!$remote) {
    Write-Host "🔗 Adicionando repositório remoto..." -ForegroundColor Yellow
    git remote add origin https://github.com/niopolimathtechnical-00110011/Suite-Educacional-PoliMath.git
}

# Enviar
Write-Host "📤 Enviando para GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

# Tag
Write-Host "🏷️  Criando tag $version..." -ForegroundColor Yellow
git tag -a $version -m $message
git push origin --tags

Write-Host "`n✅ Enviado com sucesso!" -ForegroundColor Green
Write-Host "🔗 https://github.com/niopolimathtechnical-00110011/Suite-Educacional-PoliMath" -ForegroundColor Cyan