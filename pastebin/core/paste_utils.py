
def create_excerpts_for_text_fields(pastes:[], excerpt_length):
    for p in pastes:
        if len(p.text_field) > excerpt_length:
            p.text_field = ' '.join([p.text_field[:excerpt_length], ' ...'])
        else:
            p.text_field = p.text_field[:excerpt_length]
    return pastes