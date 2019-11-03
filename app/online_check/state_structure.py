


def get_posible_states(current_state):
    posible_states = []

    if current_state == "new":
        posible_states.append(('in_stock', 'Im Schrank'))
        posible_states.append(('diagnosis', 'Diagnose'))
        posible_states.append(('wait', 'Warten auf Gerät'))
        posible_states.append(('closed', 'Abgeschlossen'))
        return posible_states

    if current_state == "wait":
        posible_states.append(('in_stock', 'Im Schrank'))
        posible_states.append(('diagnosis', 'Diagnose'))
        return posible_states

    if current_state == "in_stock":
        posible_states.append(('diagnosis', 'Diagnose'))
        return posible_states

    if current_state == "diagnosis":
        posible_states.append(('inform_customer', 'Kunde informieren'))
        posible_states.append(('in_stock', 'Im Schrank'))
        posible_states.append(('under_repair', 'In Reparatur'))
        return posible_states

    if current_state == "inform_customer":
        posible_states.append(('replacement_order', 'Warten auf Ersatzteil'))
        posible_states.append(('pickup', 'Warten auf Abholung'))
        return posible_states

    if current_state == "pickup":
        posible_states.append(('closed', 'Abgeschlossen'))
        return posible_states

    if current_state == "replacement_order":
        posible_states.append(('under_repair', 'In Reparatur'))
        return posible_states

    if current_state == "under_repair":
        posible_states.append(('taken_home', 'Gerät mitgenommen'))
        posible_states.append(('inform_customer', 'Kunde informieren'))
        return posible_states

    if current_state == "taken_home":
        posible_states.append(('under_repair', 'In Reparatur'))
        return posible_states
    