from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=300)

    def __str__(self):
        return self.nome
    
class Equipamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tipo} - {self.marca} {self.modelo}"

class OrdemServico(models.Model):

    STATUS_CHOICES = [
        ('recebido', 'Recebido'),
        ('diagnostico', 'Diagnóstico'),
        ('aprovacao', 'Aguardando Aprovação'),
        ('reparo', 'Em Reparo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)

    problema = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)

    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    garantia = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='recebido'
    )

    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente}"