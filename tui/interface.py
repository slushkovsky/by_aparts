import npyscreen as nps

from custom_widgets import MultistateCheckbox


APART_OPTIONS = ['Мебель', 'Кухонная мебель', 'Плита', 'Холодильник', 'Стиральная машина', 'Телевизор', 'Интернет', 'Лоджия или балкон', 'Кондиционер']
ROOMS_OPTIONS = ['1', '2', '3', '4+']


class App(nps.StandardApp):
    def onStart(self):
        self.addForm('MAIN', SearchParams, name='Search parameters')


class SearchParams(nps.ActionForm):
    def create(self):
        h, w = self.useable_space()

        FIRST_COLUMN_X = 2
        SECOND_COLUMN_X = w // 2 + 1

        # Row 1
        self.add(nps.FixedText, value='Onliner.by flats rental improved search', editable=False)
        self.nextrely += 2

        # Row 2
        self.add(nps.TitleMultiSelect, name='Rooms count:', values=ROOMS_OPTIONS, max_height=len(ROOMS_OPTIONS), max_width=w // 2, scroll_exit=True)
        self.nextrelx = SECOND_COLUMN_X
        self.nextrely -= 4

        self.add(nps.TitleText, name='Price min ($):', use_two_lines=False)
        self.add(nps.TitleText, name='Price max ($):', use_two_lines=False)
        self.add(nps.TitleText, name='With words:', use_two_lines=False)
        self.add(nps.TitleText, name='Without words:', use_two_lines=False)

        self.nextrely += 1

        # Row 3
        start_y = self.nextrely

        ## Col 1
        self.nextrelx = FIRST_COLUMN_X

        self.add(nps.FixedText, value='Options:', editable=False)

        for option in APART_OPTIONS:
            self.add(MultistateCheckbox)
            self.nextrely -= 1
            self.nextrelx += 5
            self.add(nps.FixedText, value=option, editable=False)
            self.nextrelx -= 5

        self.nextrely += 1
       
        row_nextrely = self.nextrely

        ## Col 2
        self.nextrely = start_y
        self.nextrelx = SECOND_COLUMN_X

        self.add(nps.Checkbox, name='Only owner (remove ads from agencies)')

        row_nextrely = max(self.nextrely, row_nextrely)
        self.nextrely = row_nextrely

        # Row 4
        self.nextrelx = FIRST_COLUMN_X
        self.add(nps.Checkbox, name='Show previous results')

    def on_ok(self):
        pass  # Run search

    def on_cancel(self):
        self.parentApp.switchForm(None)


if __name__ == '__main__':
    App().run()
