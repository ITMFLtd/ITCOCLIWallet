
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