DOCUMENTAÇÃO DO SISTEMA DE ASSISTÊNCIA TÉCNICA

Este documento detalha a arquitetura, funcionalidades e configurações técnicas do software de gestão de Assistência Técnica desenvolvido em Django.

    1. Visão Geral do Projeto

        O sistema tem como objetivo centralizar o fluxo de trabalho de uma oficina, permitindo o registro de clientes, o controle de seus equipamentos e o acompanhamento de Ordens de Serviço (O.S.) desde a abertura até a finalização ou cancelamento.

    2. Arquitetura e Tecnologias

        O software utiliza o padrão de projeto MVT (Model-Template-View).

        Linguagem: Python 3.13

        Framework Web: Django 6.0

        Interface: Bootstrap 5 (CSS/JS via CDN)

        Banco de Dados: SQLite3 (Embutido)

        Ambiente Virtual: venv (Ambiente Isolado)

    3. Estrutura de Modelagem (Banco de Dados)

    3.1. Clientes

        Armazena as informações de contato do proprietário.

        Campos: Nome, Telefone, E-mail, Endereço.

    3.2. Equipamentos

        Registra os dispositivos vinculados a um cliente (Relacionamento 1:N).

        Campos: Cliente (FK), Tipo, Marca, Modelo, Número de Série.

    3.3. Ordens de Serviço

        Controla o processo de manutenção (Relacionamento 1:N com Equipamento).

        Campos: Cliente, Equipamento, Descrição do Problema, Diagnóstico Técnico, Valor, Status (Pendente, Finalizado, Cancelado).

    4. Funcionalidades Detalhadas

    4.1. Controle de Acesso

        Todas as páginas internas estão protegidas pelo decorador @login_required. O sistema redireciona automaticamente usuários não autenticados para a tela de login.

    4.2. Tela de Login Customizada

        O formulário de login foi modificado em forms.py para:

        Incluir classes de estilização do Bootstrap.

        Preencher automaticamente os campos de Usuário e Senha com o valor adm para facilitar o acesso em ambiente de desenvolvimento.

        Alinhamento horizontal de campos usando o sistema de Grid do Bootstrap.

    4.3. Gestão de Fluxo

        Criação: Formulários otimizados para captura de dados.

        Finalização/Cancelamento: Funções rápidas na views.py que alteram o status do registro no banco de dados através de ordem.save().

    5. Estrutura de Rotas (URLs)
    
        O mapeamento de URLs do sistema conecta as requisições do navegador às funções de lógica (Views). Abaixo estão os principais endereços configurados:

    Autenticação e Acesso

        /login/: Utiliza a LoginView nativa do Django com formulário customizado para realizar a autenticação do usuário.

        /logout/: Encerra a sessão atual e redireciona o usuário para a tela de login.

    Painel e Gestão

        /: Rota principal que aciona a view dashboard, apresentando o resumo das atividades da oficina.

        /clientes/: Aciona a view clientes, responsável por listar todos os proprietários cadastrados no banco de dados.

        /clientes/novo/: Rota para o formulário de cadastro de novos clientes via método POST.

        /equipamentos/: Exibe a lista de todos os aparelhos e dispositivos registrados.

    Operações de Ordem de Serviço

        /ordens/: Central de controle que lista todas as O.S. (Ordens de Serviço).

        /finalizar/<id>/: Rota dinâmica que recebe o ID da ordem e altera seu status para "Finalizado".

        /cancelar/<id>/: Rota dinâmica que recebe o ID da ordem e altera seu status para "Cancelado".

    6. Configurações de Desenvolvimento

        Ativação do Ambiente (Windows)

        PowerShell

        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

        .\venv\Scripts\activate

    Comandos de Manutenção

        Migrações: python manage.py makemigrations e python manage.py migrate

        Execução: python manage.py runserver

        Novo Admin: python manage.py createsuperuser

    7. Notas de Estilização

        A interface utiliza o arquivo base.html como template pai, garantindo que o cabeçalho, navegação e rodapé sejam consistentes em todas as páginas do sistema.