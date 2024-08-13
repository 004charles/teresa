from django.contrib import admin
from .models import Gerente, Cliente, Empresas, Categoria_produto, Marca_produto, Condicao, Fornecedor, Produtos, Chat, contactar, Pedido, Noticia, Marca_index, Video, Contato_empresa, Fatura, Iban, Pedido_empresa, Ticket, ItemCarrinho

class ReadOnlyAdmin(admin.ModelAdmin):
    # Define todos os campos como somente leitura
    readonly_fields = [field.name for field in Cliente._meta.fields]


class ReadOnlyEmpresaAdmin(admin.ModelAdmin):
    # Define todos os campos como somente leitura
    readonly_fields = [field.name for field in Empresas._meta.fields]

    def has_add_permission(self, request):
        # Remove a permissão para adicionar novas empresas
        return False

    def has_delete_permission(self, request, obj=None):
        # Remove a permissão para excluir empresas
        return False

    def has_change_permission(self, request, obj=None):
        # Remove a permissão para modificar empresas
        return False

admin.site.register(Gerente)
admin.site.register(Noticia)
admin.site.register(Cliente, ReadOnlyAdmin)
admin.site.register(Empresas, ReadOnlyEmpresaAdmin)
admin.site.register(Categoria_produto)
admin.site.register(Marca_produto)
admin.site.register(Condicao)
admin.site.register(Fornecedor)
admin.site.register(Produtos)
admin.site.register(Chat)
admin.site.register(contactar)
admin.site.register(Pedido)
admin.site.register(Marca_index)
admin.site.register(Video)
admin.site.register(Contato_empresa)
admin.site.register(Fatura)
admin.site.register(Iban)
admin.site.register(Pedido_empresa)
admin.site.register(Ticket)
admin.site.register(ItemCarrinho)
