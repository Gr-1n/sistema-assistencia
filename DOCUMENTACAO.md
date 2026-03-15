# 📚 Documentação Técnica
## Sistema de Assistência Técnica

Esta documentação descreve a arquitetura, funcionamento e componentes do sistema **Sistema de Assistência Técnica**, desenvolvido em **Python utilizando o framework Django**.

O sistema permite gerenciar clientes, equipamentos e ordens de serviço de uma assistência técnica, além de gerar documentos em PDF e acompanhar o status das manutenções.

---

# 📌 1. Visão Geral do Sistema

O sistema foi desenvolvido para auxiliar empresas ou técnicos que realizam manutenção de equipamentos eletrônicos ou informáticos.

Ele permite:

- Cadastro de clientes
- Registro de equipamentos
- Controle de ordens de serviço
- Atualização de status da manutenção
- Geração de ordem de serviço em PDF
- Dashboard com indicadores do sistema

O sistema possui autenticação de usuários, garantindo que apenas pessoas autorizadas possam acessar e modificar as informações.

---

# 🏗 2. Arquitetura do Projeto

O projeto segue a arquitetura padrão do framework **Django**, baseada no padrão **MVT (Model – View – Template)**.

### Model
Responsável pela estrutura dos dados e comunicação com o banco de dados.

### View
Responsável pela lógica de negócio do sistema.

### Template
Responsável pela interface visual do sistema.

---

# 📂 3. Estrutura do Projeto


sistema-assistencia
│
├── assistencia_tecnica
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── oficina
│ ├── migrations
│ ├── templates
│ │ └── oficina
│ │ ├── dashboard.html
│ │ ├── clientes.html
│ │ ├── equipamentos.html
│ │ ├── ordens.html
│ │ ├── novo_cliente.html
│ │ ├── novo_equipamento.html
│ │ └── nova_ordem.html
│ │
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── tests.py
│
├── static
│
├── manage.py
└── requirements.txt


---

# 🧱 4. Modelagem de Dados

O sistema possui três modelos principais:

- Cliente
- Equipamento
- OrdemServico

---

### 👤 4.1 Modelo Cliente

Representa os clientes da assistência técnica.

### Campos

| Campo | Tipo | Descrição |
|------|------|-----------|
| nome | CharField | Nome do cliente |
| telefone | CharField | Telefone para contato |
| email | EmailField | Email do cliente |
| endereco | CharField | Endereço do cliente |

### Exemplo de modelo

```python
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=200)
```

### 💻 4.2 Modelo Equipamento

Representa os equipamentos cadastrados no sistema.

Cada equipamento pertence a um cliente.

### Campos

| Campo | Tipo | Descrição |
|------|------|-----------|
| cliente |	ForeignKey | Cliente dono do equipamento
| tipo | CharField | Tipo do equipamento
| marca | CharField | Marca
| modelo | CharField | Modelo
| numero_serie | CharField | Número de série

### Exemplo

```python
class Equipamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
```

### 🧾 4.3 Modelo Ordem de Serviço

Representa o registro de manutenção de um equipamento.

### Campos

| Campo | Tipo | Descrição |
|------|------|-----------|
| cliente |	ForeignKey | Cliente responsável
| equipamento |	ForeignKey | Equipamento em manutenção
| problema | TextField | Problema informado
| diagnostico |	TextField |	Diagnóstico técnico
| valor | DecimalField | Valor do serviço
| status | CharField | Status da ordem

# 🔄 5. Fluxo de Status das Ordens

As ordens de serviço possuem um fluxo de status:

Recebido

↓

Diagnóstico

↓

Aguardando aprovação

↓

Reparo

↓

Finalizado

Também existe o status:

Cancelado

# 📊 6. Dashboard

O dashboard apresenta indicadores importantes do sistema.

São exibidas informações como:

- Total de clientes

- Total de ordens de serviço

- Quantidade de ordens por status

Essas informações são obtidas através de consultas no banco de dados utilizando o ORM do Django.

Exemplo:

```python
total_os = OrdemServico.objects.count()
recebidos = OrdemServico.objects.filter(status="recebido").count()
```

# 👥 7. Gestão de Clientes

O sistema permite:

- Cadastrar novos clientes

- Listar clientes cadastrados

- Editar informações

- Excluir clientes

Essas operações são realizadas através das views:

- novo_cliente

- clientes

- editar_cliente

- excluir_cliente

# 🖥 8. Gestão de Equipamentos

Cada cliente pode possuir vários equipamentos cadastrados.

Funcionalidades disponíveis:

- Cadastro de equipamento

- Listagem

- Edição

- Exclusão

# 🧾 9. Gestão de Ordens de Serviço

Permite registrar manutenções realizadas em equipamentos.

As ordens registram:

- Cliente

- Equipamento

- Problema relatado

- Diagnóstico

- Valor do serviço

- Status

Também é possível:

- Finalizar ordem

- Cancelar ordem

# 📄 10. Geração de PDF

O sistema gera um documento PDF da ordem de serviço utilizando a biblioteca ReportLab.

O PDF contém:

- Número da ordem

- Dados do cliente

- Dados do equipamento

- Problema relatado

- Diagnóstico

- Valor do serviço

- Assinaturas

- Usuário que emitiu o documento

- Data e hora de emissão

Exemplo de criação do PDF:

```python
p = canvas.Canvas(response, pagesize=A4)
p.drawString(100, 750, "Ordem de Serviço")
```

# 🔐 11. Autenticação

O sistema utiliza o sistema de autenticação padrão do Django.

Todas as páginas principais são protegidas pelo decorator:

```python
@login_required
```

Isso garante que apenas usuários autenticados tenham acesso ao sistema.

# ⚙️ 12. Banco de Dados

O projeto utiliza o banco de dados SQLite, padrão do Django.

Ele é suficiente para aplicações pequenas ou para desenvolvimento.

Para ambientes de produção recomenda-se:

- PostgreSQL

- MySQL

# 🚀 13. Execução do Sistema

Passos para executar o projeto:

Clonar repositório

```python
git clone https://github.com/Gr-1n/sistema-assistencia.git
```

Criar ambiente virtual

```python
python -m venv venv
```

Ativar ambiente

- Windows:

```python
venv\Scripts\activate
```

- Linux/Mac:

```python
source venv/bin/activate
```

Instalar dependências

```python
pip install -r requirements.txt
```

Aplicar migrações

```python
python manage.py migrate
```

Criar superusuário

```python
python manage.py createsuperuser
```

Executar servidor

```python
python manage.py runserver
```

# 📈 14. Possíveis Melhorias

O sistema pode ser expandido com diversas melhorias:

- API REST com Django Rest Framework

- Upload de fotos do equipamento

- Cadastro de técnicos

- Histórico de manutenção

- Notificações por email

- Busca avançada

- Relatórios

- Dashboard com gráficos

# 👨‍💻 15. Autor

Projeto desenvolvido por:

**Lucas Tavares Sgrinier**

GitHub:
https://github.com/Gr-1n