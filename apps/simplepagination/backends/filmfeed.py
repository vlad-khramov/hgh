from apps.simplepagination.backends import Paginator


class FilmfeedPaginator(Paginator):
    def paginate(self, frame_size, number_of_pages, current_page):
        output = {}
        if number_of_pages < frame_size:
            output['page_numbers'] = range(1, number_of_pages + 1)
        elif current_page < (frame_size / 2) + 1:
            output['page_numbers'] = range(1, frame_size + 1)
        elif current_page >= (frame_size / 2) + 1 and number_of_pages - (frame_size / 2) <= current_page:
            output['page_numbers'] = range(number_of_pages - frame_size + 1, number_of_pages + 1)
        elif current_page >= (frame_size / 2) + 1:
            start = current_page - (frame_size / 2)
            end = current_page + (frame_size / 2)
            output['page_numbers'] = range(start, end + 1)
        return output

