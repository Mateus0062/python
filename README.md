# 🔐 Sistema de Gerenciamento de Usuários com Segurança Avançada

Um sistema robusto de autenticação e gerenciamento de usuários em Python, implementando as melhores práticas de segurança e desenvolvimento de software.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

## 📋 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Documentação Detalhada](#-documentação-detalhada)
- [Exemplos Avançados](#-exemplos-avançados)
- [Segurança](#-segurança)
- [Arquitetura](#-arquitetura)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

### 🛡️ Segurança de Classe Mundial

- **Criptografia BCrypt**: Hash de senhas com salt usando bcrypt (12 rounds)
- **Validação de Email**: Verificação completa usando `email-validator`
- **Requisitos de Senha Configuráveis**: 
  - Tamanho mínimo/máximo
  - Letras maiúsculas e minúsculas
  - Números
  - Caracteres especiais
- **Proteção contra Ataques Comuns**: Prevenção de força bruta e rainbow tables

### 🏗️ Arquitetura Sólida

- **Princípios SOLID**: Código modular e de fácil manutenção
- **Single Responsibility**: Cada classe tem uma responsabilidade única
- **Type Hints**: Código totalmente tipado para melhor IDE support
- **Exceções Customizadas**: Tratamento de erros específico e informativo
- **Validação Abrangente**: Coleta todos os erros de uma vez para melhor UX

### 🔧 Flexibilidade

- **Requisitos Customizáveis**: Adapte as regras de senha conforme necessário
- **Injeção de Dependência**: Fácil de testar e estender
- **Configuração Centralizada**: Modifique comportamentos sem alterar código

## 📦 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Dependências

```txt
bcrypt>=4.0.0
email-validator>=2.0.0
```

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/sistema-usuarios.git
cd sistema-usuarios
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute os testes

```bash
python user_system.py
```

## 💡 Uso Rápido

### Criar um Usuário

```python
from user_system import User

# Criar usuário com validação automática
usuario = User(
    name="João Silva",
    email="joao@email.com",
    password="Senha@123"
)

print(usuario)  # João Silva (joao@email.com)
```

### Verificar Senha

```python
# Autenticar usuário
if usuario.verificar_senha("Senha@123"):
    print("✅ Login bem-sucedido!")
else:
    print("❌ Senha incorreta!")
```

### Alterar Senha

```python
try:
    usuario.alterar_senha(
        senha_antiga="Senha@123",
        senha_nova="NovaSenha@456"
    )
    print("✅ Senha alterada com sucesso!")
except SenhaInvalidaError as e:
    print(f"❌ {e}")
```

## 📖 Documentação Detalhada

### Classes Principais

#### 🔹 `User`

Classe principal que representa um usuário do sistema.

**Atributos:**
- `name` (str): Nome do usuário
- `email` (str): Email validado e normalizado
- `_password_hash` (bytes): Hash bcrypt da senha (privado)

**Métodos:**

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `__init__(name, email, password, validador_senha?)` | Cria novo usuário | `User` |
| `verificar_senha(senha_digitada)` | Verifica se senha está correta | `bool` |
| `alterar_senha(senha_antiga, senha_nova)` | Altera senha do usuário | `bool` |

**Exemplo:**
```python
usuario = User("Maria", "maria@email.com", "Senha@123")
```

---

#### 🔹 `ValidadorSenha`

Valida senhas contra requisitos configuráveis.

**Métodos:**

```python
def validar(self, senha: str) -> tuple[bool, list[str]]:
    """
    Valida senha e retorna status + lista de erros.
    
    Returns:
        tuple: (é_válida, lista_de_erros)
    """
```

**Exemplo:**
```python
validador = ValidadorSenha()
is_valida, erros = validador.validar("abc123")

if not is_valida:
    for erro in erros:
        print(f"❌ {erro}")
```

**Saída:**
```
❌ Senha deve conter no mínimo 8 caracteres
❌ Senha deve conter pelo menos uma letra MAIÚSCULA
❌ Senha deve conter pelo menos um caractere especial (!@#$%^&*()_+-=[]{}|;:,.<>?)
```

---

#### 🔹 `RequisitosSeguranca`

Configuração centralizada dos requisitos de segurança.

**Atributos:**

| Atributo | Padrão | Descrição |
|----------|--------|-----------|
| `TAMANHO_MINIMO` | 8 | Comprimento mínimo da senha |
| `TAMANHO_MAXIMO` | 128 | Comprimento máximo da senha |
| `REQUER_MAIUSCULA` | True | Exige letra maiúscula |
| `REQUER_MINUSCULA` | True | Exige letra minúscula |
| `REQUER_NUMERO` | True | Exige pelo menos um número |
| `REQUER_ESPECIAL` | True | Exige caractere especial |
| `CARACTERES_ESPECIAIS` | "!@#$%..." | Caracteres aceitos |

---

#### 🔹 `ValidadorEmail`

Valida e normaliza endereços de email.

**Métodos:**

```python
@staticmethod
def validar(email: str) -> str:
    """Valida email usando email-validator"""
```

---

#### 🔹 `CriptografiaSenha`

Responsável pela criptografia e verificação de senhas.

**Métodos:**

```python
@staticmethod
def criptografar(senha: str) -> bytes:
    """Criptografa senha com bcrypt (12 rounds)"""

@staticmethod
def verificar(senha_digitada: str, senha_hash: bytes) -> bool:
    """Verifica senha contra hash"""
```

---

### Exceções Customizadas

#### `SenhaInvalidaError`
Lançada quando a senha não atende aos requisitos.

```python
try:
    usuario = User("João", "joao@email.com", "123")
except SenhaInvalidaError as e:
    print(e)
```

#### `EmailInvalidoError`
Lançada quando o email é inválido.

```python
try:
    usuario = User("João", "email_invalido", "Senha@123")
except EmailInvalidoError as e:
    print(e)
```

## 🎯 Exemplos Avançados

### 1. Requisitos de Senha Customizados

```python
from user_system import User, ValidadorSenha, RequisitosSeguranca

# Criar requisitos mais flexíveis
requisitos_simples = RequisitosSeguranca(
    TAMANHO_MINIMO=6,
    TAMANHO_MAXIMO=20,
    REQUER_ESPECIAL=False,  # Não exige caractere especial
    REQUER_MAIUSCULA=False
)

# Criar validador customizado
validador = ValidadorSenha(requisitos_simples)

# Usar no usuário
usuario = User(
    "Pedro",
    "pedro@email.com",
    "senha123",  # Válida com requisitos flexíveis
    validador_senha=validador
)
```

### 2. Sistema de Login Completo

```python
class SistemaLogin:
    def __init__(self):
        self.usuarios = {}
    
    def registrar(self, name: str, email: str, password: str):
        """Registra novo usuário"""
        try:
            usuario = User(name, email, password)
            self.usuarios[email] = usuario
            return True, "Usuário criado com sucesso!"
        except (SenhaInvalidaError, EmailInvalidoError) as e:
            return False, str(e)
    
    def autenticar(self, email: str, password: str):
        """Autentica usuário"""
        usuario = self.usuarios.get(email)
        
        if not usuario:
            return False, "Usuário não encontrado"
        
        if usuario.verificar_senha(password):
            return True, f"Bem-vindo, {usuario.name}!"
        
        return False, "Senha incorreta"


# Uso
sistema = SistemaLogin()

# Registrar
sucesso, msg = sistema.registrar("Ana", "ana@email.com", "Ana@2024")
print(msg)

# Login
sucesso, msg = sistema.autenticar("ana@email.com", "Ana@2024")
print(msg)  # Bem-vindo, Ana!
```

### 3. Validação em Formulários Web

```python
from flask import Flask, request, jsonify
from user_system import User, SenhaInvalidaError, EmailInvalidoError

app = Flask(__name__)

@app.route('/registrar', methods=['POST'])
def registrar():
    dados = request.json
    
    try:
        usuario = User(
            dados['name'],
            dados['email'],
            dados['password']
        )
        
        # Salvar no banco de dados aqui
        
        return jsonify({
            'success': True,
            'message': 'Usuário criado com sucesso!'
        }), 201
        
    except SenhaInvalidaError as e:
        return jsonify({
            'success': False,
            'errors': str(e).split('\n')
        }), 400
        
    except EmailInvalidoError as e:
        return jsonify({
            'success': False,
            'errors': [str(e)]
        }), 400
```

### 4. Integração com Banco de Dados

```python
import sqlite3
from user_system import User, CriptografiaSenha

class UsuarioDB:
    def __init__(self, db_path='usuarios.db'):
        self.conn = sqlite3.connect(db_path)
        self.criar_tabela()
    
    def criar_tabela(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def salvar(self, usuario: User):
        """Salva usuário no banco"""
        self.conn.execute(
            'INSERT INTO usuarios (name, email, password_hash) VALUES (?, ?, ?)',
            (usuario.name, usuario.email, usuario._password_hash)
        )
        self.conn.commit()
    
    def buscar_por_email(self, email: str):
        """Busca usuário por email"""
        cursor = self.conn.execute(
            'SELECT name, email, password_hash FROM usuarios WHERE email = ?',
            (email,)
        )
        row = cursor.fetchone()
        
        if row:
            # Reconstruir objeto User (simplificado)
            # Na prática, você criaria um método from_db
            return row
        return None
```

## 🔒 Segurança

### Práticas Implementadas

✅ **Hash de Senhas com BCrypt**
- 12 rounds de hashing (mais seguro que o padrão de 10)
- Salt único para cada senha
- Resistente a ataques de força bruta e rainbow tables

✅ **Validação Robusta de Email**
- Verificação de formato RFC compliant
- Normalização automática
- Prevenção de emails malformados

✅ **Requisitos de Senha Fortes (OWASP)**
- Mínimo de 8 caracteres (padrão OWASP)
- Combinação de maiúsculas, minúsculas, números e especiais
- Previne senhas comuns e fracas

✅ **Proteção de Dados Sensíveis**
- Senha armazenada como atributo privado (`_password_hash`)
- Nunca armazena senhas em texto plano
- Sem logs de senhas

### ⚠️ Recomendações de Produção

Ao usar em produção, considere adicionar:

1. **Rate Limiting**: Limite tentativas de login
2. **Auditoria**: Log de tentativas de acesso
3. **2FA**: Autenticação de dois fatores
4. **Recuperação de Senha**: Sistema de reset por email
5. **Sessões**: Gerenciamento de tokens JWT ou similar
6. **HTTPS**: Sempre use conexões criptografadas
7. **Proteção CSRF**: Para formulários web

## 🏛️ Arquitetura

### Diagrama de Classes

```
┌─────────────────────────┐
│   RequisitosSeguranca   │
│   (Dataclass)           │
└───────────┬─────────────┘
            │
            │ usa
            ▼
┌─────────────────────────┐
│   ValidadorSenha        │
│   ─────────────────     │
│   + validar()           │
└─────────────────────────┘
            │
            │ usa
            ▼
┌─────────────────────────┐         ┌──────────────────┐
│   User                  │◄────────│ ValidadorEmail   │
│   ─────────────────     │         └──────────────────┘
│   + name                │
│   + email               │         ┌──────────────────┐
│   - _password_hash      │◄────────│CriptografiaSenha│
│   ─────────────────     │         └──────────────────┘
│   + verificar_senha()   │
│   + alterar_senha()     │
└─────────────────────────┘
```

### Princípios SOLID Aplicados

- **S**ingle Responsibility: Cada classe tem uma única razão para mudar
- **O**pen/Closed: Aberto para extensão (requisitos customizados), fechado para modificação
- **L**iskov Substitution: Pode substituir ValidadorSenha por implementações customizadas
- **I**nterface Segregation: Interfaces mínimas e específicas
- **D**ependency Inversion: User depende de abstrações (ValidadorSenha injetável)

## 🧪 Testes

### Executar Testes Integrados

```bash
python user_system.py
```

### Exemplo de Teste Unitário

```python
import unittest
from user_system import ValidadorSenha, RequisitosSeguranca

class TestValidadorSenha(unittest.TestCase):
    def setUp(self):
        self.validador = ValidadorSenha()
    
    def test_senha_valida(self):
        is_valida, erros = self.validador.validar("Senha@123")
        self.assertTrue(is_valida)
        self.assertEqual(len(erros), 0)
    
    def test_senha_muito_curta(self):
        is_valida, erros = self.validador.validar("Ab1!")
        self.assertFalse(is_valida)
        self.assertIn("no mínimo", erros[0])
    
    def test_senha_sem_maiuscula(self):
        is_valida, erros = self.validador.validar("senha@123")
        self.assertFalse(is_valida)
        self.assertTrue(any("MAIÚSCULA" in e for e in erros))

if __name__ == '__main__':
    unittest.main()
```

## 📊 Comparação com Outras Soluções

| Característica | Este Sistema | Django Auth | Flask-Login | Passport.js |
|----------------|--------------|-------------|-------------|-------------|
| Linguagem | Python | Python | Python | JavaScript |
| BCrypt Nativo | ✅ | ✅ | ❌ | ✅ |
| Validação Email | ✅ | ❌ | ❌ | ❌ |
| Type Hints | ✅ | Parcial | ❌ | N/A |
| Requisitos Customizáveis | ✅ | ❌ | ❌ | ✅ |
| Standalone | ✅ | ❌ | ❌ | ❌ |
| SOLID Principles | ✅ | Parcial | ❌ | Parcial |

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes de Código

- Siga PEP 8
- Adicione type hints
- Documente funções com docstrings
- Escreva testes para novas features
- Mantenha cobertura de testes > 80%

## 📝 Changelog

### [1.0.0] - 2024-03-16

#### Adicionado
- Sistema completo de gerenciamento de usuários
- Validação de email com email-validator
- Validação de senha com requisitos configuráveis
- Criptografia BCrypt com 12 rounds
- Exceções customizadas
- Type hints completos
- Documentação abrangente

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento Inicial* - [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- [OWASP](https://owasp.org/) - Por diretrizes de segurança
- [bcrypt](https://github.com/pyca/bcrypt/) - Por excelente implementação de hash
- [email-validator](https://github.com/JoshData/python-email-validator) - Por validação robusta

## 📧 Contato

Tem dúvidas ou sugestões? Entre em contato:

- Email: seu-email@example.com
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)
- GitHub Issues: [Criar Issue](https://github.com/seu-usuario/sistema-usuarios/issues)

---

<div align="center">

**Feito com ❤️ e Python**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-First-red?style=for-the-badge&logo=security&logoColor=white)](https://owasp.org/)

</div>
