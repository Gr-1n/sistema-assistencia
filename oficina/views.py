from django.shortcuts import render, redirect
from .models import Cliente, Equipamento, OrdemServico
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

@login_required
def dashboard(request):
    # --- Início da Lógica de Busca ---
    busca = request.GET.get('busca')
    filtro = request.GET.get('filtro')

    if busca:
        # Começamos com todas as ordens
        ordens = OrdemServico.objects.all()
        
        if filtro == 'cliente':
            # Busca pelo nome do cliente (campo 'nome' no model Cliente)
            ordens = ordens.filter(cliente__nome__icontains=busca)
            
        elif filtro == 'serie':
            # Buscamos diretamente na tabela de Equipamentos
            equipamentos = Equipamento.objects.filter(numero_serie__icontains=busca)
            
            if not equipamentos.exists():
                messages.error(request, f'Nenhum equipamento encontrado com a série "{busca}".')
                return redirect('dashboard')
            
            # Redireciona para a lista de equipamentos passando a busca na URL
            return render(request, 'oficina/equipamentos.html', {'equipamentos': equipamentos})
            
        elif filtro == 'id':
            # Busca exata pelo ID da Ordem de Serviço
            if busca.isdigit():
                ordens = ordens.filter(id=busca)
            else:
                ordens = OrdemServico.objects.none()

        # Validação: Se a lista estiver vazia após o filtro
        if not ordens.exists():
            messages.error(request, f'Nenhuma O.S. encontrada para "{busca}" no filtro {filtro}.')
            return redirect('dashboard')
        
        # Se encontrou, leva para a tela de listagem de ordens
        return render(request, 'oficina/ordens.html', {'ordens': ordens})
    
    # --- Fim da Lógica de Busca ---

    # Seu código original de contagem dos cards continua aqui abaixo...
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
        ordem.status = request.POST.get("status")

        ordem.save()

        return redirect("/ordens/")

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

    ordem = OrdemServico.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ordem_{ordem.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    largura, altura = A4

    # TÍTULO
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(largura/2, altura - 3*cm, "ORDEM DE SERVIÇO")

    # DADOS DA EMPRESA
    p.setFont("Helvetica", 11)
    p.drawCentredString(largura/2, altura - 4*cm, "VALAB Informática")
    p.drawCentredString(largura/2, altura - 4.6*cm, "Telefone: (11) 99999-9999")

    # LINHA
    p.line(2*cm, altura - 5.5*cm, largura - 2*cm, altura - 5.5*cm)

    y = altura - 7*cm

    # NÚMERO DA ORDEM
    p.setFont("Helvetica-Bold", 13)
    p.drawString(3*cm, y, f"Ordem Nº: {ordem.id}")

    y -= 1.5*cm

    # TABELA DE DADOS
    dados = [
        ["Cliente", ordem.cliente],
        ["Equipamento", str(ordem.equipamento)],
        ["Problema", ordem.problema],
        ["Diagnóstico", ordem.diagnostico],
        ["Status", ordem.status],
    ]

    largura_label = 5*cm
    largura_valor = 11*cm

    for label, valor in dados:

        p.setFont("Helvetica-Bold", 11)
        p.drawString(3*cm, y, label + ":")

        p.setFont("Helvetica", 11)
        p.drawString(8*cm, y, str(valor))

        y -= 1*cm

    # VALOR
    y -= 0.5*cm

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.darkgreen)
    p.drawString(3*cm, y, f"Valor do Serviço: R$ {ordem.valor}")
    p.setFillColor(colors.black)

    # ASSINATURAS
    y -= 3*cm

    p.line(3*cm, y, 9*cm, y)
    p.drawCentredString(6*cm, y - 0.6*cm, "Assinatura do Cliente")

    p.line(11*cm, y, 17*cm, y)
    p.drawCentredString(14*cm, y - 0.6*cm, "Responsável Técnico")

    # DATA E USUÁRIO
    data_geracao = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M")
    usuario = request.user.username

    # RODAPÉ
    p.setFont("Helvetica", 8)

    p.drawCentredString(
        largura/2,
        2*cm,
        f"Sistema de Assistência Técnica | OS Nº {ordem.id}"
    )

    p.drawCentredString(
        largura/2,
        1.6*cm,
        f"Emitido por: {usuario} | {data_geracao}"
    )

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
    ordens = Ordem.objects.all()
    
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