from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Equipamento, OrdemServico
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from reportlab.platypus import Table, TableStyle

@login_required
def dashboard(request):
    # 1. Captura os dados da busca
    busca = request.GET.get('busca')
    filtro = request.GET.get('filtro')

    # 2. Prepara o contexto base (contadores)
    context = {
        "total_os": OrdemServico.objects.count(),
        "total_clientes": Cliente.objects.count(),
        "recebidos": OrdemServico.objects.filter(status="recebido").count(),
        "diagnostico": OrdemServico.objects.filter(status="diagnostico").count(),
        "aprovacao": OrdemServico.objects.filter(status="aprovacao").count(),
        "reparo": OrdemServico.objects.filter(status="reparo").count(),
        "finalizados": OrdemServico.objects.filter(status="finalizado").count(),
        "filtro_selecionado": filtro  # Isso faz o filtro "travar" na última escolha
    }

    # 3. Lógica de busca e redirecionamento
    if busca:
        if filtro == 'cliente':
            clientes = Cliente.objects.filter(nome__icontains=busca)
            if not clientes.exists():
                messages.error(request, f'Cliente "{busca}" não encontrado.')
                return render(request, 'oficina/dashboard.html', context)
            return render(request, 'oficina/clientes.html', {'clientes': clientes})

        elif filtro == 'serie':
            equipamentos = Equipamento.objects.filter(numero_serie__icontains=busca)
            if not equipamentos.exists():
                messages.error(request, f'Equipamento com série "{busca}" não encontrado.')
                return render(request, 'oficina/dashboard.html', context)
            return render(request, 'oficina/equipamentos.html', {'equipamentos': equipamentos})

        elif filtro == 'id':
            if busca.isdigit():
                ordens = OrdemServico.objects.filter(id=busca)
                if not ordens.exists():
                    messages.error(request, f'O.S. #{busca} não encontrada.')
                    return render(request, 'oficina/dashboard.html', context)
                return render(request, 'oficina/ordens.html', {'ordens': ordens})
            else:
                messages.error(request, "O filtro por ID aceita apenas números.")
                return render(request, 'oficina/dashboard.html', context)

    # Se não houver busca, renderiza o dashboard normal
    return render(request, 'oficina/dashboard.html', context)

    context = {
        "total_os": OrdemServico.objects.count(),
        "total_clientes": Cliente.objects.count(),
        "recebidos": OrdemServico.objects.filter(status="recebido").count(),
        "diagnostico": OrdemServico.objects.filter(status="diagnostico").count(),
        "aprovacao": OrdemServico.objects.filter(status="aprovacao").count(),
        "reparo": OrdemServico.objects.filter(status="reparo").count(),
        "finalizados": OrdemServico.objects.filter(status="finalizado").count()
    }

    return render(request, 'oficina/dashboard.html', context)

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'oficina/clientes.html', {'clientes': clientes})

@login_required
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        cliente.nome = request.POST.get("nome")
        cliente.telefone = request.POST.get("telefone")
        cliente.email = request.POST.get("email")
        cliente.endereco = request.POST.get("endereco")
        cliente.save()

        return redirect("clientes")

    return render(request, "oficina/editar_cliente.html", {"cliente": cliente})

@login_required
def excluir_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()

    return redirect("clientes")

@login_required
def equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'oficina/equipamentos.html', {'equipamentos': equipamentos})

@login_required
def editar_equipamento(request, id):

    equipamento = get_object_or_404(Equipamento, id=id)

    if request.method == "POST":

        equipamento.cliente_id = request.POST.get("cliente")
        equipamento.tipo = request.POST.get("tipo")
        equipamento.marca = request.POST.get("marca")
        equipamento.modelo = request.POST.get("modelo")
        equipamento.numero_serie = request.POST.get("numero_serie")

        equipamento.save()

        return redirect("equipamentos")

    clientes = Cliente.objects.all()

    return render(request, "oficina/editar_equipamento.html", {
        "equipamento": equipamento,
        "clientes": clientes
    })

@login_required
def excluir_equipamento(request, id):

    equipamento = get_object_or_404(Equipamento, id=id)
    equipamento.delete()

    return redirect("equipamentos")

@login_required
def ordens(request):
    ordens = OrdemServico.objects.all()
    return render(request, 'oficina/ordens.html', {'ordens': ordens})

