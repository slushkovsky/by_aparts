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

        _y = 0

        # Row 1
        self.add(nps.FixedText, value='Onliner.by flats rental improved search', editable=False)
        _y += 5

        # Row 2
        self.add(nps.TitleMultiSelect, name='Rooms count:', values=ROOMS_OPTIONS, rely=_y, max_height=len(ROOMS_OPTIONS), max_width=w // 2)
        self.add(nps.TitleText, name='Price min ($):', relx=w // 2 + 1, rely=_y, use_two_lines=False)
        self.add(nps.TitleText, name='Price max ($):', relx=w // 2 + 1, rely=_y + 1, use_two_lines=False)
        self.add(nps.TitleText, name='With words:', relx=w // 2 + 1, rely=_y + 2, use_two_lines=False)
        self.add(nps.TitleText, name='Without words:', relx=w // 2 + 1, rely=_y + 3, use_two_lines=False)
        _y += max(len(ROOMS_OPTIONS), 4) + 1

        # Row 3
        self.add(nps.FixedText, value='Options:', rely=_y, editable=False)
        _y += 1

        for option in APART_OPTIONS:
            self.add(MultistateCheckbox, rely=_y, relx=18)
            self.add(nps.FixedText, value=option, rely=_y, relx=18 + 5, editable=False)
            _y += 1

        _y += 1

        # Row 4
        self.add(nps.Checkbox, name='Show previous results', rely=_y)

    def on_ok(self):
        pass  # Run search

    def on_cancel(self):
        self.parentApp.switchForm(None)


if __name__ == '__main__':
    App().run()
