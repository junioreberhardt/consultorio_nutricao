from app import app
from models import db, Usuario

with app.app_context():
    print("Destruindo estruturas antigas...")
    db.drop_all()
    
    print("Criando novas tabelas granulares no SQLite3...")
    db.create_all()
    
    print("Inserindo admin como Administrador Geral do Sistema...")
    admin = Usuario(
        nome='Administrador do Sistema', 
        nome_usuario='admin', 
        email='admin@admin.com',
        senha='123', 
        cargo='Administrador',
        ativo=True,
        pode_cadastrar_paciente=True,
        pode_montar_cardapio=True,
        pode_ver_financeiro=True       # Apenas você tem esse acesso
    )
    db.session.add(admin)
    db.session.commit()
    
    print("--- BANCO CONFIGURADO COM SUCESSO! ---")
