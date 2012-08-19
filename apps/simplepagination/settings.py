from django.conf import settings

### BACKENDS #################################################################################################
# Dictionary with paginator name as key and path to class as value.                                          #
# Class must have 'paginate' function inside that receive 3 parameters                                       #
# frame_size, number_of_pages and current_page_number                                                        #
# this function must return dictionary that will be added to view dictionary under key 'paginator'           #
PAGINATION_BACKENDS = getattr(settings, 'PAGINATION_BACKENDS', {                                             #
    'digg': 'apps.simplepagination.backends.digg.DiggPaginator',                                                  #
    'filmfeed': 'apps.simplepagination.backends.filmfeed.FilmfeedPaginator',                                      #
})                                                                                                           #
##############################################################################################################

### STYLE ####################################################################################################
# Style is name of the backend, it will be used as default style for all paginators if no style parameter    #
# is passed to decorator.                                                                                    #
PAGINATION_STYLE = getattr(settings, 'PAGINATION_STYLE', 'digg')                                             #
##############################################################################################################

### KEY ######################################################################################################
# Key is name of the key with items in view returned dictionary that we paginate                             #
PAGINATION_KEY = getattr(settings, 'PAGINATION_KEY', 'object_list')                                          #
##############################################################################################################

### PER_PAGE #################################################################################################
# Default number of items on page                                                                            #
PAGINATION_PER_PAGE = getattr(settings, 'PAGINATION_PER_PAGE', 20)                                           #
##############################################################################################################

### FRAME_SIZE ###############################################################################################
# Default frame size of paginator.                                                                           #
PAGINATION_FRAME_SIZE = getattr(settings, 'PAGINATION_FRAME_SIZE', 8)                                        #
##############################################################################################################

### USER_PER_PAGE_ALLOWED ####################################################################################
# IF set to True, user can manualy change per_page setting with GET parameters, the default is to allow      #
# it in debug mode and disable in production.                                                                #
PAGINATION_USER_PER_PAGE_ALLOWED = getattr(settings, 'PAGINATION_USER_PER_PAGE_ALLOWED', settings.DEBUG)     #
##############################################################################################################

### USER_PER_PAGE_MAX ########################################################################################
# Maximum items per page                                                                                     #
PAGINATION_USER_PER_PAGE_MAX = getattr(settings, 'PAGINATION_USER_PER_PAGE_MAX', 100)                        #
##############################################################################################################

### TEMPLATE #################################################################################################
# Default template for all paginators, dont set it if you use more than one backends                         #
PAGINATOR_TEMPLATE = getattr(settings, 'PAGINATOR_TEMPLATE', None)                                           #
##############################################################################################################
