from django.db import models

arquivos=[
    ".png",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".doc",
    ".ppt",
    ".docx",
    ".xlsx",
    ".csv"
]

class TipoArquivo(models.Model):
    tipoArquivo = models.CharField("Tipo de Arquivo", max_length= 100, choices=[(i,i) for i in arquivos], unique=True)

    class Meta:
        verbose_name = "Tipo de Arquivo"
        verbose_name_plural = "Tipos de Arquivos"

    def __str__(self):
        return f"{self.tipoArquivo}"
