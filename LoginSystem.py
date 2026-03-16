from email_validator import validate_email, EmailNotValidError
import bcrypt
from typing import Optional
from dataclasses import dataclass
import re

class SenhaInvalidaError(Exception):
    pass

class EmailInvalidoError(Exception): 
    pass

@dataclass
class RequisitosSeguranca:
    TAMANHO_MINIMO: int = 8  
    TAMANHO_MAXIMO: int = 128 
    REQUER_MAIUSCULA: bool = True
    REQUER_MINUSCULA: bool = True
    REQUER_NUMERO: bool = True
    REQUER_ESPECIAL: bool = True
    CARACTERES_ESPECIAIS: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"

class ValidadordeSenha:
    def __init__(self, requisitos: RequisitosSeguranca = None):
        self.requisitos = requisitos or RequisitosSeguranca()

    def validar(self, senha: str) -> tuple[bool, list[str]]:
        erros = []

        # Validar comprimento da Senha
        if len(senha) < self.requisitos.TAMANHO_MINIMO:
            # adiciona no vetor de erros
            erros.append(
                f"Senha deve conter no mínimo {self.requisitos.TAMANHO_MINIMO} caracteres"
            )
        
        if len(senha) > self.requisitos.TAMANHO_MAXIMO:
            # adiciona no vetor de erros
            erros.append(
                f"Senha deve conter no máximo {self.requisitos.TAMANHO_MAXIMO} caracteres"
            )
        
        # Validar requisitos de caracteres
        if self.requisitos.REQUER_MAIUSCULA and not any(c.isupper() for c in senha):
            erros.append("Senha deve conter pelo menos uma letra Maiuscula")

        if self.requisitos.REQUER_MINUSCULA and not any(c.islower() for c in senha):
            erros.append("Senha deve conter pelo menos uma letra Minuscula")

        if self.requisitos.REQUER_NUMERO and not any(c.isdigit() for c in senha):
            erros.append("Senha deve conter pelo menos um numero")
        
        if self.requisitos.REQUER_ESPECIAL:
            if not any(c in self.requisitos.CARACTERES_ESPECIAIS for c in senha):
                erros.append(
                    f"A senha deve conter pelo menos um caractere especial ({self.requisitos.CARACTERES_ESPECIAIS})"
                )
        
        return len(erros) == 0, erros

class ValidadorEmail:
    def validar(email: str) -> str:
        try:
            info = validate_email(email, check_deliverability=False)
            return info.normalized
        except EmailNotValidError as e:
            raise EmailInvalidoError(f"Email inválido: {str(e)}")

class CriptografarSenha:
    def cripto(senha: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(senha.encode('utf-8'), salt)

    def verificar(senha_digitada: str, senha_hash: bytes) -> bool:        
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash)
    
class User:
    def __init__(self, name: str, email: str, password: str, validador_senha: Optional[ValidadordeSenha] = None):
        if not name or not name.strip():
            raise ValueError("Nome não pode ser vazio")
        
        self.name = name.strip();
        self.email = ValidadorEmail.validar(email)
        self._validador_senha = validador_senha or ValidadordeSenha()
        self._password_hash = self._processar_senha(password)
    
    def _processar_senha(self, senha: str) -> bytes:
        is_valida, erros = self._validador_senha.validar(senha)

        if not is_valida:
            mensagem_erro = "Senha inválida:\n" + "\n".join(f" * {erro}" for erro in erros)
            raise SenhaInvalidaError(mensagem_erro)
        
        return CriptografarSenha.cripto(senha)

    def verificar_senha(self, senha_digitada: str) -> bool:
        return CriptografarSenha.verificar(senha_digitada, self._password_hash)
    
    def alterar_senha(self, senha_antiga: str, senha_nova: str) -> bool:
        if not self.verificar_senha(senha_antiga):
            raise SenhaInvalidaError("Senha antiga incorreta")

        self._password_hash = self._processar_senha(senha_nova)
        return True
    
    def __repr__(self) -> str:
        return f"User(name='{self.name}', email='{self.email}')"

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.email == other.email
    
# ===== Exemplos de Uso =====
def testar_sistema():
    """Função para testar o sistema de usuários"""
    print("=" * 70)
    print("TESTANDO SISTEMA DE USUÁRIOS")
    print("=" * 70)
    
    # Teste 1: Usuário válido
    print("\n1 - Criando usuário válido:")
    try:
        usuario1 = User("João Silva", "joao@email.com", "Senha@123")
        print(f"{usuario1} criado com sucesso!")
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"Erro: {e}")
    
    # Teste 2: Email inválido
    print("\n2 - Tentando criar com email inválido:")
    try:
        usuario2 = User("Maria", "email_invalido", "Senha@123")
        print(f"{usuario2} criado com sucesso!")
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"Erro: {e}")
    
    # Teste 3: Senha sem caractere especial
    print("\n3 - Tentando criar com senha sem caractere especial:")
    try:
        usuario3 = User("Pedro", "pedro@email.com", "Senha123")
        print(f"{usuario3} criado com sucesso!")
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"{e}")
    
    # Teste 4: Senha muito curta
    print("\n4 - Tentando criar com senha muito curta:")
    try:
        usuario4 = User("Ana", "ana@email.com", "Se1!")
        print(f"{usuario4} criado com sucesso!")
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"{e}")
    
    # Teste 5: Verificar e alterar senha
    print("\n5 - Testando verificação e alteração de senha:")
    try:
        usuario5 = User("Carlos", "carlos@email.com", "Teste@123")
        print(f"{usuario5} criado com sucesso!")
        
        print("\n   Verificando senhas:")
        print(f"   Senha 'Teste@123': {usuario5.verificar_senha('Teste@123')}")
        print(f"   Senha 'SenhaErrada': {usuario5.verificar_senha('SenhaErrada')}")
        
        print("\n   Alterando senha:")
        usuario5.alterar_senha("Teste@123", "NovaSenha@456")
        print("    Senha alterada com sucesso!")
        print(f"   Nova senha funciona: {usuario5.verificar_senha('NovaSenha@456')}")
        
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"Erro: {e}")
    
    # Teste 6: Requisitos customizados
    print("\n6 - Criando usuário com requisitos customizados:")
    try:
        requisitos_simples = RequisitosSeguranca(
            TAMANHO_MINIMO=6,
            TAMANHO_MAXIMO=20,
            REQUER_ESPECIAL=False  # Não requer especial
        )
        validador_custom = ValidadordeSenha(requisitos_simples)
        
        usuario6 = User(
            "Diana", 
            "diana@email.com", 
            "Senha123",  # Sem caractere especial, mas válido
            validador_senha=validador_custom
        )
        print(f"{usuario6} criado com requisitos customizados!")
        
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"Erro: {e}")
    
    # Teste 7: Nome vazio
    print("\n7 - Tentando criar com nome vazio:")
    try:
        usuario7 = User("   ", "teste@email.com", "Senha@123")
        print(f"{usuario7} criado com sucesso!")
    except (EmailInvalidoError, SenhaInvalidaError, ValueError) as e:
        print(f"Erro: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    testar_sistema()