import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Peças")
        self.geometry("700x600")
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

        # Criação dos widgets
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
            self, values=["Bom", "Ótimo", "Ruim"])
        self.label_valor = tk.Label(self, text="Valor:")
        self.entry_valor = tk.Entry(self)
        self.button_adicionar = tk.Button(
            self, text="Adicionar", command=self.adicionar_peca)
        self.button_listar = tk.Button(
            self, text="Listar Peças", command=self.listar_pecas)
        self.listbox_pecas = tk.Listbox(self, width=100)
        self.button_atualizar = tk.Button(
            self, text="Atualizar", command=self.atualizar_peca)
        self.button_vendas = tk.Button(
            self, text="Vendas", command=self.abrir_janela_vendas)

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
        self.button_atualizar.grid(row=7, column=0, padx=5, pady=5)
        self.button_vendas.grid(row=7, column=1, padx=5, pady=5)

    def adicionar_peca(self):
        categoria = self.combobox_categoria.get()
        descricao = self.combobox_descricao.get()
        quantidade = self.entry_quantidade.get()
        qualidade = self.combobox_qualidade.get()
        valor = self.entry_valor.get()

        if not categoria or not descricao or not quantidade or not qualidade or not valor:
            messagebox.showerror(
                "Erro", "Preencha todos os campos para adicionar uma peça.")
            return

        try:
            quantidade = int(quantidade)
            valor = float(valor)
        except ValueError:
            messagebox.showerror(
                "Erro", "Quantidade e valor devem ser números.")
            return

        self.cursor.execute("""
            INSERT INTO pecas (categoria, descricao, quantidade, qualidade, valor)
            VALUES (?, ?, ?, ?, ?)
        """, (categoria, descricao, quantidade, qualidade, valor))

        self.conn.commit()
        messagebox.showinfo("Sucesso", "Peça adicionada com sucesso.")
        self.limpar_campos()

    def listar_pecas(self):
        self.listbox_pecas.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM pecas")
        pecas = self.cursor.fetchall()
        for peca in pecas:
            self.listbox_pecas.insert(
                tk.END, f"{peca[0]} - {peca[1]} - {peca[2]} - {peca[3]} - {peca[4]} - {peca[5]}")

    def atualizar_peca(self):
        selecionado = self.listbox_pecas.curselection()
        if not selecionado:
            messagebox.showerror(
                "Erro", "Selecione uma peça para atualizar.")
            return

        peca_id = self.listbox_pecas.get(selecionado).split(" - ")[0]
        nova_quantidade = self.entry_quantidade.get()
        novo_valor = self.entry_valor.get()

        if not nova_quantidade or not novo_valor:
            messagebox.showerror(
                "Erro", "Preencha todos os campos para atualizar a peça.")
            return

        try:
            nova_quantidade = int(nova_quantidade)
            novo_valor = float(novo_valor)
        except ValueError:
            messagebox.showerror(
                "Erro", "Quantidade e valor devem ser números.")
            return

        self.cursor.execute("""
            UPDATE pecas
            SET quantidade = ?, valor = ?
            WHERE id = ?
        """, (nova_quantidade, novo_valor, peca_id))

        self.conn.commit()
        messagebox.showinfo("Sucesso", "Peça atualizada com sucesso.")
        self.limpar_campos()

    def abrir_janela_vendas(self):
        selecionado = self.listbox_pecas.curselection()
        if not selecionado:
            messagebox.showerror(
                "Erro", "Selecione uma peça para registrar a venda.")
            return

        peca_id = self.listbox_pecas.get(selecionado).split(" - ")[0]
        self.conn.close()
        self.destroy()
        JanelaVendas(peca_id)

    def limpar_campos(self):
        self.combobox_categoria.set("")
        self.combobox_descricao.set("")
        self.entry_quantidade.delete(0, tk.END)
        self.combobox_qualidade.set("")
        self.entry_valor.delete(0, tk.END)


class JanelaVendas(tk.Tk):
    def __init__(self, peca_id):
        super().__init__()
        self.title("Registrar Venda")
        self.geometry("400x200")
        self.option_add("*Font", "Helvetica 12")

        self.peca_id = peca_id

        self.label_quantidade = tk.Label(self, text="Quantidade Vendida:")
        self.entry_quantidade = tk.Entry(self)
        self.button_registrar = tk.Button(
            self, text="Registrar", command=self.registrar_venda)

        self.label_quantidade.pack(padx=10, pady=10)
        self.entry_quantidade.pack(padx=10, pady=10)
        self.button_registrar.pack(padx=10, pady=10)

    def registrar_venda(self):
        quantidade_vendida = self.entry_quantidade.get()

        if not quantidade_vendida:
            messagebox.showerror(
                "Erro", "Preencha a quantidade vendida.")
            return

        try:
            quantidade_vendida = int(quantidade_vendida)
        except ValueError:
            messagebox.showerror(
                "Erro", "Quantidade vendida deve ser um número.")
            return

        app = App()
        app.conn = sqlite3.connect("pecas.db")
        app.cursor = app.conn.cursor()

        app.cursor.execute("SELECT quantidade FROM pecas WHERE id = ?",
                           (self.peca_id,))
        peca = app.cursor.fetchone()
        quantidade_atual = peca[0]

        if quantidade_vendida > quantidade_atual:
            messagebox.showerror(
                "Erro", "Não há quantidade suficiente em estoque.")
            return

        quantidade_restante = quantidade_atual - quantidade_vendida

        app.cursor.execute("""
            UPDATE pecas
            SET quantidade = ?
            WHERE id = ?
        """, (quantidade_restante, self.peca_id))

        app.conn.commit()
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso.")
        app.listar_pecas()

        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
