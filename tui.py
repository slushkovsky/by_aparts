from npyscreen import StandardApp, MultiSelectAction, TitleFilename, TitleFixedText, FixedText, Textfield, GridColTitles, ActionForm, TitleMultiSelect, SimpleGrid, TitleText, TitleSlider, BoxTitle


APART_OPTIONS = ['Мебель', 'Кухонная мебель', 'Плита', 'Холодильник', 'Стиральная машина', 'Телевизор', 'Интернет', 'Лоджия или балкон', 'Кондиционер']
ROOMS_OPTIONS = ['1', '2', '3', '4+']


class App(StandardApp):
    def onStart(self):
        self.addForm('MAIN', SearchParams, name='Search parameters')

class SearchParams(ActionForm):
    def create(self):
        h, w = self.useable_space()

        ROWS_HEIGHTS = [4, 9, len(APART_OPTIONS) + 1]

        # Row 1
        self.add(FixedText, value='Onliner.by flats rental improved search')

        # Row 2
        self.add(TitleMultiSelect, name='Rooms count:', values=ROOMS_OPTIONS, rely=sum(ROWS_HEIGHTS[:1]), max_height=ROWS_HEIGHTS[1], max_width=w // 2)
        self.add(TitleText, name='Price min ($):', relx=w // 2 + 1, rely=sum(ROWS_HEIGHTS[:1]))
        self.add(TitleText, name='Price max ($):', relx=w // 2 + 1, rely=sum(ROWS_HEIGHTS[:1]) + 2)
        self.add(TitleText, name='With words:', relx=w // 2 + 1, rely=sum(ROWS_HEIGHTS[:1]) + 4)
        self.add(TitleText, name='Without words:', relx=w // 2 + 1, rely=sum(ROWS_HEIGHTS[:1]) + 6)
        
        # Row 3
        self.add(TitleMultiSelect, name='With options:', values=APART_OPTIONS, rely=sum(ROWS_HEIGHTS[:2]), max_width=w // 2, max_height=ROWS_HEIGHTS[2])
        self.add(TitleMultiSelect, name='Without options:', values=APART_OPTIONS, rely=sum(ROWS_HEIGHTS[:2]), relx=w // 2 + 1, max_height=ROWS_HEIGHTS[2])
        
        # Row 4
        self.add(TitleFilename, name='Ignore list', rely=sum(ROWS_HEIGHTS[:3]))

    def on_ok(self):
        pass # Run search

    def on_cancel(self):
        self.parentApp.switchForm(None) 


if __name__ == '__main__':
    App().run()
