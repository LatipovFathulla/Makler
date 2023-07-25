from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import MasterModel, MasterImagesModel, MasterProfessionModel, HowServiceModel


@admin.register(MasterProfessionModel)
class MasterProfessionModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    search_fields = ['title']
    list_filter = ['title']
    save_on_top = True
    save_as = True


@admin.register(HowServiceModel)
class HowServiceModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created_at']
    search_fields = ['title']
    save_as = True


class MasterImagesModelAdmin(admin.TabularInline):
    model = MasterImagesModel
    extra = 1


#         for i in validated_data['profession']:
#             profession = MasterProfessionModel.objects.get(id=i)
#             mastermodel.profession.add(profession)
#        profession = MasterProfessionModel.objects.filter(profession=self.instance.id)
@admin.register(MasterModel)
class MasterModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address_title', 'avatar_image_tag', 'get_profession_titles',
                    'product_status', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['name', 'email', 'phone']
    inlines = [MasterImagesModelAdmin]
    save_on_top = True
    save_as = True

    def avatar_image_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" height="60" />'.format(obj.avatar.url))
        else:
            return '-'

    avatar_image_tag.short_description = _('Image')

    def get_profession_titles(self, obj):
        return ", ".join([profession.title for profession in obj.profession.all()])

    get_profession_titles.short_description = _('Profession')
