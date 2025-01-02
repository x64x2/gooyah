from typing import Sequence, Any, Optional, List


def clear_term():
    print('\033c', end='')


class Prompt:
    def __init__(
        self,
        options: Sequence[Any],
        title: Optional[str] = None,
        multiselect: bool = False,
        pagination: bool = False,
        lines: int = 20,
        indicator: str = '*',
    ):
        self.options = options
        self.title = title
        self.multiselect = multiselect
        self.pagination = pagination
        self.lines_per_page = lines
        self.indicator = indicator
        self._offset = 0
        self.selected_indexes: List[int] = []

    def _unpack_range(self, raw: str):
        """
        Handle single arguments
        (arguments that allows you to select only one option)

        Format: `start-end`, `-end`, `start-`, `-`
        """
        raw = raw.strip()

        negate = False
        if raw.startswith('!'):
            negate = True
            raw = raw[1:]

        arguments = raw.split('>')

        start, end = [i.strip() for i in arguments]

        if len(arguments) > 2:
            raise ValueError('Invalid range format:', raw)
        elif len(arguments) - arguments.count('') < 2:
            # format: -e, s-, -
            if raw.startswith('>'):
                start = 0
            if raw.endswith('>'):
                end = len(self.options) - 1

        start, end = int(start), int(end)

        if start > end:
            raise ValueError(
                'Ending value should be higher than starting value', raw
            )
        if start < 0 or end >= len(self.options):
            raise IndexError('Index out of bounds', raw)

        for index in range(start, end + 1):
            if index in self.selected_indexes and negate:
                # only add index when it is not selected
                self.selected_indexes.remove(index)
            if index not in self.selected_indexes and not negate:
                # this if clause is necessary because
                # if the index was added already,
                # and `negate` is false,
                # we don't want to add the index for a second time
                self.selected_indexes.append(index)

    def _unpack_single(self, raw: str):
        """
        Handle single arguments
        (arguments that allows you to select only one option)
        """
        arguments = raw.split(' ')

        for index in arguments:
            if index == '':
                continue

            negate = False
            if index.startswith('!'):
                negate = True
                index = index[1:]

            index = int(index.strip())

            if index < 0 or index >= len(self.options):
                raise IndexError('Index out of bounds', index)

            if index in self.selected_indexes and negate:
                self.selected_indexes.remove(index)
            if index not in self.selected_indexes and not negate:
                self.selected_indexes.append(index)

    def _unpack_values(self, raw: str):
        """
        Unpack one-line arguments into seperate arguments.
        """
        arguments = raw.split(';')

        if not self.multiselect and (len(arguments) > 1 or raw.count('>') > 0):
            raise ValueError(
                'Multiple options was selected for a single value prompt',
                arguments,
            )

        for argument in arguments:
            if argument.count('>') > 0:
                self._unpack_range(argument)
            else:
                self._unpack_single(argument)

    def _print_options(self):
        """
        Print out the supplied options
        """

        options = self.options
        start = 0

        if self.pagination:
            start = self._offset * self.lines_per_page
            end = (self._offset + 1) * self.lines_per_page
            options = options[start:end]

        for (index, option) in enumerate(options):
            index = index + start
            if index in self.selected_indexes:
                print('{} {:>3}) {}'.format(self.indicator, index, option))
            else:
                print('{:>5}) {}'.format(index, option))

    def _get_selected(self):
        """
        Return values (and/or options, indexes) that were selected.
        """
        if self.multiselect:
            return_tuples = []
            for selected in self.selected_indexes:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            index = self.selected_indexes[0]
            return self.options[index], index

    def prompt(self):
        """
        The prompt itself.
        """
        while True:
            clear_term()
            print(self.title, '\n')

            self._print_options()

            response = input('> ').strip()

            if response.startswith('help'):
                self.print_help()
                continue

            elif (
                response.startswith('n') or response.startswith('next')
            ) and self.pagination:

                # Check if the next page is available
                if (self._offset + 1) * self.lines_per_page <= len(
                    self.options
                ):
                    self._offset += 1
                continue

            elif response.startswith('pg'):
                self.pagination = not self.pagination
                continue

            elif (
                response.startswith('p') or response.startswith('prev')
            ) and self.pagination:

                # Check if the previous page is available
                if self._offset > 0:
                    self._offset -= 1
                continue

            elif (
                len(response) < 1
                or response.startswith('q')
                or response.startswith('quit')
                or response.startswith('exit')
            ):
                raise ValueError("Prompt exits without choosing.")

            self._unpack_values(response)

            if not self.multiselect:
                # we just let this loop one time if we are not multiselecting
                break

        return self._get_selected()

    def print_help(self):
        clear_term()
        print(
            """
We have a dummy array here: [1, 2, 4, 3, 6, 7, 9, 5, 8]

With this array as our options, the prompt will look something like this:
```
0) 1
1) 2
2) 4
3) 3
4) 6
5) 7
6) 9
7) 5
8) 8
```

There are two types of prompt: single and multi.

# Single prompt
You can only select one option with the single prompt.

# Multi prompt
You can select multiple options with the multi prompt.

A multi prompt runs in a loop, so the user can choose multiple times.
The interaction ends if the user submitted nothing (eg: blank `Enter`).

# Single select
This example selects one option from the prompt described above:
6 -> [9]
3 -> [3]

Only single select is allowed for single prompts.

# Range select
You can select a range of options with `>`, for example:
```
0>3 -> [1, 2, 4, 3] // select from index 0 to index 3
6>8 -> [9, 5, 8] // select from index 6 to index 8
```

You can also omit both starting value and ending value.
```
>6 -> [1, 2, 4, 3, 6, 7, 9] // select from the start to index 6
3> -> [3, 6, 7, 9, 5, 8] // select from index 3 to the end
> -> [1, 2, 4, 3, 6, 7, 9, 5, 8] // select everything
```

# Arguments
You can merge statements with `,`, for example:
```
// select from index 2 to index 6 *then* select index 8
2>6, 8 -> [4, 3, 6, 7, 9, 8]

// select from index 0 to index 2 *then* select from ...
0>2, 4>5 -> [1, 2, 4, 6, 7]
```

# Negate (not)
You can exclude an index with `!`, for example:
```
> -> [1, 2, 4, 3, 6, 7, 9, 5, 8] // select everything
>, !2 -> [1, 2, 3, 6, 7, 9, 5, 8] // everything but index 2
>, !2, !4>6 -> [1, 2, 4, 5, 8] // everything but index 2 and 4 to 6
```
        """
        )

        input('Enter to exit this help screen')


def prompt(
    options: Sequence[Any],
    title: Optional[str] = None,
    multiselect: bool = False,
    pagination: bool = False,
    lines: int = 20,
    indicator: str = '*',
):
    return Prompt(
        options, title, multiselect, pagination, lines, indicator
    ).prompt()
