from email_validator import validate_email, EmailNotValidError
import bcrypt

class User: 
    def __init__(self, name, email, password):
        self.name = name
        
        email_validado = self.verificarEmail(email)
        
        if email_validado.startswith("The email addres"):
            raise ValueError(f"Email inválido: {email_validado}")
        self.email = email_validado
        
        senha_criptografada = self.verificareCriptografarSenha(password)
        if senha_criptografada is None:
            raise ValueError("senha não atende aos requisitos")
        self.password = senha_criptografada
    
    def verificarEmail(self, email): 
        # verificar email
        try:
            info = validate_email(email, check_deliverability=False)
            return info.normalized
        except EmailNotValidError as e:
            return str(e)
        
    def verificareCriptografarSenha(self, password):
        # verificar senha
        if len(password) < 6:
            print("Senha deve conter no mínimo 6 caracteres")
            return None
        elif len(password) > 10:
            print("Deve conter no máximo 10 caracteres")
            return None
        
        tem_maiuscula = any(x.isupper() for x in password)
        tem_minuscula = any(x.islower() for x in password)
        tem_numero = any(x.isdigit() for x in password)

        if not tem_maiuscula:
            print("A senha deve conter pelo menos uma letra maiuscula")
            return None
        
        if not tem_minuscula:
            print("A senha dever conter pelo menos uma letra minuscula")
            return None
        
        if not tem_numero:
            print("A senha deve conter pelo menos um número")
            return None
        
        # se senha ok, criptografar
        print("Senha válida! Criptografando...")
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # retornar senha criptografada
        return senha_hash
    
    def verificarSenha(self, senha_digitada):
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), self.password)    