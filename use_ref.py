"""
1.  A "memória interna" do React, onde será guardado os estados.
A estrutura será :{ 'id_componente': [estado1, estado2, ...] }
"""

__react_internal_memory = {}
# __effect_memory = {}
# {'id_componente': {hook_index: {'callback': callback, 'dependencies': [...]}}}
__previous_dependencies = {}
__cleanup_functions = {}

__current_component_id = None
__hook_index = 0


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
            print(
                f"  -> `set_state` chamado para '{component_id_for_closure}' no índice {index_for_closure}. Valor mudou para: {new_value}"
            )
            __react_internal_memory[component_id_for_closure][index_for_closure] = (
                new_value
            )

        return set_state

    setter = create_setter(__current_component_id, __hook_index)
    __hook_index += 1
    return [current_value, setter]


def useEffect(callback, dependencies):
    global __hook_index

    component_effects = __react_internal_memory.setdefault(__current_component_id, {})

    component_effects[__hook_index] = {
        "callback": callback,
        "dependencies": dependencies,
    }
    __hook_index += 1


class RefObject:
    def __init__(self, initial_value=None):
        self.current = initial_value

    def __repr__(self):
        return f"<RefObject current={self.current}>"


def useRef(initial_value):
    global __hook_index

    component_data = __react_internal_memory.setdefault(__current_component_id, [])
    if __hook_index >= len(component_data):
        new_ref = RefObject(initial_value)
        component_data.append(new_ref)

    ref_object = component_data[__hook_index]

    __hook_index += 1
    return ref_object


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


def MeuComponenteComRef():
    render_count_ref = useRef(0)

    count, set_count = useState(0)

    input_ref = useRef(None)

    if input_ref.current is None:
        input_ref.current = {"type": "text", "value": ""}
        print("    -> Elemento DOM criado e anexado ao ref.")

    render_count_ref.current += 1

    print(
        f"    Componente executado.\n Estado: {count},\n contador de renders (do ref): {render_count_ref.current} "
    )


# --- SIMULAÇÃO DO CICLO DE VIDA ---

# 1. PRIMEIRA RENDERIZAÇÃO
print("=" * 20, "PRIMEIRA RENDERIZAÇÃO", "=" * 20)
render(MeuComponenteComRef, "componenteRef1")
print(__react_internal_memory["componenteRef1"])
# 2. ATUALIZANDO O ESTADO E RENDERIZANDO NOVAMENTE
print("\n" + "=" * 20, "ATUALIZANDO ESTADO PARA 10", "=" * 20)
# A chamada de set_count irá disparar o re-render
__react_internal_memory["componenteRef1"][1] = 10
render(MeuComponenteComRef, "componenteRef1")
print(__react_internal_memory["componenteRef1"])
# 3. RENDERIZANDO DE NOVO
print("\n" + "=" * 20, "ATUALIZANDO ESTADO PARA 20", "=" * 20)
__react_internal_memory["componenteRef1"][1] = 20
render(MeuComponenteComRef, "componenteRef1")

print("\n" + "=" * 20, "MEMÓRIA FINAL", "=" * 20)
print(__react_internal_memory["componenteRef1"])
