#coding: utf-8

from functools import partial, update_wrapper

from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404

from . import settings
from .utils import unicode_urlencode, get_instance_from_path


class SimplePaginator(object):
    """
    Class based decorator.

    SimplePagination decorator must be used along with 'render_to' 
    decorator from django-annoying application
    http://bitbucket.org/offline/django-annoying/wiki/Home
    """

    def __init__(self, key=None, style=None, per_page=None, 
                frame_size=None, template=None, anchor=None):
        """
        Decorator parameters 

        key - Name of the variable with objects that we paginate.
        style - name of pagination backend.
        per_page - number of objects to show on page.
        frame_size - max pages numbers to show.
        """

        self.style = style or settings.PAGINATION_STYLE
        self.anchor = anchor
        self.backend = get_instance_from_path(settings.PAGINATION_BACKENDS[self.style])
        self.key = key or self.backend.KEY
        self.per_page = per_page or self.backend.PER_PAGE
        self.frame_size = frame_size or self.backend.FRAME_SIZE
        self.template = template or self.backend.TEMPLATE or 'paginator_%s.html' % self.style
        self.user_per_page_allowed = self.backend.USER_PER_PAGE_ALLOWED
        self.user_per_page_max = self.backend.USER_PER_PAGE_MAX
        
    def __call__(self, function):
        """
        Receive decorated function and return
        function decorated with decorate method
        """
        decorated = partial(self.decorate, function)
        return update_wrapper(decorated, self.decorate)
    
    def decorate(self, function, request, *args, **kwargs):

        # execute view 
        output = function(request, *args, **kwargs)
        
        # only try to paginate if view returned dictionary,
        # in all other cases just return view output.
        if not isinstance(output, dict):
            return output
        
        params = request.GET.copy()
        
        try:
            current_page = int(params.pop('page')[0])
        except (ValueError, KeyError):
            current_page = 1
        
        # we dont modify self.per_page because it's decorator
        # and it initialize only once.
        per_page = self.per_page 

        # per_page should change from GET parameters only if this
        # is allowed in settings or backend, also it must be lower
        # or equal then self.user_per_page_max.
        if self.user_per_page_allowed and 'per_page' in params:
            try:
                user_per_page = int(params['per_page'])
                if user_per_page <= self.user_per_page_max:
                    per_page = user_per_page
                else:
                    per_page = self.user_per_page_max
                    params['per_page'] = self.user_per_page_max
            except (ValueError, KeyError):
                params['per_page'] = self.per_page

        elif 'per_page' in params:
            params.pop('per_page')
        
        # we will paginate value of self.key, original object will be replaced 
        # by items that should be only in current page.
        try:
            paginate_qs = output.pop(self.key)
        except KeyError:
            raise KeyError("Key '%s' not found in view's returned dictionary" % self.key)

        # create django built in paginator object
        paginator = Paginator(paginate_qs, per_page)
        
        try:
            # check that asked page is exists
            page = paginator.page(current_page)
        except EmptyPage:
            raise Http404()

        # replace paginated items by only items we should see.
        output[self.key] = page.object_list
        
        # extra data that we may need to build links
        data = {}
        data['current_page'] = current_page # active page number
        data['per_page'] = per_page # items per page
        data['params'] = unicode_urlencode(params) # get parameters
        data['anchor'] = self.anchor # ancor
        data['number_of_pages'] = number_of_pages = paginator.num_pages # number of pages
        data['template'] = self.template
        data['count'] = paginator.count

        # execute the pagination function
        data.update(self.backend.paginate(self.frame_size, number_of_pages, current_page))

        # your view now have extra key 'paginator' with all extra data inside.
        output['paginator'] = data
        
        return output

    
paginate = SimplePaginator


def simple_paginate(queryset, request, *args, **kwargs):
    """
    http://habrahabr.ru/blogs/django/76961/#comment_2239477
    обертка для того, чтобы не использовать render_to
    """
    @paginate(*args, **kwargs)
    def inner(request,queryset):
        return {'object_list': queryset}

    data = inner(request,queryset)
    # в data будет лежать
    # {'object_list': <отфильтрованный object_list>, 'paginator': <наш паджинатор>}

    # вместо этого можно возвращать 2 значения.
    # Или принимать словарь с контекстом и обновлять его.
    data['paginator']['object_list'] = data['object_list']

    return data['paginator']


