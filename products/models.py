from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class UnitMeasurement(models.TextChoices):
    UNIDADE = 'un', 'Unidade'
    PACOTE = 'pct', 'Pacote'
    CAIXA = 'cx', 'Caixa'
    DUZIA = 'dz', 'Dúzia'
    FARDO = 'fd', 'Fardo'
    LATA = 'lt', 'Lata'
    ROLO = 'rl', 'Rolo'
    QUILOGRAMA = 'kg', 'Quilograma'
    GRAMA = 'g', 'Grama'
    LITRO = 'l', 'Litro'
    MILILITRO = 'ml', 'Mililitro'
    METRO = 'm', 'Metro'


class Product(models.Model):
    name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=2, decimal_places=1)
    selling_price = models.DecimalField(max_digits=2, decimal_places=1)
    unit_measurement = models.CharField(
        max_length=15,
        choices=UnitMeasurement,
        default=UnitMeasurement.UNIDADE
    )
    barcode = models.CharField(max_length=50, blank=False, null=False, unique=True)
    current_stock = models.IntegerField()

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['name']

    def __str__(self):
        return self.name


class StockMovementType(models.TextChoices):
    ENTRADA = 'entrada', 'Entrada'
    SAIDA = 'saida', 'Saída'


class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=10, choices=StockMovementType.choices)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-date']

    def __str__(self):
        return f'{self.get_movement_type_display()} - {self.product.name} ({self.quantity})'

