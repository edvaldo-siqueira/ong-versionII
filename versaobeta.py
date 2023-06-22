import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import locale

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(" - Ong CASA DAS MANGUEIRAS - ")
        self.geometry("800x600")
        self.option_add("*Font", "Helvetica 10")

        # Conexão com o banco de dados
        self.conn = sqlite3.connect("pecas.db")
        self.cursor = self.conn.cursor()

        # Criação da tabela de peças
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pecas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT,
                descricao TEXT,
                quantidade INTEGER,
                qualidade TEXT,
                valor REAL
            )
        """)
        self.conn.commit()

        # Criação da tabela de vendas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                peca_id INTEGER,
                quantidade_vendida INTEGER
            )
        """)
        self.conn.commit()

        # Criação dos widgets
        self.label_categoria = tk.Label(self, text="Categoria/Departamento:")
        self.combobox_categoria = ttk.Combobox(self, values=["Homem", "Mulher", "Infantil"], state="readonly")
        self.label_descricao = tk.Label(self, text="Descrição:")
        self.combobox_descricao = ttk.Combobox(self, values=["Blusa", "Short", "Bermuda", "Saia", "Calça", "Jaqueta", "Vestido", "Sapato", "Sobretudo"], state="readonly")
        self.label_quantidade = tk.Label(self, text="Quantidade:")
        self.entry_quantidade = tk.Entry(self)
        self.label_qualidade = tk.Label(self, text="Qualidade:")
        self.combobox_qualidade = ttk.Combobox(self, values=["Bom", "Ótimo", "Ruim"], state="readonly")
        self.label_valor = tk.Label(self, text="Valor/Preço Final:")
        self.entry_valor = tk.Entry(self)
        self.button_adicionar = tk.Button(self, text="Adicionar", command=self.adicionar_peca, bg="#4CAF50", fg="white")
        self.button_listar = tk.Button(self, text="Listar Peças", command=self.listar_pecas, bg="#FF9800", fg="white")
        self.listbox_pecas = tk.Listbox(self, width=100)
        self.button_vendas = tk.Button(self, text="Vendas", command=self.abrir_janela_vendas, bg="#2196F3", fg="white")
        self.button_sobre = tk.Button(self, text="Sobre", command=self.abrir_janela_sobre,  bg="#9C27B0", fg="white")

        # Campo para o valor total de produtos
        self.label_total_produtos = tk.Label(self, text="Total de Produtos:")
        self.cursor.execute("DELETE FROM pecas WHERE quantidade = 0")
        self.conn.commit()

        # Campo para o total de vendas
        self.label_vendas_totais = tk.Label(self, text="Vendas Totais:")

        # Posicionamento dos widgets
        self.label_categoria.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combobox_categoria.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.label_descricao.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combobox_descricao.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.label_quantidade.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_quantidade.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.label_qualidade.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combobox_qualidade.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.label_valor.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_valor.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.button_adicionar.grid(row=5, column=0, padx=5, pady=5)
        self.button_listar.grid(row=5, column=1, padx=5, pady=5)
        self.listbox_pecas.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.button_vendas.grid(row=7, column=1, padx=5, pady=5)
        self.button_sobre.grid(row=7, column=0, padx=5, pady=5)

        # Posicionamento do campo de valor total de produtos
        self.label_total_produtos.grid(row=8, column=0, sticky="w", padx=5, pady=5)

        # Posicionamento do campo de vendas totais
        self.label_vendas_totais.grid(row=9, column=0, sticky="w", padx=5, pady=5)

        # Atualiza o total de produtos e vendas totais
        self.atualizar_total_produtos()
        self.atualizar_vendas_totais()

    def adicionar_peca(self):
        categoria = self.combobox_categoria.get()
        descricao = self.combobox_descricao.get()
        quantidade = self.entry_quantidade.get()
        qualidade = self.combobox_qualidade.get()
        valor = self.entry_valor.get()

        if not categoria or not descricao or not quantidade or not qualidade or not valor:
            messagebox.showerror("Erro", "Preencha todos os campos para adicionar uma peça.")
            return

        try:
            quantidade = int(quantidade)
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e valor devem ser números.")
            return

        self.cursor.execute("""
            INSERT INTO pecas (categoria, descricao, quantidade, qualidade, valor)
            VALUES (?, ?, ?, ?, ?)
        """, (categoria, descricao, quantidade, qualidade, valor))
        self.cursor.execute("DELETE FROM pecas WHERE quantidade = 0")
        self.conn.commit()

        self.conn.commit()
        messagebox.showinfo("Sucesso", "Peça adicionada com sucesso.")
        self.limpar_campos()
        self.atualizar_total_produtos()

    def listar_pecas(self):
        self.listbox_pecas.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM pecas")
        pecas = self.cursor.fetchall()
        for peca in pecas:
            identificacao = f"{peca[0]} - {peca[1]} - {peca[2]} - {peca[3]} - {peca[4]} - {peca[5]}"
            self.listbox_pecas.insert(tk.END, identificacao)

    def abrir_janela_vendas(self):
        VendasWindow(self)

    def abrir_janela_sobre(self):
        SobreWindow(self)

    def limpar_campos(self):
        self.combobox_categoria.set("")
        self.combobox_descricao.set("")
        self.entry_quantidade.delete(0, tk.END)
        self.combobox_qualidade.set("")
        self.entry_valor.delete(0, tk.END)

    def atualizar_total_produtos(self):
        self.cursor.execute("SELECT SUM(quantidade) FROM pecas")
        total_produtos = self.cursor.fetchone()[0]
        if total_produtos is None:
            total_produtos = 0
        self.label_total_produtos.configure(text=f"Total de Produtos: {total_produtos}")

    def atualizar_vendas_totais(self):
        self.cursor.execute("SELECT COUNT(*) FROM vendas")
        total_vendas = self.cursor.fetchone()[0]
        self.label_vendas_totais.configure(text=f"Vendas Totais: {total_vendas}")

        self.cursor.execute("SELECT SUM(p.valor * v.quantidade_vendida) FROM vendas v JOIN pecas p ON v.peca_id = p.id")
        valor_total_vendido = self.cursor.fetchone()[0]
        if valor_total_vendido is None:
            valor_total_vendido = 0.0
        self.label_valor_vendido = tk.Label(self, text=f"Valor Total Vendido: R$ {valor_total_vendido:.2f}")
        self.label_valor_vendido.grid(row=10, column=0, sticky="w", padx=5, pady=5)


class VendasWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Vendas")
        self.geometry("500x400")
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        # Conexão com o banco de dados
        self.conn = sqlite3.connect("pecas.db")
        self.cursor = self.conn.cursor()

        # Criação dos widgets
        self.listbox_pecas = tk.Listbox(self, width=100)
        self.label_quantidade = tk.Label(self, text="Quantidade:")
        self.entry_quantidade = tk.Entry(self)
        self.button_vender = tk.Button(self, text="Vender", command=self.vender_peca)

        # Posicionamento dos widgets
        self.listbox_pecas.pack(padx=5, pady=5)
        self.label_quantidade.pack(padx=5, pady=5)
        self.entry_quantidade.pack(padx=5, pady=5)
        self.button_vender.pack(padx=5, pady=5)

        # Listar peças disponíveis para venda
        self.listar_pecas_disponiveis()

    def listar_pecas_disponiveis(self):
        self.listbox_pecas.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM pecas WHERE quantidade > 0")
        pecas = self.cursor.fetchall()
        for peca in pecas:
            identificacao = f"{peca[0]} - {peca[1]} - {peca[2]} - {peca[3]} - {peca[4]} - {peca[5]}"
            self.listbox_pecas.insert(tk.END, identificacao)

    def vender_peca(self):
        peca_selecionada = self.listbox_pecas.get(tk.ACTIVE)
        quantidade = self.entry_quantidade.get()

        if not peca_selecionada or not quantidade:
            messagebox.showerror("Erro", "Selecione uma peça e informe a quantidade para efetuar a venda.")
            return

        peca_id = peca_selecionada.split(" - ")[0]

        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
            return

        self.cursor.execute("SELECT quantidade FROM pecas WHERE id = ?", (peca_id,))
        quantidade_disponivel = self.cursor.fetchone()[0]

        if quantidade > quantidade_disponivel:
            messagebox.showerror("Erro", "Quantidade solicitada indisponível.")
            return

        self.cursor.execute("""
            INSERT INTO vendas (peca_id, quantidade_vendida)
            VALUES (?, ?)
        """, (peca_id, quantidade))

        self.cursor.execute("""
            UPDATE pecas SET quantidade = quantidade - ? WHERE id = ?
        """, (quantidade, peca_id))

        self.conn.commit()
        messagebox.showinfo("Sucesso", "Venda realizada com sucesso.")
        self.entry_quantidade.delete(0, tk.END)
        self.master.atualizar_total_produtos()
        self.master.atualizar_vendas_totais()
        self.listar_pecas_disponiveis()

    def fechar_janela(self):
        self.conn.close()
        self.destroy()

class SobreWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Sobre")
        self.geometry("500x400")
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        desenvolvedores = [
            "André Alexandre Diederich",
            "Luiz André Soares dos Santos",
            "Karina Basso Punales",
            "Karla Cristina Nascimento de Almeida",
            "Thiago Reis Silva",
            "Heitor Santos Pimentel",
            "Elton Amancio Santos",
            "Robinson Diego da Silva",
            "Ebenezer Guedes da Silva",
            "Edvaldo Siqueira"
        ]

        self.label_sobre = tk.Label(self, text=" - Casa das Mangueiras -")
        self.label_sobre.pack(padx=20, pady=10)

        self.label_desenvolvedores = tk.Label(self, text="Desenvolvedores:")
        self.label_desenvolvedores.pack(padx=20, pady=5)

        for desenvolvedor in desenvolvedores:
            label_desenvolvedor = tk.Label(self, text=desenvolvedor)
            label_desenvolvedor.pack()

    def fechar_janela(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
