# build.py
import os
import subprocess
import sys
import shutil

def clean_build():
    """Limpa arquivos de build anteriores"""
    folders = ['build', 'dist']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Limpando {folder}/...")
    
    # Remove arquivos .spec antigos (opcional)
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)
            print(f"🧹 Removendo {file}...")

def build_with_spec(spec_file):
    """Compila usando arquivo .spec"""
    if not os.path.exists(spec_file):
        print(f"⚠️  {spec_file} não encontrado! Usando compilação direta...")
        return False
    
    # Usa python -m pyinstaller em vez de pyinstaller direto
    cmd = [sys.executable, '-m', 'PyInstaller', spec_file]
    print(f"📦 Compilando {spec_file}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            exe_name = spec_file.replace('.exe.spec', '.exe')
            print(f"✅ {exe_name} criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao compilar {spec_file}")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def build_from_script(script_name):
    """Compila diretamente do script Python"""
    output_name = script_name.replace('.py', '.exe')
    is_gui = 'gui' in script_name.lower()
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--noconsole' if is_gui else '--console',
        '--name', output_name,
        script_name
    ]
    
    print(f"📦 Compilando {script_name} -> {output_name}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print(f"✅ {output_name} criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao compilar {script_name}")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_dependencies():
    """Verifica e instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    # Verifica cryptography
    try:
        import cryptography
        print("✅ cryptography instalado")
    except ImportError:
        print("📥 Instalando cryptography...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'cryptography'])
    
    # Verifica pyinstaller
    try:
        import PyInstaller
        print("✅ PyInstaller instalado")
    except ImportError:
        print("📥 Instalando PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

def main():
    print("=" * 70)
    print("    🚀 COMPILADOR DA SUÍTE POLYMATH EDUCACIONAL")
    print("=" * 70)
    print()
    
    # Verifica dependências
    check_dependencies()
    print()
    
    # Lista de scripts para compilar
    scripts = [
        'suite_cmd.py',
        'suite_gui.py',
        'calculadora_cmd.py',
        'calculadora_gui.py',
        'cadastro_cmd.py',
        'cadastro_gui.py',
    ]
    
    # Pergunta se deve limpar build anteriores
    clean = input("🧹 Limpar builds anteriores? (s/N): ").strip().lower()
    if clean == 's':
        clean_build()
        print()
    
    print("=" * 70)
    print("    🔨 INICIANDO COMPILAÇÃO")
    print("=" * 70 + "\n")
    
    success_count = 0
    fail_count = 0
    compiled_files = []
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"⚠️  Arquivo {script} não encontrado!")
            fail_count += 1
            continue
        
        # Tenta usar .spec primeiro
        spec_file = script.replace('.py', '.exe.spec')
        if os.path.exists(spec_file):
            print(f"📄 Usando arquivo .spec: {spec_file}")
            if build_with_spec(spec_file):
                success_count += 1
                compiled_files.append(script.replace('.py', '.exe'))
            else:
                # Se falhar, tenta compilação direta
                print(f"🔄 Tentando compilação direta de {script}...")
                if build_from_script(script):
                    success_count += 1
                    compiled_files.append(script.replace('.py', '.exe'))
                else:
                    fail_count += 1
        else:
            # Compilação direta
            if build_from_script(script):
                success_count += 1
                compiled_files.append(script.replace('.py', '.exe'))
            else:
                fail_count += 1
        
        print()  # Linha em branco entre compilações
    
    print("=" * 70)
    print("    📊 RESUMO DA COMPILAÇÃO")
    print("=" * 70)
    print(f"✅ Sucesso: {success_count} arquivos")
    print(f"❌ Falhas: {fail_count} arquivos")
    
    if success_count > 0 and os.path.exists('dist'):
        print("\n📁 Executáveis gerados em: ./dist/")
        print("\n📋 Arquivos gerados:")
        
        exe_files = [f for f in os.listdir('dist') if f.endswith('.exe')]
        if exe_files:
            for file in sorted(exe_files):
                size = os.path.getsize(f'dist/{file}') / (1024 * 1024)
                print(f"   ✅ {file} ({size:.2f} MB)")
        else:
            print("   ⚠️  Nenhum executável encontrado na pasta dist/")
    
    print("\n🎉 Compilação concluída!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Compilação interrompida pelo usuário!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)