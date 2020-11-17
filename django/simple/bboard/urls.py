from django.urls import path

from .views import index, by_rubric

#from .views import BbCreateView
from .views import add_and_save
from .views import BbDetailView
from .views import BbEditView
from .views import BbDeleteView
from django.views.decorators.http import condition
from .views import bb_lmf
from .views import api_rubrics
from .views import api_rubric_detail


urlpatterns = [
	path('<int:rubric_id>/', by_rubric, name = 'by_rubric'), # тут у нас параметезированный адрес на каждую рубрику
	path('', index, name = 'index'), # Первая страница сайта (доска объявлений)
	path('detail/<int:pk>/', condition(last_modified_func = bb_lmf) (BbDetailView.as_view()), name = 'detail'), # Детали заказа (вся страница под один заказ) Тут у нас используется кэш, то есть если дата публицаии не была изменена, значит брать страницу из кэша
	path('edit/<int:pk>', BbEditView.as_view(), name = 'edit'), # Для изменения объявления 
	path('add/', add_and_save, name = 'add'), # тут у нас контроллер, который выполняет две задачи, а значит для него нужен всего один адрес
	path('delete/<int:pk>', BbDeleteView.as_view(), name = 'delete'), # Для того чтобы удалять записи 
	path('api/rubrics/', api_rubrics), # Для того чтобы получить сведения о рубрике если их запросили какие-либо приложения
	path('api/rubrics/<int:pk>', api_rubric_detail),
]