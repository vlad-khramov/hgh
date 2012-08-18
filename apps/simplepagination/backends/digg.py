from apps.simplepagination.backends import Paginator


class DiggPaginator(Paginator):

    def paginate(self, frame_size, number_of_pages, current_page):
        output = {}
        if current_page > 1:
            output['PREVIOUS'] = current_page -1
        if current_page < number_of_pages:
            output['NEXT'] = current_page + 1
        if number_of_pages > frame_size and number_of_pages <= frame_size +2:
            output['left_page_numbers'] = range(1, number_of_pages + 1)
        elif number_of_pages <= frame_size:
            output['left_page_numbers'] = range(1, number_of_pages + 1)
        elif number_of_pages > frame_size and current_page < frame_size - 1:
            output['left_page_numbers'] = range(1, frame_size + 1)
            output['right_page_numbers'] = range(number_of_pages -1, number_of_pages +1)
        elif number_of_pages > frame_size and current_page > frame_size - 2 and number_of_pages - (frame_size / 2) <= current_page + 1:
            output['left_page_numbers'] = range(1, 3)
            output['middle_page_numbers'] = range(number_of_pages - frame_size + 1, number_of_pages +1)
        elif number_of_pages > frame_size and current_page > frame_size - 2:
            output['left_page_numbers'] = range(1, 3)
            output['middle_page_numbers'] = range(current_page - (frame_size / 2) +1, current_page + (frame_size / 2))
            output['right_page_numbers'] = range(number_of_pages -1, number_of_pages +1)
        return output

