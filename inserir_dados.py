#!/usr/bin/env python3
"""
Script para inserção manual de dados de receitas oftalmológicas
Autor: Manus AI
Data: 2025

Este script permite inserir dados de receitas oftalmológicas diretamente no banco de dados.
Pode ser usado para migração de dados ou inserção em lote.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Adicionar o diretório src ao path para importar os modelos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def conectar_banco():
    """Conecta ao banco de dados SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'database', 'app.db')
    return sqlite3.connect(db_path)

def inserir_receita(conn, dados_receita):
    """
    Insere uma receita no banco de dados
    
    Args:
        conn: Conexão com o banco de dados
        dados_receita: Dicionário com os dados da receita
    """
    cursor = conn.cursor()
    
    query = """
    INSERT INTO receita (
        paciente_nome, armacao, lentes, medico, data_receita,
        esferico_od, cilindrico_od, eixo_od, adicao_od,
        esferico_oe, cilindrico_oe, eixo_oe, adicao_oe,
        observacoes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    valores = (
        dados_receita.get('paciente_nome'),
        dados_receita.get('armacao'),
        dados_receita.get('lentes'),
        dados_receita.get('medico'),
        dados_receita.get('data_receita'),
        dados_receita.get('esferico_od'),
        dados_receita.get('cilindrico_od'),
        dados_receita.get('eixo_od'),
        dados_receita.get('adicao_od'),
        dados_receita.get('esferico_oe'),
        dados_receita.get('cilindrico_oe'),
        dados_receita.get('eixo_oe'),
        dados_receita.get('adicao_oe'),
        dados_receita.get('observacoes')
    )
    
    cursor.execute(query, valores)
    conn.commit()
    return cursor.lastrowid

def inserir_usuario(conn, dados_usuario):
    """
    Insere um usuário no banco de dados
    
    Args:
        conn: Conexão com o banco de dados
        dados_usuario: Dicionário com os dados do usuário
    """
    from werkzeug.security import generate_password_hash
    
    cursor = conn.cursor()
    
    query = """
    INSERT INTO user (username, password_hash, role)
    VALUES (?, ?, ?)
    """
    
    password_hash = generate_password_hash(dados_usuario['password'])
    
    valores = (
        dados_usuario['username'],
        password_hash,
        dados_usuario.get('role', 'atendente')
    )
    
    cursor.execute(query, valores)
    conn.commit()
    return cursor.lastrowid

def exemplo_insercao_receitas():
    """Exemplo de como inserir receitas"""
    
    # Dados de exemplo
    receitas_exemplo = [
        {
            'paciente_nome': 'João Silva',
            'armacao': 'Ray-Ban RB5154',
            'lentes': 'Varilux Comfort',
            'medico': 'Dr. Maria Santos',
            'data_receita': '2025-01-15',
            'esferico_od': -2.50,
            'cilindrico_od': -0.75,
            'eixo_od': 90,
            'adicao_od': None,
            'esferico_oe': -2.25,
            'cilindrico_oe': -0.50,
            'eixo_oe': 85,
            'adicao_oe': None,
            'observacoes': 'Paciente com miopia e astigmatismo'
        },
        {
            'paciente_nome': 'Ana Costa',
            'armacao': 'Oakley OX8081',
            'lentes': 'Zeiss Progressive',
            'medico': 'Dr. Carlos Oliveira',
            'data_receita': '2025-01-20',
            'esferico_od': +1.00,
            'cilindrico_od': None,
            'eixo_od': None,
            'adicao_od': +2.00,
            'esferico_oe': +1.25,
            'cilindrico_oe': None,
            'eixo_oe': None,
            'adicao_oe': +2.00,
            'observacoes': 'Presbiopia, primeira receita multifocal'
        }
    ]
    
    conn = conectar_banco()
    
    try:
        for receita in receitas_exemplo:
            receita_id = inserir_receita(conn, receita)
            print(f"Receita inserida com ID: {receita_id} - Paciente: {receita['paciente_nome']}")
    
    except Exception as e:
        print(f"Erro ao inserir receitas: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def exemplo_insercao_usuarios():
    """Exemplo de como inserir usuários"""
    
    usuarios_exemplo = [
        {
            'username': 'medico1',
            'password': 'senha123',
            'role': 'medico'
        },
        {
            'username': 'atendente1',
            'password': 'senha456',
            'role': 'atendente'
        }
    ]
    
    conn = conectar_banco()
    
    try:
        for usuario in usuarios_exemplo:
            user_id = inserir_usuario(conn, usuario)
            print(f"Usuário inserido com ID: {user_id} - Username: {usuario['username']}")
    
    except Exception as e:
        print(f"Erro ao inserir usuários: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def inserir_dados_interativo():
    """Interface interativa para inserção de dados"""
    
    print("=== Sistema de Inserção de Dados ===")
    print("1. Inserir receita")
    print("2. Inserir usuário")
    print("3. Inserir dados de exemplo")
    print("0. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        inserir_receita_interativa()
    elif opcao == "2":
        inserir_usuario_interativo()
    elif opcao == "3":
        print("Inserindo dados de exemplo...")
        exemplo_insercao_receitas()
        exemplo_insercao_usuarios()
        print("Dados de exemplo inseridos com sucesso!")
    elif opcao == "0":
        print("Saindo...")
    else:
        print("Opção inválida!")

def inserir_receita_interativa():
    """Interface interativa para inserir uma receita"""
    
    print("\n=== Inserir Nova Receita ===")
    
    dados = {}
    dados['paciente_nome'] = input("Nome do paciente: ")
    dados['medico'] = input("Nome do médico: ")
    dados['data_receita'] = input("Data da receita (YYYY-MM-DD): ")
    dados['armacao'] = input("Armação (opcional): ") or None
    dados['lentes'] = input("Lentes (opcional): ") or None
    
    print("\n--- Olho Direito (OD) ---")
    dados['esferico_od'] = input("Esférico OD: ") or None
    dados['cilindrico_od'] = input("Cilíndrico OD: ") or None
    dados['eixo_od'] = input("Eixo OD: ") or None
    dados['adicao_od'] = input("Adição OD: ") or None
    
    print("\n--- Olho Esquerdo (OE) ---")
    dados['esferico_oe'] = input("Esférico OE: ") or None
    dados['cilindrico_oe'] = input("Cilíndrico OE: ") or None
    dados['eixo_oe'] = input("Eixo OE: ") or None
    dados['adicao_oe'] = input("Adição OE: ") or None
    
    dados['observacoes'] = input("Observações (opcional): ") or None
    
    # Converter strings vazias para None e números
    for key in ['esferico_od', 'cilindrico_od', 'eixo_od', 'adicao_od',
                'esferico_oe', 'cilindrico_oe', 'eixo_oe', 'adicao_oe']:
        if dados[key]:
            try:
                dados[key] = float(dados[key]) if key != 'eixo_od' and key != 'eixo_oe' else int(dados[key])
            except ValueError:
                dados[key] = None
    
    conn = conectar_banco()
    
    try:
        receita_id = inserir_receita(conn, dados)
        print(f"\nReceita inserida com sucesso! ID: {receita_id}")
    
    except Exception as e:
        print(f"Erro ao inserir receita: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def inserir_usuario_interativo():
    """Interface interativa para inserir um usuário"""
    
    print("\n=== Inserir Novo Usuário ===")
    
    dados = {}
    dados['username'] = input("Nome de usuário: ")
    dados['password'] = input("Senha: ")
    
    print("Roles disponíveis:")
    print("1. adm (Administrador)")
    print("2. medico (Médico)")
    print("3. atendente (Atendente)")
    
    role_opcao = input("Escolha o role (1-3): ")
    
    if role_opcao == "1":
        dados['role'] = 'adm'
    elif role_opcao == "2":
        dados['role'] = 'medico'
    else:
        dados['role'] = 'atendente'
    
    conn = conectar_banco()
    
    try:
        user_id = inserir_usuario(conn, dados)
        print(f"\nUsuário inserido com sucesso! ID: {user_id}")
    
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--exemplo":
            print("Inserindo dados de exemplo...")
            exemplo_insercao_receitas()
            exemplo_insercao_usuarios()
            print("Concluído!")
        else:
            print("Uso: python inserir_dados.py [--exemplo]")
    else:
        inserir_dados_interativo()

