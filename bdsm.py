from collections import defaultdict, deque

def minimize_dfa(states, alphabet, transitions, start_state, accept_states):
    # Ulaşılamayan durumların kaldırılması
    reachable = set()
    queue = deque([start_state])
    
    while queue:
        current = queue.popleft()
        reachable.add(current)
        for symbol in alphabet:
            next_state = transitions.get((current, symbol))
            if next_state and next_state not in reachable:
                queue.append(next_state)
    
    reachable_states = reachable
    transitions = {k: v for k, v in transitions.items() if k[0] in reachable_states}
    
    # Denk durumların birleştirilmesi
    non_accept_states = reachable_states - set(accept_states)
    partition = [set(accept_states), set(non_accept_states)]
    
    while True:
        new_partition = []
        for group in partition:
            subgroups = defaultdict(set)
            for state in group:
                key = tuple(transitions.get((state, symbol), None) in group for symbol in alphabet)
                subgroups[key].add(state)
            new_partition.extend(subgroups.values())
        if new_partition == partition:
            break
        partition = new_partition
    
    # Yeni durumların oluşturulması
    new_states = [frozenset(group) for group in partition]
    new_start_state = next(state for state in new_states if start_state in state)
    new_accept_states = [state for state in new_states if state & set(accept_states)]
    
    # Yeni geçişlerin oluşturulması
    new_transitions = {}
    for group in new_states:
        representative = next(iter(group))
        for symbol in alphabet:
            target = transitions.get((representative, symbol))
            if target:
                target_group = next(g for g in new_states if target in g)
                new_transitions[(group, symbol)] = target_group
    
    return new_states, new_transitions, new_start_state, new_accept_states

# Örnek DFA tanımı
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
alphabet = {'a', 'b'}
transitions = {
    ('q0', 'a'): 'q1', ('q0', 'b'): 'q3',
    ('q1', 'a'): 'q2', ('q1', 'b'): 'q4',
    ('q2', 'a'): 'q0', ('q2', 'b'): 'q5',
    ('q3', 'a'): 'q4', ('q3', 'b'): 'q5',
    ('q4', 'a'): 'q5', ('q4', 'b'): 'q0',
    ('q5', 'a'): 'q5', ('q5', 'b'): 'q5'
}
start_state = 'q0'
accept_states = {'q2', 'q4'}


# DFA'yı indirgeme
new_states, new_transitions, new_start_state, new_accept_states = minimize_dfa(
    states, alphabet, transitions, start_state, accept_states
)

# Sonuçları yazdırma
print("Yeni Durumlar:", new_states)
print("Yeni Geçişler:", new_transitions)
print("Yeni Başlangıç Durumu:", new_start_state)
print("Yeni Kabul Durumları:", new_accept_states)