@login_required
def editar_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    clientes = Cliente.objects.all()
    equipamentos = Equipamento.objects.all()

    if request.method == "POST":
        ordem.cliente_id = request.POST.get("cliente")
        ordem.equipamento_id = request.POST.get("equipamento")
        ordem.problema = request.POST.get("problema")
        ordem.diagnostico = request.POST.get("diagnostico")
        ordem.valor = request.POST.get("valor")
        valor_raw = request.POST.get("valor")

        # TRATAMENTO: Troca vírgula por ponto para o banco aceitar
        if valor_raw:
            valor_convertido = valor_raw.replace(',', '.')
            ordem.valor = valor_convertido
        
        # O problema deve estar aqui. Garanta que o nome seja 'status'
        status_novo = request.POST.get("status")
        if status_novo:
            ordem.status = status_novo
            
        ordem.save()
        return redirect('ordens')

    return render(request, "oficina/editar_ordem.html", {
        "ordem": ordem,
        "clientes": clientes,
        "equipamentos": equipamentos
    })

@login_required
def alterar_status(request, id, status):
    ordem = get_object_or_404(OrdemServico, id=id)
    ordem.status = status
    ordem.save()

    return redirect('ordens')

from django.shortcuts import render, redirect
from .models import Cliente, Equipamento, OrdemServico

