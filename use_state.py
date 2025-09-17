"""
1.  A "memória interna" do React, onde será guardado os estados.
A estrutura será :{ 'id_componente': [estado1, estado2, ...] }
"""

__react_internal_memory = {}
__current_component_id = None
__hook_index = 0


def render(component_function, component_id):
    """
    Simula a renderização de um componente React.
    """
    global __current_component_id, __hook_index
    __current_component_id = component_id
    __hook_index = 0
    
    print(f"\n--- Renderizando componente '{component_id}' ---")
    component_function()
    print(f"--- Renderização de '{component_id}' concluída ---\n")


def useState(initial_value):
    """
    Usa memória global para buscar ou inicializar o estado,
    baseado na ordem de chamada.
    """
    global __hook_index
    
    component_states = __react_internal_memory.setdefault(__current_component_id, [])
    
    if __hook_index >= len(component_states):
        component_states.append(initial_value)
        
    current_value = component_states[__hook_index]
    
    def create_setter(component_id_for_closure, index_for_closure):
        def set_state(new_value):
            print(f"  -> `set_state` chamado para '{component_id_for_closure}' no índice {index_for_closure}. Valor mudou para: {new_value}")
            __react_internal_memory[component_id_for_closure][index_for_closure] = new_value
        
        return set_state
    
    setter = create_setter(__current_component_id, __hook_index)
    
    __hook_index += 1
    
    return [current_value, setter]


# --- Uso do useState ---
def CounterComponent():
    
    count, set_count = useState(0)
    name, set_name = useState("Visitante")
    
    print(f"---- Componente executado: Olá, {name} a contagem é {count} ----")
    
    if count < 2:
        set_count(count + 1) # aqui chama a funcao interna que altera o estado (set_state)
        
    if count == 1 and name == "Visitante":
        set_name("Desenvolvedor Python")
    
    if count == 2:
        set_name("Usuário Avançado")
        
        
if __name__ == "__main__":
    # --- Simulação do Ciclo de Vida ---
    print("Iniciando simulação do ciclo de vida do componente com useState...\n")
    print("Memória inicial:", __react_internal_memory)
    
    # 1. Primeira renderização
    print("\n--- Primeira renderização ---")
    render(CounterComponent, 'meuContador')
    print("Memória após primeira renderização:", __react_internal_memory)
    
    # `set_count(1)` foi chamado. Vamos simular a re-renderização que o React faria.
    # 2. Segunda renderização
    print("\n--- Segunda renderização ---")
    render(CounterComponent, 'meuContador')
    print("Memória após segunda renderização:", __react_internal_memory)
    
    # `set_count(2)` e `set_name("...")` foram chamados. Vamos simular a próxima renderização.
    # 3. Terceira renderização
    print("\n--- Terceira renderização ---")
    render(CounterComponent, 'meuContador')
    print("Memória após terceira renderização:", __react_internal_memory)
    
    # Agora, o estado está estável (count não é mais < 2), então não haverá mais chamadas de `set_state`.
    # Se renderizarmos de novo, os valores serão os mesmos.
    print("\n--- Quarta renderização ---")
    print("\n--- Verificação de estabilidade ---")
    render(CounterComponent, 'meuContador')
    print("Memória após quarta renderização:", __react_internal_memory)
    
    # Vamos ver como a memória ficou no final
    print("\nEstado final na memória interna do 'React':")
    print(__react_internal_memory)