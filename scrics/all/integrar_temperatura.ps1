# Script para integrar ollama_temperatura_dinamico.py en multi-tools
# Ejecutar desde: C:\Users\joseantonio.legidoma\copilot\apis\

Write-Host "Integrando ollama_temperatura_dinamico.py en sistema multi-tools..." -ForegroundColor Cyan

# Paso 1: Renombrar
if (Test-Path "ollama_temperatura_dinamico.py") {
    Write-Host "[1/3] Renombrando archivo..." -ForegroundColor Yellow
    Rename-Item "ollama_temperatura_dinamico.py" "ollama_temperatura.py" -Force
    Write-Host "      ✓ Renombrado a ollama_temperatura.py" -ForegroundColor Green
} else {
    Write-Host "[1/3] Archivo ollama_temperatura_dinamico.py no encontrado!" -ForegroundColor Red
    exit 1
}

# Paso 2: Mover a tools/
if (Test-Path "ollama_temperatura.py") {
    Write-Host "[2/3] Moviendo a carpeta tools/..." -ForegroundColor Yellow
    
    # Crear carpeta tools si no existe
    if (-not (Test-Path "tools")) {
        New-Item -ItemType Directory -Path "tools" | Out-Null
        Write-Host "      ✓ Carpeta tools/ creada" -ForegroundColor Green
    }
    
    # Mover archivo
    Move-Item "ollama_temperatura.py" "tools\" -Force
    Write-Host "      ✓ Movido a tools/ollama_temperatura.py" -ForegroundColor Green
} else {
    Write-Host "[2/3] Error: archivo no renombrado correctamente" -ForegroundColor Red
    exit 1
}

# Paso 3: Verificar
Write-Host "[3/3] Verificando integración..." -ForegroundColor Yellow

if (Test-Path "tools\ollama_temperatura.py") {
    Write-Host "      ✓ Archivo en posición correcta" -ForegroundColor Green
    
    # Verificar que tiene KEYWORDS y TOOL_DEFINITION
    $content = Get-Content "tools\ollama_temperatura.py" -Raw
    
    if ($content -match "TOOL_DEFINITION\s*=") {
        Write-Host "      ✓ TOOL_DEFINITION encontrado" -ForegroundColor Green
    } else {
        Write-Host "      ✗ TOOL_DEFINITION NO encontrado" -ForegroundColor Red
    }
    
    if ($content -match "KEYWORDS\s*=") {
        Write-Host "      ✓ KEYWORDS encontrado" -ForegroundColor Green
    } else {
        Write-Host "      ✗ KEYWORDS NO encontrado" -ForegroundColor Red
    }
} else {
    Write-Host "      ✗ Error al mover archivo" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "✅ INTEGRACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora puedes ejecutar:" -ForegroundColor White
Write-Host "  python ollama_multi_tools.py --test" -ForegroundColor Yellow
Write-Host "  python ollama_multi_tools.py" -ForegroundColor Yellow
Write-Host ""
