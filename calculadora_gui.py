# calculadora_gui.py
import tkinter as tk
from tkinter import messagebox, ttk

class CalculadoraGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🧮 Calculadora PolyMath - GUI")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        # Variáveis
        self.operation = tk.StringVar(value="+")
        self.num1_var = tk.StringVar()
        self.num2_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")
        
        self.create_widgets()
        self.window.mainloop()
    
    def create_widgets(self):
        # Título
        title_frame = tk.Frame(self.window, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🧮 Calculadora PolyMath", 
                               font=('Arial', 18, 'bold'), bg='#2c3e50', 
                               fg='white')
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle = tk.Label(title_frame, text="Modo Gráfico", 
                           font=('Arial', 10), bg='#2c3e50', fg='#ecf0f1')
        subtitle.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Campo Número 1
        tk.Label(main_frame, text="Primeiro Número:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=5)
        tk.Entry(main_frame, textvariable=self.num1_var, font=('Arial', 12),
                width=30).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Operação
        tk.Label(main_frame, text="Operação:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=5)
        
        operations_frame = tk.Frame(main_frame, bg='#f0f0f0')
        operations_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        for op in ['+', '-', '*', '/']:
            rb = tk.Radiobutton(operations_frame, text=op, value=op,
                              variable=self.operation, font=('Arial', 14),
                              bg='#f0f0f0', selectcolor='#bdc3c7')
            rb.pack(side='left', padx=10)
        
        # Campo Número 2
        tk.Label(main_frame, text="Segundo Número:", font=('Arial', 10, 'bold'),
                bg='#f0f0f0').grid(row=4, column=0, sticky='w', pady=5)
        tk.Entry(main_frame, textvariable=self.num2_var, font=('Arial', 12),
                width=30).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Botão Calcular
        calc_btn = tk.Button(main_frame, text="🧮 Calcular", 
                            command=self.calculate,
                            font=('Arial', 12, 'bold'), bg='#27ae60',
                            fg='white', padx=20, pady=10)
        calc_btn.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Resultado
        result_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='groove',
                               bd=2)
        result_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')
        
        tk.Label(result_frame, text="Resultado:", font=('Arial', 12, 'bold'),
                bg='#ecf0f1').pack(pady=5)
        
        result_label = tk.Label(result_frame, textvariable=self.result_var,
                              font=('Arial', 20, 'bold'), bg='#ecf0f1',
                              fg='#2c3e50')
        result_label.pack(pady=10)
    
    def calculate(self):
        try:
            num1 = float(self.num1_var.get())
            num2 = float(self.num2_var.get())
            op = self.operation.get()
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    messagebox.showerror("Erro", "Divisão por zero!")
                    return
                result = num1 / num2
            
            self.result_var.set(f"{result:.2f}" if isinstance(result, float) else str(result))
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite números válidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    CalculadoraGUI()