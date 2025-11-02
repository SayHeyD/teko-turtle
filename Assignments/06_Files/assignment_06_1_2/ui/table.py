from typing import List, Any

class Table:
    def __init__(self, headers: List[str], rows: List[List[Any]]):
        self.__headers = headers
        self.__rows = rows

    def __get_max_column_length(self, header: str, column_index: int) -> int:
        max_length = len(header) + 2

        for row in self.__rows:
            value = row[column_index] if column_index < len(row) else ''
            value_length = len(str(value)) + 2
            if value_length > max_length:
                max_length = value_length

        return max_length

    def __get_all_column_lengths(self) -> List[int]:
        return [self.__get_max_column_length(header, idx) for idx, header in enumerate(self.__headers)]

    def __print_seperator(self, length: int) -> None:
        print('+'.ljust(length, '-'), end='-')

    def __print_seperator_row(self) -> None:
        column_lengths = self.__get_all_column_lengths()
        for column_length in column_lengths:
            self.__print_seperator(column_length)
        print('+')

    def __print_header_row(self) -> None:
        column_lengths = self.__get_all_column_lengths()
        self.__print_seperator_row()
        for i, header in enumerate(self.__headers):
            # For all but last, keep same pattern with trailing space
            if i < len(self.__headers) - 1:
                print(f'| {header}'.ljust(column_lengths[i]), end=' ')
            else:
                print(f'| {header}'.ljust(column_lengths[i]) + ' |')
        self.__print_seperator_row()

    def __print_data_row(self, row: List[Any]) -> None:
        column_lengths = self.__get_all_column_lengths()
        for i, value in enumerate(row):
            text = f'| {value}'
            if i < len(self.__headers) - 1:
                print(text.ljust(column_lengths[i]), end=' ')
            else:
                print(text.ljust(column_lengths[i]) + ' |')

    def print_table(self) -> None:
        self.__print_header_row()
        for row in self.__rows:
            self.__print_data_row(row)
        self.__print_seperator_row()
