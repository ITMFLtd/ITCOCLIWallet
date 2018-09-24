SPLASH = """  _____ _______ _____ ____  
 |_   _|__   __/ ____/ __ \ 
   | |    | | | |   | |  | |
   | |    | | | |   | |  | |
  _| |_   | | | |___| |__| |
 |_____|  |_|  \_____\____/ 

                            """

def gui_select_from(term, options, prompt=''):
    if not prompt:
        prompt = "Use arrow keys to select option:"
    selected = 0
    while True:
        with term.hidden_cursor():
            print(term.clear)
            print(prompt)
            for i, o in enumerate(options):
                if i == selected:
                    print(term.reverse(o))
                else:
                    print(o)
            with term.cbreak():
                button = term.inkey()
                if button.name == 'KEY_UP':
                    selected = max(0, selected - 1)
                if button.name == 'KEY_DOWN':
                    selected = min(len(options) - 1, selected + 1)
                if button.name == 'KEY_ENTER':
                    return options[selected]


def show_splash_screen(term):
    with term.hidden_cursor():
        offset = 7
        for line in SPLASH.splitlines():
            print(term.move_y(term.height // 2 - offset) +
                  term.center(line).rstrip())
            offset -= 1
        print(term.move_y(term.height // 2) +
              term.center(term.bold('Press Any Key to Continue')))
        with term.cbreak():
            term.inkey()
    print(term.clear)