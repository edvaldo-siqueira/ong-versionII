import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from tkinter import ttk
from reportlab.pdfgen import canvas


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Peças")
        self.geometry("800x700")
        self.option_add("*Font", "Helvetica 12")
       
        # Conexão com o banco de dados
        self.conn = sqlite3.connect("pecas.db")
        self.cursor = self.conn.cursor()

        # Criação da tabela de peças
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pecas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo INTEGER,
                categoria TEXT,
                descricao TEXT,
                quantidade INTEGER,
                qualidade TEXT,
                valor REAL
            )
        """)
        self.conn.commit()

        # Criação dos widgets
        self.label_codigo = tk.Label(self, text="Código:")
        self.entry_codigo = tk.Entry(self)
        self.label_categoria = tk.Label(
            self, text="Categoria/Departamento:")
        self.combobox_categoria = ttk.Combobox(
            self, values=["Homen", "Mulher", "Infantil"])
        self.label_descricao = tk.Label(self, text="Descrição:")
        self.combobox_descricao = ttk.Combobox(
            self, values=["Blusa", "Short", "Bermuda", "Saia", "Calça", "Jaqueta", "Vestido", "Sapato", "Sobretudo"])
        self.label_quantidade = tk.Label(self, text="Quantidade:")
        self.entry_quantidade = tk.Entry(self)
        self.label_qualidade = tk.Label(self, text="Qualidade:")
        self.combobox_qualidade = ttk.Combobox(
            self, values=["BOM", "ÓTIMO", "RUIM"])
        self.label_valor = tk.Label(self, text="Valor:")
        self.entry_valor = tk.Entry(self)
        self.button_adicionar = tk.Button(
            self, text="Adicionar", command=self.adicionar_peca)
        self.button_listar = tk.Button(
            self, text="Listar Peças", command=self.listar_pecas)
        self.listbox_pecas = tk.Listbox(self, width=100)
        self.button_atualizar = tk.Button(
            self, text="Atualizar", command=self.atualizar_peca)
        self.button_imprimir = tk.Button(
            self, text="Imprimir", command=self.abrir_janela_imprimir)
        self.label_pesquisa = tk.Label(
            self, text="Pesquisa:")
        self.entry_pesquisa = tk.Entry(self)
        self.button_pesquisar = tk.Button(
            self, text="Pesquisar", command=self.pesquisar_peca)

        # Posicionamento dos widgets
        self.label_codigo.grid(row=0, column=0, padx=10, pady=10)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=10)
        self.label_categoria.grid(row=1, column=0, padx=10, pady=10)
        self.combobox_categoria.grid(row=1, column=1, padx=10, pady=10)
        self.label_descricao.grid(row=2, column=0, padx=10, pady=10)
        self.combobox_descricao.grid(row=2, column=1, padx=10, pady=10)
        self.label_quantidade.grid(row=3, column=0, padx=10, pady=10)
        self.entry_quantidade.grid(row=3, column=1, padx=10, pady=10)
        self.label_qualidade.grid(row=4, column=0, padx=10, pady=10)
        self.combobox_qualidade.grid(row=4, column=1, padx=10, pady=10)
        self.label_valor.grid(row=5, column=0, padx=10, pady=10)
        self.entry_valor.grid(row=5, column=1, padx=10, pady=10)
        self.button_adicionar.grid(row=6, column=1, pady=10)
        self.button_listar.grid(row=7, column=1, pady=10)
        self.listbox_pecas.grid(
            row=8, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        self.button_atualizar.grid(row=9, column=0, pady=10, sticky="w")
        self.button_imprimir.grid(row=9, column=1, pady=10)
        self.label_pesquisa.grid(row=10, column=0, sticky="w")
        self.entry_pesquisa.grid(row=10, column=1, padx=10, pady=10)
        self.button_pesquisar.grid(row=11, column=1, pady=10)

        # Configuração da seleção da lista
        self.listbox_pecas.bind("<<ListboxSelect>>", self.atualizar_campos)

    def adicionar_peca(self):
        codigo = self.entry_codigo.get()
        categoria = self.combobox_categoria.get()
        descricao = self.combobox_descricao.get()
        quantidade = self.entry_quantidade.get()
        qualidade = self.combobox_qualidade.get()
        valor = self.entry_valor.get()

        if codigo and categoria and descricao and quantidade and qualidade and valor:
            self.cursor.execute("""
                INSERT INTO pecas (codigo, categoria, descricao, quantidade, qualidade, valor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, categoria, descricao, quantidade, qualidade, valor))
            self.conn.commit()
            self.entry_codigo.delete(0, tk.END)
            self.combobox_categoria.set('')
            self.combobox_descricao.set('')
            self.entry_quantidade.delete(0, tk.END)
            self.combobox_qualidade.set('')
            self.entry_valor.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Peça adicionada com sucesso!")

    def listar_pecas(self):
        self.listbox_pecas.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM pecas")
        pecas = self.cursor.fetchall()
        for peca in pecas:
            self.listbox_pecas.insert(tk.END, peca)

    def atualizar_peca(self):
        item_selecionado = self.listbox_pecas.curselection()
        if item_selecionado:
            peca = self.listbox_pecas.get(item_selecionado[0])
            id_peca = peca[0]
            codigo = self.entry_codigo.get()
            categoria = self.combobox_categoria.get()
            descricao = self.combobox_descricao.get()
            quantidade = self.entry_quantidade.get()
            qualidade = self.combobox_qualidade.get()
            valor = self.entry_valor.get()

            if codigo and categoria and descricao and quantidade and qualidade and valor:
                self.cursor.execute("""
                    UPDATE pecas SET codigo=?, categoria=?, descricao=?, quantidade=?, qualidade=?, valor=?
                    WHERE id=?
                """, (codigo, categoria, descricao,
                      quantidade, qualidade, valor, id_peca))
                self.conn.commit()
                self.entry_codigo.delete(0, tk.END)
                self.combobox_categoria.set('')
                self.combobox_descricao.set('')
                self.entry_quantidade.delete(0, tk.END)
                self.combobox_qualidade.set('')
                self.entry_valor.delete(0, tk.END)
                messagebox.showinfo(
                    "Sucesso", "Peça atualizada com sucesso!")
                self.listar_pecas()
            else:
                messagebox.showerror(
                    "Erro", "Por favor, preencha todos os campos!")

    def abrir_janela_imprimir(self):
        janela_imprimir = tk.Toplevel(self)
        janela_imprimir.title("Imprimir Peças")
        janela_imprimir.geometry("500x400")

        scrollbar = tk.Scrollbar(janela_imprimir)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(janela_imprimir, yscrollcommand=scrollbar.set)
        text_area.pack(fill=tk.BOTH, expand=True)

        self.cursor.execute("SELECT * FROM pecas")
        pecas = self.cursor.fetchall()
        for peca in pecas:
            texto_peca = f"Código: {peca[1]}, Categoria/Departamento: {peca[2]}, Descrição: {peca[3]}, " \
                         f"Quantidade: {peca[4]}, Qualidade: {peca[5]}, Valor: {peca[6]}\n"
            text_area.insert(tk.END, texto_peca)

        scrollbar.config(command=text_area.yview)

        button_pdf = tk.Button(janela_imprimir, text="Salvar PDF",
                               command=lambda: self.salvar_pdf(text_area.get("1.0", tk.END)))
        button_pdf.pack(pady=10)

    def salvar_pdf(self, conteudo):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file_path:
            try:
                c = canvas.Canvas(file_path)
                c.setFont("Helvetica", 12)
                lines = conteudo.split("\n")
                y = 750
                for line in lines:
                    c.drawString(50, y, line)
                    y -= 20
                c.save()
                messagebox.showinfo("Sucesso", "PDF salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def pesquisar_peca(self):
        pesquisa = self.entry_pesquisa.get()
        self.listbox_pecas.delete(0, tk.END)
        self.cursor.execute(
            "SELECT * FROM pecas WHERE descricao LIKE ? OR categoria LIKE ?", (f"%{pesquisa}%", f"%{pesquisa}%"))
        pecas = self.cursor.fetchall()
        for peca in pecas:
            self.listbox_pecas.insert(tk.END, peca)

    def atualizar_campos(self, event):
        item_selecionado = self.listbox_pecas.curselection()
        if item_selecionado:
            peca = self.listbox_pecas.get(item_selecionado[0])
            self.entry_codigo.delete(0, tk.END)
            self.combobox_categoria.set('')
            self.combobox_descricao.set('')
            self.entry_quantidade.delete(0, tk.END)
            self.combobox_qualidade.set('')
            self.entry_valor.delete(0, tk.END)
            self.entry_codigo.insert(tk.END, peca[1])
            self.combobox_categoria.set(peca[2])
            self.combobox_descricao.set(peca[3])
            self.entry_quantidade.insert(tk.END, peca[4])
            self.combobox_qualidade.set(peca[5])
            self.entry_valor.insert(tk.END, peca[6])

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
