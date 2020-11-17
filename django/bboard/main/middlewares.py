from .models import SubRubric

def bboard_context_processor(request): # Вообще это посредник, который принимает запрос клиента перед самим контроллером
	context = {}
	context['rubrics'] = SubRubric.objects.all()
	context['keyword'] = ''
	context['all'] = ''
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		if keyword:
			context['keyword'] = '?keyword=' + keyword
			context['all'] = context['keyword']
	if 'page' in request.GET:
		page = request.GET['page']
		if page != '1':
			if context['all']:
				context['all'] += '&page=' + page
			else:
				context['all'] = '?page=' + page
	return context
'''
Пояснения для переменных keyword и page в списке контекста
пример
вот человек воспользовался поиском и на 2 странице пагинатора к примеру
переходит на какое-то объявление оно ему не нравиться и он возвращается обратно
но попадает на 1 страницу без использования поиска
чтобы это исправить мы из гет запроа берем переменную keyword и если она не пустая то вставляем её в контекст
также со страницой пагинатора если она не первая, то мы вставляем её в контекст, вот и все
'''