# suite_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class PolyMathSuiteGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🧮 Suíte PolyMath Educacional")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        self.create_widgets()
        self.window.mainloop()
    
    def create_widgets(self):
        # Título
        title_frame = tk.Frame(self.window, bg='#2c3e50', height=100)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🧮 Suíte PolyMath Educacional",
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(expand=True)
        tk.Label(title_frame, text="Versão 1.0.0",
                font=('Arial', 10), bg='#2c3e50', fg='#ecf0f1').pack()
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Botões
        self.create_button(main_frame, "🧮 Calculadora (CMD)", 
                          "calculadora_cmd.exe", 0)
        self.create_button(main_frame, "🧮 Calculadora (GUI)", 
                          "calculadora_gui.exe", 1)
        self.create_button(main_frame, "📋 Cadastro de Alunos (CMD)", 
                          "cadastro_cmd.exe", 2)
        self.create_button(main_frame, "📋 Cadastro de Alunos (GUI)", 
                          "cadastro_gui.exe", 3)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=4, column=0, 
                                                            columnspan=2, sticky='ew', pady=15)
        
        # Botões de informação
        self.create_info_button(main_frame, "ℹ️ Sobre", self.show_about, 5)
        self.create_info_button(main_frame, "📚 Instruções", self.show_instructions, 6)
        
        # Botão Sair
        tk.Button(main_frame, text="🚪 Sair", command=self.window.quit,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).grid(row=7, column=0, columnspan=2, pady=20)
    
    def create_button(self, parent, text, executable, row):
        btn = tk.Button(parent, text=text, 
                       command=lambda: self.run_executable(executable),
                       font=('Arial', 11), bg='#3498db', fg='white',
                       padx=20, pady=10, width=25)
        btn.grid(row=row, column=0, columnspan=2, pady=5, sticky='ew')
    
    def create_info_button(self, parent, text, command, row):
        btn = tk.Button(parent, text=text,
                       command=command,
                       font=('Arial', 11), bg='#95a5a6', fg='white',
                       padx=20, pady=10, width=25)
        btn.grid(row=row, column=0, columnspan=2, pady=5, sticky='ew')
    
    def run_executable(self, executable):
        """Executa um programa da suíte"""
        try:
            if os.path.exists(executable):
                subprocess.Popen([executable], shell=True)
            else:
                # Tenta executar como script Python se o executável não existir
                script_name = executable.replace('.exe', '.py')
                if os.path.exists(script_name):
                    subprocess.Popen([sys.executable, script_name], shell=True)
                else:
                    messagebox.showerror("Erro", f"Programa não encontrado: {executable}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar: {e}")
    
    def show_about(self):
        about_window = tk.Toplevel(self.window)
        about_window.title("ℹ️ Sobre a Suíte PolyMath")
        about_window.geometry("500x450")
        about_window.configure(bg='#f0f0f0')
        
        # Scrollable text
        text_widget = tk.Text(about_window, wrap='word', font=('Arial', 10),
                             bg='#f0f0f0', padx=20, pady=20)
        scrollbar = ttk.Scrollbar(about_window, orient='vertical', 
                                  command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        about_text = """
        👨‍💻 DESENVOLVEDOR
        
        Nome: Enio Alves Borges
        GitHub: @niopolimathtechnical-00110011
        Projeto: Suíte PolyMath Educacional
        
        
        📌 SOBRE A SUÍTE
        
        A Suíte PolyMath Educacional é um conjunto de ferramentas
        educacionais desenvolvidas para exemplificar o funcionamento
        de programas em Windows nos modos texto e gráfico.
        
        Objetivos Pedagógicos:
        • Demonstrar a interação usuário-programa em diferentes interfaces
        • Exemplificar conceitos de persistência de dados
        • Ilustrar segurança de dados com criptografia
        • Apresentar operações básicas de computação
        
        Aplicativos Inclusos:
        • Calculadora (CMD e GUI) - Operações matemáticas básicas
        • Cadastro de Alunos (CMD e GUI) - CRUD com persistência
        
        
        📁 ESTRUTURA DE DADOS
        
        • db_alunos.polymath - Dados não criptografados (demo)
        • db_alunos.polymath_crypt - Dados criptografados (segurança)
        • key.key - Chave de criptografia (gerada automaticamente)
        
        
        📄 LICENÇA
        
        MIT License - Software livre para fins educacionais
        
        
        ☕ DOAÇÕES
        
        Chave PIX: soletrepix@gmail.com
        Titular: Enio Alves Borges
        Instituição: Banco do Brasil
        
        Sua contribuição ajuda a manter o projeto!
        """
        
        text_widget.insert('1.0', about_text)
        text_widget.configure(state='disabled')
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(about_window, text="Fechar", command=about_window.destroy,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(pady=10)
    
    def show_instructions(self):
        inst_window = tk.Toplevel(self.window)
        inst_window.title("📚 Instruções Didáticas")
        inst_window.geometry("550x500")
        inst_window.configure(bg='#f0f0f0')
        
        text_widget = tk.Text(inst_window, wrap='word', font=('Arial', 10),
                             bg='#f0f0f0', padx=20, pady=20)
        scrollbar = ttk.Scrollbar(inst_window, orient='vertical',
                                  command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        instructions = """
        🎯 OBJETIVO GERAL
        
        Esta suíte foi desenvolvida para demonstrar na prática os
        conceitos fundamentais de programação e computação.
        
        
        📖 CONCEITOS ABORDADOS
        
        1. Interface de Usuário:
           • Modo Texto (CMD): Interação via console/terminal
           • Modo Gráfico (GUI): Interface com janelas e botões
        
        2. Persistência de Dados:
           • Armazenamento em arquivos locais
           • Dados não criptografados vs. criptografados
           • Importância da segurança da informação
        
        3. Operações Básicas:
           • Operações matemáticas (calculadora)
           • CRUD (Create, Read, Update, Delete) de registros
        
        4. Estrutura de Dados:
           • Listas, dicionários e JSON
           • Manipulação de strings e formatação
        
        
        🔧 COMO UTILIZAR
        
        Menu Principal:
          1. Calculadora - Realize operações matemáticas
          2. Cadastro de Alunos - Gerencie registros de alunos
          3. Sobre - Informações detalhadas do projeto
          4. Instruções - Este guia
          5. Sair - Encerra o programa
        
        
        📝 DICAS PARA ESTUDO
        
        • Compare o funcionamento entre versões CMD e GUI
        • Observe como os dados são armazenados em ambos os formatos
        • Analise a diferença entre dados criptografados e não
        • Experimente editar os arquivos .polymath com um editor de texto
        • Tente importar/exportar dados entre as duas versões
        
        
        🔐 SOBRE CRIPTOGRAFIA
        
        • Dados criptografados usam Fernet (symmetric encryption)
        • A chave é gerada automaticamente na primeira vez que você salva
        • A chave é armazenada em key.key - NÃO PERCA ESTE ARQUIVO!
        • Sem a chave, os dados criptografados não podem ser lidos
        """
        
        text_widget.insert('1.0', instructions)
        text_widget.configure(state='disabled')
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(inst_window, text="Fechar", command=inst_window.destroy,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(pady=10)

if __name__ == "__main__":
    PolyMathSuiteGUI()