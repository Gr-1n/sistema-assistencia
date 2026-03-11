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
        ('aprovacao', 'Aguardando aprovação'),
        ('reparo', 'Em reparo'),
        ('finalizado', 'Finalizado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)

    problema = models.TextField()
    diagnostico = models.TextField(blank=True)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='recebido'
    )

    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente}"
