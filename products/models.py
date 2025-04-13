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
