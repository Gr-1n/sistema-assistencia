from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Equipamento, OrdemServico
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    total_os = OrdemServico.objects.count()
    total_clientes = Cliente.objects.count()
    abertas = OrdemServico.objects.filter(status="aberto").count()
    prontas = OrdemServico.objects.filter(status="pronto").count()

    context = {
        "total_os": total_os,
        "total_clientes": total_clientes,
        "abertas": abertas,
        "prontas": prontas
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