@login_required
def novo_cliente(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')

        Cliente.objects.create(
            nome=nome,
            telefone=telefone,
            email=email,
            endereco=endereco
        )

        return redirect('/clientes/')

    return render(request, 'oficina/novo_cliente.html')

@login_required
def novo_equipamento(request):

    clientes = Cliente.objects.all()

    if request.method == 'POST':

        cliente_id = request.POST.get('cliente')
        tipo = request.POST.get('tipo')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        numero_serie = request.POST.get('numero_serie')

        cliente = Cliente.objects.get(id=cliente_id)

        Equipamento.objects.create(
            cliente=cliente,
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie
        )

        return redirect('/equipamentos/')

    return render(request, 'oficina/novo_equipamento.html', {'clientes': clientes})

@login_required
def nova_ordem(request):

    clientes = Cliente.objects.all()
    equipamentos = Equipamento.objects.all()

    if request.method == 'POST':

        cliente_id = request.POST.get('cliente')
        equipamento_id = request.POST.get('equipamento')
        problema = request.POST.get('problema')
        diagnostico = request.POST.get('diagnostico')
        valor = request.POST.get('valor')
        status = request.POST.get('status')

        cliente = Cliente.objects.get(id=cliente_id)
        equipamento = Equipamento.objects.get(id=equipamento_id)

        OrdemServico.objects.create(
            cliente=cliente,
            equipamento=equipamento,
            problema=problema,
            diagnostico=diagnostico,
            valor=valor,
            status=status
        )

        return redirect('/ordens/')

    return render(request, 'oficina/nova_ordem.html', {
        'clientes': clientes,
        'equipamentos': equipamentos
    })

@login_required
def finalizar_ordem(request, id):

    ordem = OrdemServico.objects.get(id=id)

    ordem.status = 'finalizado'

    ordem.save()

    return redirect('/ordens/')

@login_required
def cancelar_ordem(request, id):

    ordem = OrdemServico.objects.get(id=id)

    ordem.status = 'cancelado'

    ordem.save()

    return redirect('/ordens/')

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.http import HttpResponse
from .models import OrdemServico
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
from django.conf import settings

import os

@login_required
def pdf_ordem(request, id):
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    
    ordem = OrdemServico.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ordem_{ordem.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # TÍTULO E CABEÇALHO
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(largura/2, altura - 3*cm, "ORDEM DE SERVIÇO"),

    p.setFont("Helvetica", 11)
    p.drawCentredString(largura/2, altura - 4*cm, "VALAB Informática"),
    p.drawCentredString(largura/2, altura - 4.6*cm, "Telefone: (11) 99999-9999"),

    p.line(2*cm, altura - 5.5*cm, largura - 2*cm, altura - 5.5*cm)

    y = altura - 7*cm
    p.setFont("Helvetica-Bold", 13)
    p.drawString(3*cm, y, f"Ordem Nº: {ordem.id}"),

    # --- CONFIGURAÇÃO DA TABELA DINÂMICA ---
    
    # 1. Formatação do Valor para Padrão BRL
    valor_br = f"R$ {ordem.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    # 2. Estilos de Texto para permitir quebra de linha (Paragraph)
    styles = getSampleStyleSheet()
    style_texto = styles["Normal"]
    style_texto.fontSize = 11
    style_texto.leading = 14  # Espaçamento entre linhas

    # 3. Montagem dos Dados (Usando Paragraph nas colunas de texto longo)
    dados_tabela = [
        [Paragraph("<b>Cliente:</b>", style_texto), Paragraph(str(ordem.cliente.nome), style_texto)],
        [Paragraph("<b>Equipamento:</b>", style_texto), Paragraph(str(ordem.equipamento), style_texto)],
        [Paragraph("<b>Problema:</b>", style_texto), Paragraph(str(ordem.problema), style_texto)],
        [Paragraph("<b>Diagnóstico:</b>", style_texto), Paragraph(str(ordem.diagnostico), style_texto)],
        [Paragraph("<b>Status:</b>", style_texto), Paragraph(str(ordem.get_status_display()).upper(), style_texto)],
        [Paragraph("<b>Valor Total:</b>", style_texto), Paragraph(str(valor_br), style_texto)]
    ]

    # 4. Criação da Tabela com larguras fixas (4cm rótulo, 13cm conteúdo)
    tabela = Table(dados_tabela, colWidths=[4*cm, 13*cm])

    # 5. Estilização da Tabela com Moldura (GRID)
    tabela.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),          # Texto alinhado no topo da célula
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 5), (1, 5), colors.darkgreen),
        ('FONTSIZE', (0, 5), (1, 5), 13),
    ]))

    # 6. Cálculo e Desenho da Tabela
    tabela.wrapOn(p, largura, altura)
    altura_tabela = tabela._height  # Mede a altura que a tabela ocupou com os textos longos
    
    # Desenha a tabela. O 'y' é ajustado pela altura calculada
    tabela.drawOn(p, 2.5*cm, y - altura_tabela - 0.5*cm)

    # 7. ASSINATURAS (Posicionadas dinamicamente abaixo da tabela)
    y_assinaturas = y - altura_tabela - 4*cm # Espaço após a tabela

    # Cálculo para centralizar os blocos na página
    # Dividimos a largura em duas colunas imaginárias
    coluna_1 = largura / 4
    coluna_2 = (largura / 4) * 3

    # Bloco Assinatura do Cliente (Esquerda)
    p.line(coluna_1 - 3*cm, y_assinaturas, coluna_1 + 3*cm, y_assinaturas)
    p.drawCentredString(coluna_1, y_assinaturas - 0.6*cm, "Assinatura do Cliente")

    # Bloco Responsável Técnico (Direita)
    p.line(coluna_2 - 3*cm, y_assinaturas, coluna_2 + 3*cm, y_assinaturas)
    p.drawCentredString(coluna_2, y_assinaturas - 0.6*cm, "Responsável Técnico")

    # 8. RODAPÉ
    data_geracao = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M")
    usuario = request.user.username

    p.setFont("Helvetica", 8)
    p.drawCentredString(largura/2, 2*cm, f"Sistema de Assistência Técnica | OS Nº {ordem.id}"),
    p.drawCentredString(largura/2, 1.6*cm, f"Emitido por: {usuario} | {data_geracao}"),
    p.showPage()
    p.save()

    return response

from django.http import JsonResponse

@login_required
def atualizar_status(request, id):

    if request.method == "POST":

        ordem = OrdemServico.objects.get(id=id)
        novo_status = request.POST.get("status")

        ordem.status = novo_status
        ordem.save()

        return JsonResponse({"success": True})
    
from django.db.models import Q

def lista_ordens(request):
    ordens = OrdemServico.objects.all()
    
    # Captura os dados da busca
    busca = request.GET.get('busca')
    filtro = request.GET.get('filtro')

    if busca:
        if filtro == 'Nome':
            ordens = ordens.filter(cliente__nome__icontains=busca)
        elif filtro == 'Número de Série':
            ordens = ordens.filter(equipamento__serie__icontains=busca)
        elif filtro == 'ID':
            ordens = ordens.filter(id__exact=busca)

    return render(request, 'oficina/ordens.html', {'ordens': ordens})

@login_required
def lista_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    
    # Captura a busca se ela vier do Dashboard ou de um campo na própria página
    busca = request.GET.get('busca')
    if busca:
        equipamentos = equipamentos.filter(numero_serie__icontains=busca)
        
    return render(request, 'oficina/equipamentos.html', {'equipamentos': equipamentos})