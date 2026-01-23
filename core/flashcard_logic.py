def next_card(state):
    state.index = (state.index + 1) % len(state.cards)
    state.show_answer = False
    

def flip_card(state):
    state.show_answer = not state.show_answer

