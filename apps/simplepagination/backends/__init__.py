from apps.simplepagination import settings


class Paginator(object):
    def paginate(self, frame_size, number_of_pages, current_page):
        raise NotImplemented

    # see settings file for explanations

    KEY = getattr(settings, 'PAGINATION_KEY')
    PER_PAGE = getattr(settings, 'PAGINATION_PER_PAGE')
    FRAME_SIZE = getattr(settings, 'PAGINATION_FRAME_SIZE')
    TEMPLATE = getattr(settings, 'PAGINATOR_TEMPLATE')
    USER_PER_PAGE_ALLOWED = getattr(settings, 'PAGINATION_USER_PER_PAGE_ALLOWED')
    USER_PER_PAGE_MAX = getattr(settings, 'PAGINATION_USER_PER_PAGE_MAX')
