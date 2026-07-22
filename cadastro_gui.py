# cadastro_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # <-- ADICIONADO simpledialog
import json
import os
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

class CadastroAlunosGUI:
    def __init__(self):
        self.data_file = "db_alunos.polymath"
        self.crypt_file = "db_alunos.polymath_crypt"
        self.key_file = "key.key"
        self.data = []
        self.current_id = 1
        
        self.window = tk.Tk()
        self.window.title("📋 Cadastro de Alunos - PolyMath")
        self.window.geometry("950x650")  # Aumentado para acomodar mais botões
        self.window.configure(bg='#f0f0f0')
        
        self.create_widgets()
        self.load_initial_data()
        self.window.mainloop()
    
    def create_widgets(self):
        # Título
        title_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📋 Sistema de Cadastro de Alunos",
                font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=10, pady=10)
        main_frame.pack(fill='both', expand=True)
        
        # Frame de entrada
        entry_frame = tk.LabelFrame(main_frame, text="Dados do Aluno",
                                   font=('Arial', 10, 'bold'), bg='#f0f0f0')
        entry_frame.pack(fill='x', pady=(0, 10))
        
        # Campos de entrada
        fields_frame = tk.Frame(entry_frame, bg='#f0f0f0')
        fields_frame.pack(pady=10, padx=10)
        
        # Nome
        tk.Label(fields_frame, text="Nome:", font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Idade
        tk.Label(fields_frame, text="Idade:", font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.age_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.age_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Telefone
        tk.Label(fields_frame, text="Telefone:", font=('Arial', 10), bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.phone_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Curso
        tk.Label(fields_frame, text="Curso:", font=('Arial', 10), bg='#f0f0f0').grid(row=1, column=2, sticky='e', padx=5, pady=5)
        self.course_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.course_var, width=30).grid(row=1, column=3, padx=5, pady=5)
        
        # Botões de ação - Linha 1
        btn_frame1 = tk.Frame(entry_frame, bg='#f0f0f0')
        btn_frame1.pack(pady=5)
        
        tk.Button(btn_frame1, text="➕ Adicionar", command=self.add_student,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), width=12).pack(side='left', padx=3)
        tk.Button(btn_frame1, text="✏️ Atualizar", command=self.update_student,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'), width=12).pack(side='left', padx=3)
        tk.Button(btn_frame1, text="🗑️ Remover", command=self.delete_student,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), width=12).pack(side='left', padx=3)
        tk.Button(btn_frame1, text="🔍 Buscar", command=self.search_student,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), width=12).pack(side='left', padx=3)
        
        # Botões de ação - Linha 2 (SALVAR E CARREGAR)
        btn_frame2 = tk.Frame(entry_frame, bg='#f0f0f0')
        btn_frame2.pack(pady=5)
        
        tk.Button(btn_frame2, text="💾 Salvar (Normal)", 
                 command=lambda: self.save_data(encrypted=False),
                 bg='#27ae60', fg='white', font=('Arial', 9, 'bold'), width=15).pack(side='left', padx=3)
        tk.Button(btn_frame2, text="🔒 Salvar (Crypt)", 
                 command=lambda: self.save_data(encrypted=True),
                 bg='#2c3e50', fg='white', font=('Arial', 9, 'bold'), width=15).pack(side='left', padx=3)
        tk.Button(btn_frame2, text="📤 Carregar (Normal)", 
                 command=lambda: self.load_data_dialog(encrypted=False),
                 bg='#2980b9', fg='white', font=('Arial', 9, 'bold'), width=15).pack(side='left', padx=3)
        tk.Button(btn_frame2, text="🔓 Carregar (Crypt)", 
                 command=lambda: self.load_data_dialog(encrypted=True),
                 bg='#8e44ad', fg='white', font=('Arial', 9, 'bold'), width=15).pack(side='left', padx=3)
        tk.Button(btn_frame2, text="🔄 Atualizar Lista", 
                 command=self.refresh_tree,
                 bg='#7f8c8d', fg='white', font=('Arial', 9, 'bold'), width=15).pack(side='left', padx=3)
        
        # Frame de listagem
        list_frame = tk.LabelFrame(main_frame, text="Lista de Alunos",
                                  font=('Arial', 10, 'bold'), bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True)
        
        # Treeview
        columns = ('ID', 'Nome', 'Idade', 'Telefone', 'Curso')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind para seleção
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = tk.Label(self.window, textvariable=self.status_var, 
                             relief='sunken', anchor='w', bg='#ecf0f1')
        status_bar.pack(side='bottom', fill='x')
    
    def format_phone(self, phone):
        """Formata telefone: (XX) X XXXX-XXXX"""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 11:
            return f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}"
        else:
            return phone
    
    def load_initial_data(self):
        """Tenta carregar dados existentes"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    if self.data:
                        self.current_id = max(s['id'] for s in self.data) + 1
                        self.refresh_tree()
                        self.status_var.set(f"Carregados {len(self.data)} alunos")
            except:
                pass
    
    def load_data(self, encrypted=False):
        """Carrega os dados do arquivo"""
        try:
            if encrypted:
                if not os.path.exists(self.crypt_file):
                    return []
                with open(self.crypt_file, 'rb') as f:
                    encrypted_data = f.read()
                
                if os.path.exists(self.key_file):
                    with open(self.key_file, 'rb') as f:
                        key = f.read()
                    cipher = Fernet(key)
                    decrypted_data = cipher.decrypt(encrypted_data)
                    return json.loads(decrypted_data.decode())
                else:
                    return []
            else:
                if not os.path.exists(self.data_file):
                    return []
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except InvalidToken:
            messagebox.showerror("Erro", "Chave de criptografia inválida!\nOs dados não podem ser lidos.")
            return []
    
    def save_data(self, encrypted=False):
        """Salva os dados no arquivo"""
        try:
            if not self.data:
                messagebox.showwarning("Aviso", "Não há dados para salvar!")
                return
            
            if encrypted:
                if not os.path.exists(self.key_file):
                    key = Fernet.generate_key()
                    with open(self.key_file, 'wb') as f:
                        f.write(key)
                else:
                    with open(self.key_file, 'rb') as f:
                        key = f.read()
                
                cipher = Fernet(key)
                json_data = json.dumps(self.data, ensure_ascii=False)
                encrypted_data = cipher.encrypt(json_data.encode())
                
                with open(self.crypt_file, 'wb') as f:
                    f.write(encrypted_data)
                self.status_var.set(f"Dados salvos com criptografia! ({len(self.data)} alunos)")
                messagebox.showinfo("Sucesso", f"Dados salvos com criptografia!\n{len(self.data)} alunos salvos.")
            else:
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                self.status_var.set(f"Dados salvos! ({len(self.data)} alunos)")
                messagebox.showinfo("Sucesso", f"Dados salvos com sucesso!\n{len(self.data)} alunos salvos.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")
            self.status_var.set("Erro ao salvar dados!")
    
    def load_data_dialog(self, encrypted=False):
        """Carrega dados do arquivo selecionado"""
        try:
            data = self.load_data(encrypted=encrypted)
            if data:
                self.data = data
                if self.data:
                    self.current_id = max(s['id'] for s in self.data) + 1
                self.refresh_tree()
                self.status_var.set(f"Carregados {len(data)} alunos")
                msg = "criptografados" if encrypted else "não criptografados"
                messagebox.showinfo("Sucesso", f"Carregados {len(data)} alunos ({msg})!")
            else:
                msg = "criptografados" if encrypted else "não criptografados"
                messagebox.showwarning("Aviso", f"Nenhum dado {msg} encontrado!")
                self.status_var.set("Nenhum dado encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            self.status_var.set("Erro ao carregar dados!")
    
    def refresh_tree(self):
        """Atualiza a Treeview com os dados atuais"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for student in sorted(self.data, key=lambda x: x['id']):
            self.tree.insert('', 'end', values=(
                student['id'],
                student['nome'],
                student['idade'],
                student['telefone'],
                student['curso']
            ))
        self.status_var.set(f"{len(self.data)} alunos na lista")
    
    def add_student(self):
        """Adiciona um novo aluno"""
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        phone = self.phone_var.get().strip()
        course = self.course_var.get().strip()
        
        if not all([name, age, phone, course]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        try:
            age = int(age)
            if age <= 0 or age > 120:
                messagebox.showwarning("Aviso", "Idade inválida!")
                return
        except ValueError:
            messagebox.showwarning("Aviso", "Digite uma idade válida!")
            return
        
        if not phone.isdigit():
            messagebox.showwarning("Aviso", "Telefone deve conter apenas números!")
            return
        
        formatted_phone = self.format_phone(phone)
        
        student = {
            'id': self.current_id,
            'nome': name,
            'idade': age,
            'telefone': formatted_phone,
            'curso': course
        }
        
        self.data.append(student)
        self.current_id += 1
        self.refresh_tree()
        self.clear_fields()
        self.status_var.set(f"Aluno '{name}' adicionado com sucesso!")
        messagebox.showinfo("Sucesso", f"Aluno '{name}' adicionado com sucesso!")
    
    def update_student(self):
        """Atualiza os dados do aluno selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um aluno para atualizar!")
            return
        
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        phone = self.phone_var.get().strip()
        course = self.course_var.get().strip()
        
        if not all([name, age, phone, course]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        try:
            age = int(age)
            if age <= 0 or age > 120:
                messagebox.showwarning("Aviso", "Idade inválida!")
                return
        except ValueError:
            messagebox.showwarning("Aviso", "Digite uma idade válida!")
            return
        
        if not phone.isdigit():
            messagebox.showwarning("Aviso", "Telefone deve conter apenas números!")
            return
        
        student_id = int(self.tree.item(selection[0])['values'][0])
        
        for student in self.data:
            if student['id'] == student_id:
                student['nome'] = name
                student['idade'] = age
                student['telefone'] = self.format_phone(phone)
                student['curso'] = course
                break
        
        self.refresh_tree()
        self.clear_fields()
        self.status_var.set(f"Aluno '{name}' atualizado com sucesso!")
        messagebox.showinfo("Sucesso", f"Aluno '{name}' atualizado com sucesso!")
    
    def delete_student(self):
        """Remove o aluno selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um aluno para remover!")
            return
        
        student_id = int(self.tree.item(selection[0])['values'][0])
        student_name = self.tree.item(selection[0])['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o aluno '{student_name}'?"):
            self.data = [s for s in self.data if s['id'] != student_id]
            self.refresh_tree()
            self.clear_fields()
            self.status_var.set(f"Aluno '{student_name}' removido!")
            messagebox.showinfo("Sucesso", f"Aluno '{student_name}' removido com sucesso!")
    
    def search_student(self):
        """Busca aluno por nome ou ID"""
        search = simpledialog.askstring("🔍 Buscar Aluno", "Digite o nome ou ID do aluno:")
        if not search:
            return
        
        self.refresh_tree()
        found = False
        found_items = []
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if search.lower() in str(values[1]).lower() or search == str(values[0]):
                found_items.append(item)
                self.tree.selection_add(item)
                self.tree.see(item)
                found = True
        
        if not found:
            messagebox.showinfo("Busca", "Nenhum aluno encontrado!")
            self.status_var.set("Nenhum aluno encontrado")
        else:
            self.status_var.set(f"Encontrados {len(found_items)} alunos")
            if len(found_items) == 1:
                messagebox.showinfo("Busca", f"1 aluno encontrado!")
            else:
                messagebox.showinfo("Busca", f"{len(found_items)} alunos encontrados!")
    
    def on_tree_select(self, event):
        """Preenche campos com dados do aluno selecionado"""
        selection = self.tree.selection()
        if not selection:
            return
        
        values = self.tree.item(selection[0])['values']
        if values:
            self.name_var.set(values[1])
            self.age_var.set(values[2])
            
            # Remove formatação para edição
            phone_raw = values[3].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
            self.phone_var.set(phone_raw)
            
            self.course_var.set(values[4])
            self.status_var.set(f"Editando aluno: {values[1]}")
    
    def clear_fields(self):
        """Limpa os campos de entrada"""
        self.name_var.set('')
        self.age_var.set('')
        self.phone_var.set('')
        self.course_var.set('')
        self.tree.selection_remove(self.tree.selection())

if __name__ == "__main__":
    CadastroAlunosGUI()