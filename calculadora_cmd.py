# calculadora_cmd.py
import os
import time

class CalculadoraCMD:
    def __init__(self):
        self.clear_screen()
        self.show_header()
        self.run()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        print("=" * 70)
        print("                    🧮 CALCULADORA POLYMATH (CMD)")
        print("=" * 70)
    
    def calculate(self, num1, num2, operator):
        try:
            if operator == '+':
                return num1 + num2
            elif operator == '-':
                return num1 - num2
            elif operator == '*':
                return num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Erro: Divisão por zero!"
                return num1 / num2
            else:
                return "Operador inválido!"
        except Exception as e:
            return f"Erro: {e}"
    
    def run(self):
        while True:
            print("\nOperações disponíveis: +, -, *, /")
            print("Digite 'sair' para voltar ao menu principal\n")
            
            try:
                num1 = input("Digite o primeiro número: ").strip()
                if num1.lower() == 'sair':
                    break
                
                operator = input("Digite o operador (+, -, *, /): ").strip()
                if operator.lower() == 'sair':
                    break
                
                num2 = input("Digite o segundo número: ").strip()
                if num2.lower() == 'sair':
                    break
                
                # Conversão para float
                try:
                    n1 = float(num1)
                    n2 = float(num2)
                except ValueError:
                    print("\n❌ Erro: Digite números válidos!")
                    time.sleep(1)
                    continue
                
                # Calculando
                result = self.calculate(n1, n2, operator)
                
                print("\n" + "-" * 70)
                print(f"📊 Resultado: {n1} {operator} {n2} = {result}")
                print("-" * 70)
                
            except KeyboardInterrupt:
                print("\n")
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                time.sleep(1)
        
        print("\n👋 Retornando ao menu principal...")
        time.sleep(1)

if __name__ == "__main__":
    CalculadoraCMD()