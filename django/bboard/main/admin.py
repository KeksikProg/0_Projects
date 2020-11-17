from django.contrib import admin
from .models import AdvUser
import datetime
from .utilities import send_activation_notification
from .models import SuperRubric, SubRubric
from .forms import SubRubricForm
from .models import Bb, AdditionalImage
from .models import Comment
from django.utils.safestring import mark_safe

#-----------------------------------------------------------------------------------------------
def send_activation_notifications(modeladmin, request, queryset): # Это у нас действие, которое позволяет всем кто не активировал аккаунт его активировать
	for rec in queryset: # Мы берем все юзеров
		if not rec.is_active: # и если они не активны
			send_activation_notification(rec) # То отправляем им сообщения 
	modeladmin.message_user(request, 'Письма с оповещениями отправлены') # Говорим админу что сообщения успешно отправлены
send_activation_notifications.short_description = 'Отправка писем с оповещениями об активации' # Название действия 

class NonactivatedFilter(admin.SimpleListFilter):
	title = 'Прошли активацию?' # Название фильтра
	parameter_name = 'actstate'

	def lookups(self, request, model_admin): # Название пунтов списков (значение, объяснение)
		return (
					('activated', 'Прошли'),
					('threedays', 'Не прошли более 3-ех дней'),
					('week', 'Не прошли более недели'),
				)

	def queryset(self, request, queryset):
		val = self.value
		if val == 'activated':
			return queryset.filter(is_active = True)
		elif val == 'threedays':
			d = datetime.date.today() - date.timedelta(days = 3)
			return queryset.filter(is_active = False, date_joined__date__lt = d)
		elif val == 'week':
			d = datetime.date.today() - date.timedelta(weeks = 1)
			return queryset.filter(is_active = False, date_joined__date__lt = d)

class AdvUserAdmin(admin.ModelAdmin): # Это редактор для модели пользователя
	list_display = ('__str__', 'is_active', 'date_joined')# Поля которые будут видны на всех записях
	search_fields = ('username', 'email', 'first_name', 'last_name',) # Поля по которым можно будет проводить поиск
	list_filter = (NonactivatedFilter,) # Фильтр который может использоваться в данной модели 
	fields = (('username', 'email'), # Поля которые уже будут видны на детальной странице записи
		('first_name', 'last_name'),
		('send_comment', 'is_active'),
		('is_staff', 'is_superuser', 'groups', 'user_permissions'),
		('last_login', 'date_joined'),)
	readonly_fileds = ('last_login', 'date_joined')
	actions = (send_activation_notifications,) # Действия которые будут доступны с данными записями 
#-----------------------------------------------------------------------------------------------

class SubRubricInline(admin.TabularInline): # Для того чтобы можно было создавать подрубрики прямо в редакторе надрубрик в линию
	model = SubRubric
class SuperRubricAdmin(admin.ModelAdmin): # Редактор для надрубрик
	exclude = ('super_rubric',)
	inlines = (SubRubricInline,) #Создает поле с линиями где будут создаваться подрубрики

class SubRubricAdmin(admin.ModelAdmin): # Для редактирования подрубрик на сайте администрации
	form = SubRubricForm


class AdditionalImageInline(admin.TabularInline): # Для того чтобы в создании объявления на сайте администрации можно было удобно управлять дополнительными иллюстрациями в линию
	model = AdditionalImage 

class BbAdmin(admin.ModelAdmin):
	list_display = (
		'rubric', 
		'title', 
		'content', 
		'author', 
		'created_at')
	
	
	fields = (
		('rubric', 'author'), 
		'title', 
		'content', 
		'price', 
		'contacts', 
		'image', 
		'is_active')
	inlines = (AdditionalImageInline,)

class CommentAdmin(admin.ModelAdmin):
	
	list_display = (
		'bb',
		'author',
		'content',
		'created_at')
	fields = (
		('bb', 'author'),
		'content',
		'is_active',)
	readonly_fileds = ('created_at',)
	search_fields = (
		'bb',
		'author',
		'content',)

	

admin.site.register(Comment, CommentAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(Bb, BbAdmin)
# Register your models here.
