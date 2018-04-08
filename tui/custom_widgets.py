from npyscreen.wgcheckbox import curses, Widget, widget


class MultistateCheckbox(Widget):
    def __init__(self, screen, cases=[' ', '+', '-'], value=0, controlColor='CONTROL', **keywords):
        super().__init__(screen, **keywords)
        self.value = value
        self.hide = False
        self.controlColor = controlColor
        self.cases = cases

    def set_up_handlers(self):
        super().set_up_handlers()

        self.handlers.update({
                curses.ascii.SP: self.on_toggle,
                ord('x'):        self.on_toggle,
                curses.ascii.NL: self.h_select_exit,
                curses.ascii.CR: self.h_select_exit,
                ord('j'):        self.h_exit_down,
                ord('k'):        self.h_exit_up,
                ord('h'):        self.h_exit_left,
                ord('l'):        self.h_exit_right,
            })

    def on_toggle(self, ch):
        self.value = self.value + 1 if self.value + 1 != len(self.cases) else 0

        self.whenToggled()

    def whenToggled(self):
        pass

    def h_select_exit(self, ch):
        if not self.value:
            self.on_toggle(ch)
        self.editing = False
        self.how_exited = widget.EXITED_DOWN

    def calculate_area_needed(self):
        return 1, 4

    def update(self, clear=True):
        if clear:
            self.clear()
        if self.hidden:
            self.clear()
            return False
        if self.hide:
            return True

        symbol = self.cases[self.value]
        cb_display = '[' + symbol + ']'

        if self.do_colors():
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display, self.parent.theme_manager.findPair(self, self.controlColor))
        else:
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display)

        if self.editing:
            char_under_cur = symbol

            if self.do_colors():
                self.parent.curses_pad.addstr(self.rely, self.relx + 1, char_under_cur, self.parent.theme_manager.findPair(self) | curses.A_STANDOUT)
            else:
                self.parent.curses_pad.addstr(self.rely,  self.relx + 1, curses.A_STANDOUT)
