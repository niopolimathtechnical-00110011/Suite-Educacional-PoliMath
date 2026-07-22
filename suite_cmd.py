# suite_cmd.py
import os
import subprocess
import sys
import time

class PolyMathSuiteCMD:
    def __init__(self):
        self.version = "1.0.0"
        self.developer = "Enio Alves Borges"
        self.github = "@niopolimathtechnical-00110011"
        self.clear_screen()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        print("=" * 70)
        print("          🧮 Suíte PolyMath Educacional v{}".format(self.version))
        print("=" * 70)
        print("  Desenvolvedor: {}".format(self.developer))
        print("  GitHub: {}".format(self.github))
        print("=" * 70)
    
    def show_about(self):
        self.clear_screen()
        print("=" * 70)
        print("                         📋 SOBRE O PROGRAMA")
        print("=" * 70)
        print("\n👨‍💻 DESENVOLVEDOR")
        print("  Nome: Enio Alves Borges")
        print("  GitHub: @niopolimathtechnical-00110011")
        print("  Projeto: Suíte PolyMath Educacional")
        print("\n📌 SOBRE A SUÍTE")
        print("  A Suíte PolyMath Educacional é um conjunto de ferramentas")
        print("  educacionais desenvolvidas para exemplificar o funcionamento")
        print("  de programas em Windows nos modos texto e gráfico.")
        print("\n  Objetivos Pedagógicos:")
        print("  • Demonstrar a interação usuário-programa em diferentes interfaces")
        print("  • Exemplificar conceitos de persistência de dados")
        print("  • Ilustrar segurança de dados com criptografia")
        print("  • Apresentar operações básicas de computação")
        print("\n  Aplicativos Inclusos:")
        print("  • Calculadora (CMD e GUI) - Operações matemáticas básicas")
        print("  • Cadastro de Alunos (CMD e GUI) - CRUD com persistência")
        print("\n📁 ESTRUTURA DE DADOS")
        print("  • db_alunos.polymath - Dados não criptografados (demo)")
        print("  • db_alunos.polymath_crypt - Dados criptografados (segurança)")
        print("\n📄 LICENÇA")
        print("  MIT License - Software livre para fins educacionais")
        print("\n☕ DOAÇÕES")
        print("  Chave PIX: soletrepix@gmail.com")
        print("  Titular: Enio Alves Borges")
        print("  Instituição: Banco do Brasil")
        print("\n  Sua contribuição ajuda a manter o projeto!")
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def show_instructions(self):
        self.clear_screen()
        print("=" * 70)
        print("                    📚 INSTRUÇÕES DIDÁTICAS")
        print("=" * 70)
        print("\n🎯 OBJETIVO GERAL")
        print("  Esta suíte foi desenvolvida para demonstrar na prática os")
        print("  conceitos fundamentais de programação e computação.")
        print("\n📖 CONCEITOS ABORDADOS")
        print("\n  1. Interface de Usuário:")
        print("     • Modo Texto (CMD): Interação via console/terminal")
        print("     • Modo Gráfico (GUI): Interface com janelas e botões")
        print("\n  2. Persistência de Dados:")
        print("     • Armazenamento em arquivos locais")
        print("     • Dados não criptografados vs. criptografados")
        print("     • Importância da segurança da informação")
        print("\n  3. Operações Básicas:")
        print("     • Operações matemáticas (calculadora)")
        print("     • CRUD (Create, Read, Update, Delete) de registros")
        print("\n  4. Estrutura de Dados:")
        print("     • Listas, dicionários e JSON")
        print("     • Manipulação de strings e formatação")
        print("\n🔧 COMO UTILIZAR")
        print("\n  Menu Principal:")
        print("    1. Calculadora - Realize operações matemáticas")
        print("    2. Cadastro de Alunos - Gerencie registros de alunos")
        print("    3. Sobre - Informações detalhadas do projeto")
        print("    4. Instruções - Este guia")
        print("    5. Sair - Encerra o programa")
        print("\n  Dicas para Estudo:")
        print("    • Compare o funcionamento entre versões CMD e GUI")
        print("    • Observe como os dados são armazenados em ambos os formatos")
        print("    • Analise a diferença entre dados criptografados e não")
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def show_menu(self):
        while True:
            self.clear_screen()
            self.show_header()
            print("\n  [1] 🧮 Calculadora (CMD)")
            print("  [2] 🧮 Calculadora (GUI)")
            print("  [3] 📋 Cadastro de Alunos (CMD)")
            print("  [4] 📋 Cadastro de Alunos (GUI)")
            print("  [5] ℹ️  Sobre")
            print("  [6] 📚 Instruções Didáticas")
            print("  [7] 🚪 Sair")
            print("\n" + "-" * 70)
            
            try:
                option = input("\nEscolha uma opção: ").strip()
                
                if option == "1":
                    subprocess.run(["calculadora_cmd.exe"], shell=True)
                elif option == "2":
                    subprocess.run(["calculadora_gui.exe"], shell=True)
                elif option == "3":
                    subprocess.run(["cadastro_cmd.exe"], shell=True)
                elif option == "4":
                    subprocess.run(["cadastro_gui.exe"], shell=True)
                elif option == "5":
                    self.show_about()
                elif option == "6":
                    self.show_instructions()
                elif option == "7":
                    print("\n👋 Obrigado por usar a Suíte PolyMath Educacional!")
                    time.sleep(1)
                    sys.exit(0)
                else:
                    print("\n❌ Opção inválida!")
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n👋 Programa encerrado!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                time.sleep(2)

if __name__ == "__main__":
    app = PolyMathSuiteCMD()
    app.show_menu()