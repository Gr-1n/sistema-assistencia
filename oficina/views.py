from django.shortcuts import render
from .models import Cliente, Equipamento, OrdemServico


def dashboard(request):
    return render(request, 'oficina/dashboard.html')


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'oficina/clientes.html', {'clientes': clientes})


def equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'oficina/equipamentos.html', {'equipamentos': equipamentos})


def ordens(request):
    ordens = OrdemServico.objects.all()
    return render(request, 'oficina/ordens.html', {'ordens': ordens})

from django.shortcuts import render, redirect
from .models import Cliente, Equipamento, OrdemServico


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

def finalizar_ordem(request, id):

    ordem = OrdemServico.objects.get(id=id)

    ordem.status = 'finalizado'

    ordem.save()

    return redirect('/ordens/')

def cancelar_ordem(request, id):

    ordem = OrdemServico.objects.get(id=id)

    ordem.status = 'cancelado'

    ordem.save()

    return redirect('/ordens/')