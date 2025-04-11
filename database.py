import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("musicas.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key, nome text, senha text)''' )
    
    cursor.execute('''create table if not exists musicas (id integer primary key, titulo text, conteudo text, status text, email_usuario text,
             FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')

    conexao.commit()

def criar_usuario(formulario):
    # Verifica se ja existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) from usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()

    quantidade_de_emails = cursor.fetchone()
    if(quantidade_de_emails[0] > 0):
        print("LOG: Já existe esse email cadastrado no banco!")
        return False
    
    senha_criptografada = generate_password_hash(formulario['senha'])
    cursor.execute('''INSERT INTO usuarios (email, nome, senha)
                        VALUES (?, ?, ?)''', (formulario['email'], formulario['nome'], senha_criptografada))
    conexao.commit()
    return True

def fazer_login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) from usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()

    quantidade_de_emails = cursor.fetchone()
    if(quantidade_de_emails[0] < 0):
        print("LOG: email não encontrado.")
        return False
    else:
        try: 
            cursor = conexao.cursor()
            cursor.execute('''SELECT (senha) from usuarios WHERE email=?''',(formulario['email'],))
            conexao.commit()
            senha_criptografada = cursor.fetchone()
            resultado_verificacao = check_password_hash(senha_criptografada[0], formulario['senha'])
            return resultado_verificacao
        except:
            return False
        
def criar_musica(titulo,conteudo,status,email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' INSERT INTO musicas (titulo, conteudo, status, email_usuario)
                   VALUES (?,?,?,?)''', 
                   (titulo,conteudo, status, False, email))
    conexao.commit()
    return True

def excluir_musica(id, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT email_usuario FROM musicas WHERE id=?''', (id,))
    conexao.commit()
    email_banco = cursor.fetchone()
    print(email, email_banco)
    if (email_banco[0] !=email):
        
        return False
    else:
        cursor.execute(''' DELETE FROM musicas WHERE id=?''', (id,))
        conexao.commit()
        cursor.close()
        return True

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM musicas WHERE email_usuario=?',(email,))
    cursor.execute('DELETE FROM usuarios WHERE email=?',(email,))
    conexao.commit()
    return True

# PARTE PRINCIPAL DO PROGRAMA
if __name__ == '__main__':
    criar_tabelas()