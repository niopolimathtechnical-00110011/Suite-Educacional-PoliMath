# cadastro_cmd.py
import os
import json
import time
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

class CadastroAlunosCMD:
    def __init__(self):
        self.data_file = "db_alunos.polymath"
        self.crypt_file = "db_alunos.polymath_crypt"
        self.key_file = "key.key"
        self.clear_screen()
        self.run()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def load_data(self, encrypted=False):
        """Carrega os dados do arquivo"""
        try:
            if encrypted:
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
                with open(self.data_file, 'r') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except InvalidToken:
            print("\n❌ Erro: Chave de criptografia inválida!")
            return []
    
    def save_data(self, data, encrypted=False):
        """Salva os dados no arquivo"""
        try:
            if encrypted:
                if not os.path.exists(self.key_file):
                    key = Fernet.generate_key()
                    with open(self.key_file, 'wb') as f:
                        f.write(key)
                else:
                    with open(self.key_file, 'rb') as f:
                        key = f.read()
                
                cipher = Fernet(key)
                json_data = json.dumps(data, ensure_ascii=False)
                encrypted_data = cipher.encrypt(json_data.encode())
                
                with open(self.crypt_file, 'wb') as f:
                    f.write(encrypted_data)
            else:
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"\n❌ Erro ao salvar dados: {e}")
            return False
    
    def format_phone(self, phone):
        """Formata telefone: (XX) X XXXX-XXXX"""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 11:
            return f"({digits[:2]}) {digits[2]} {digits[3:7]}-{digits[7:]}"
        else:
            return phone
    
    def show_header(self):
        print("=" * 70)
        print("                 📋 SISTEMA DE CADASTRO DE ALUNOS (CMD)")
        print("=" * 70)
    
    def show_menu(self):
        print("\n  [1] ➕ Adicionar Aluno")
        print("  [2] 📋 Listar Alunos")
        print("  [3] 🔍 Buscar Aluno")
        print("  [4] ✏️  Atualizar Aluno")
        print("  [5] 🗑️  Remover Aluno")
        print("  [6] 💾 Salvar (Não Criptografado)")
        print("  [7] 🔒 Salvar (Criptografado)")
        print("  [8] 📤 Carregar Dados")
        print("  [9] 🚪 Voltar ao Menu Principal")
        print("\n" + "-" * 70)
    
    def add_student(self, data):
        self.clear_screen()
        self.show_header()
        print("\n📝 ADICIONAR NOVO ALUNO\n")
        
        name = input("Nome do Aluno: ").strip()
        if not name:
            print("❌ Nome não pode ser vazio!")
            return data
        
        try:
            age = int(input("Idade: ").strip())
            if age <= 0 or age > 120:
                print("❌ Idade inválida!")
                return data
        except ValueError:
            print("❌ Digite uma idade válida!")
            return data
        
        phone = input("Telefone (apenas números): ").strip()
        if not phone.isdigit():
            print("❌ Digite apenas números para o telefone!")
            return data
        
        course = input("Curso: ").strip()
        if not course:
            print("❌ Curso não pode ser vazio!")
            return data
        
        # Formatar telefone
        formatted_phone = self.format_phone(phone)
        
        student = {
            'id': len(data) + 1,
            'nome': name,
            'idade': age,
            'telefone': formatted_phone,
            'curso': course
        }
        
        data.append(student)
        print("\n✅ Aluno adicionado com sucesso!")
        time.sleep(1)
        return data
    
    def list_students(self, data):
        self.clear_screen()
        self.show_header()
        print("\n📋 LISTA DE ALUNOS\n")
        
        if not data:
            print("Nenhum aluno cadastrado!")
        else:
            print(f"Total: {len(data)} alunos\n")
            print("-" * 70)
            for student in data:
                print(f"ID: {student['id']}")
                print(f"Nome: {student['nome']}")
                print(f"Idade: {student['idade']}")
                print(f"Telefone: {student['telefone']}")
                print(f"Curso: {student['curso']}")
                print("-" * 70)
        
        input("\nPressione ENTER para continuar...")
    
    def search_student(self, data):
        self.clear_screen()
        self.show_header()
        print("\n🔍 BUSCAR ALUNO\n")
        
        search = input("Digite o nome ou ID do aluno: ").strip()
        if not search:
            print("❌ Digite um termo para buscar!")
            time.sleep(1)
            return
        
        found = False
        print("\n" + "-" * 70)
        for student in data:
            if search.lower() in student['nome'].lower() or search == str(student['id']):
                print(f"\nID: {student['id']}")
                print(f"Nome: {student['nome']}")
                print(f"Idade: {student['idade']}")
                print(f"Telefone: {student['telefone']}")
                print(f"Curso: {student['curso']}")
                print("-" * 70)
                found = True
        
        if not found:
            print("\n❌ Nenhum aluno encontrado!")
        
        input("\nPressione ENTER para continuar...")
    
    def update_student(self, data):
        self.clear_screen()
        self.show_header()
        print("\n✏️  ATUALIZAR ALUNO\n")
        
        try:
            student_id = int(input("Digite o ID do aluno: ").strip())
            found = False
            
            for student in data:
                if student['id'] == student_id:
                    found = True
                    print(f"\nAluno encontrado: {student['nome']}")
                    
                    name = input("Novo nome (ENTER para manter): ").strip()
                    if name:
                        student['nome'] = name
                    
                    age = input("Nova idade (ENTER para manter): ").strip()
                    if age:
                        try:
                            student['idade'] = int(age)
                        except ValueError:
                            print("❌ Idade inválida, mantendo anterior")
                    
                    phone = input("Novo telefone (ENTER para manter): ").strip()
                    if phone:
                        if phone.isdigit():
                            student['telefone'] = self.format_phone(phone)
                        else:
                            print("❌ Telefone inválido, mantendo anterior")
                    
                    course = input("Novo curso (ENTER para manter): ").strip()
                    if course:
                        student['curso'] = course
                    
                    print("\n✅ Aluno atualizado com sucesso!")
                    break
            
            if not found:
                print("\n❌ Aluno não encontrado!")
            
        except ValueError:
            print("❌ ID inválido!")
        
        time.sleep(1)
        return data
    
    def delete_student(self, data):
        self.clear_screen()
        self.show_header()
        print("\n🗑️  REMOVER ALUNO\n")
        
        try:
            student_id = int(input("Digite o ID do aluno: ").strip())
            found = False
            
            for i, student in enumerate(data):
                if student['id'] == student_id:
                    found = True
                    print(f"\nAluno encontrado: {student['nome']}")
                    confirm = input("Confirma remoção? (s/N): ").strip().lower()
                    
                    if confirm == 's':
                        del data[i]
                        print("\n✅ Aluno removido com sucesso!")
                    else:
                        print("\n❌ Operação cancelada!")
                    break
            
            if not found:
                print("\n❌ Aluno não encontrado!")
            
        except ValueError:
            print("❌ ID inválido!")
        
        time.sleep(1)
        return data
    
    def load_saved_data(self):
        """Carrega dados salvos"""
        self.clear_screen()
        self.show_header()
        print("\n📤 CARREGAR DADOS\n")
        
        print("Opções:")
        print("  1. Carregar dados não criptografados")
        print("  2. Carregar dados criptografados")
        print("  3. Voltar")
        
        option = input("\nEscolha: ").strip()
        
        if option == "1":
            data = self.load_data(encrypted=False)
            if data:
                print(f"\n✅ Carregados {len(data)} alunos!")
            else:
                print("\n⚠️  Nenhum dado encontrado ou arquivo vazio!")
            time.sleep(1)
            return data
        elif option == "2":
            data = self.load_data(encrypted=True)
            if data:
                print(f"\n✅ Carregados {len(data)} alunos!")
            else:
                print("\n⚠️  Nenhum dado encontrado ou arquivo vazio!")
            time.sleep(1)
            return data
        
        return []
    
    def run(self):
        data = []
        
        while True:
            self.clear_screen()
            self.show_header()
            self.show_menu()
            
            option = input("\nEscolha uma opção: ").strip()
            
            if option == "1":
                data = self.add_student(data)
            elif option == "2":
                self.list_students(data)
            elif option == "3":
                self.search_student(data)
            elif option == "4":
                data = self.update_student(data)
            elif option == "5":
                data = self.delete_student(data)
            elif option == "6":
                if self.save_data(data, encrypted=False):
                    print("\n✅ Dados salvos (não criptografado)!")
                else:
                    print("\n❌ Erro ao salvar dados!")
                time.sleep(1)
            elif option == "7":
                if self.save_data(data, encrypted=True):
                    print("\n✅ Dados salvos (criptografado)!")
                else:
                    print("\n❌ Erro ao salvar dados!")
                time.sleep(1)
            elif option == "8":
                loaded_data = self.load_saved_data()
                if loaded_data:
                    data = loaded_data
            elif option == "9":
                print("\n👋 Retornando ao menu principal...")
                time.sleep(1)
                break
            else:
                print("\n❌ Opção inválida!")
                time.sleep(1)

if __name__ == "__main__":
    CadastroAlunosCMD()