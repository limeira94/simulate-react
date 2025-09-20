import time

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

    component_states = __react_internal_memory.setdefault(__current_component_id, {})

    if __hook_index >= len(component_states):
        component_states[__hook_index] = initial_value

    current_value = component_states[__hook_index]

    def create_setter(component_id_for_closure, index_for_closure):
        def set_state(new_value):
            __react_internal_memory[component_id_for_closure][index_for_closure] = (
                new_value
            )

        return set_state

    setter = create_setter(__current_component_id, __hook_index)

    __hook_index += 1

    return [current_value, setter]


def useMemo(creator_function, dependencies):
    global __hook_index

    component_memo = __react_internal_memory.setdefault(__current_component_id, {})

    memoized_data = component_memo.get(__hook_index)

    if memoized_data is None:
        new_value = creator_function()
        component_memo[__hook_index] = {
            "value": new_value,
            "dependencies": dependencies,
        }
        value_to_return = new_value
    else:
        last_value = memoized_data["value"]
        last_dependencies = memoized_data["dependencies"]

        if dependencies == last_dependencies:
            value_to_return = last_value
        else:
            new_value = creator_function()
            component_memo[__hook_index] = {
                "value": new_value,
                "dependencies": dependencies,
            }
            value_to_return = new_value

    __hook_index += 1
    return value_to_return


def render(component_function, component_id):
    global __current_component_id, __hook_index
    __current_component_id = component_id
    __hook_index = 0
    print(f"\n--- Renderizando componente '{component_id}' ---")
    component_function()
    print(f"--- Renderização de '{component_id}' concluída ---")


# --- NOSSO CENÁRIO DE TESTE ---


def calculo_muito_lento(num):
    """Uma função que simula um cálculo pesado e nos avisa quando é executada."""
    print(f"   😱 CÁLCULO LENTO EXECUTADO com o número {num}!")
    time.sleep(1)  # Pausa por 1 segundo para sentirmos o impacto
    return num * 2


def ComponenteComCalculoCaro():
    # Este estado é uma dependência do nosso cálculo
    count, set_count = useState(0)
    # Este estado NÃO é uma dependência
    theme, set_theme = useState("claro")

    # Usamos o useMemo para proteger a chamada da função lenta.
    # A função só será re-executada se `count` mudar.
    valor_calculado = useMemo(lambda: calculo_muito_lento(count), [count])

    print(
        f"   Componente renderizado. Tema: {theme}, Valor calculado: {valor_calculado}"
    )


# 3. A SIMULAÇÃO
# Cenário 1: Primeira renderização. O cálculo DEVE acontecer.
print("=" * 20, "1. RENDERIZAÇÃO INICIAL", "=" * 20)
render(ComponenteComCalculoCaro, "componenteMemo")

# Cenário 2: Mudando um estado que NÃO é dependência. O cálculo NÃO deve acontecer.
print("\n" + "=" * 20, "2. MUDANDO ESTADO NÃO RELACIONADO (TEMA)", "=" * 20)
# Simulando a chamada de `set_theme("escuro")`
__react_internal_memory["componenteMemo"][1] = "escuro"
render(ComponenteComCalculoCaro, "componenteMemo")

# Cenário 3: Mudando um estado que É a dependência. O cálculo DEVE acontecer de novo.
print("\n" + "=" * 20, "3. MUDANDO A DEPENDÊNCIA (COUNT)", "=" * 20)
# Simulando a chamada de `set_count(5)`
__react_internal_memory["componenteMemo"][0] = 1000
render(ComponenteComCalculoCaro, "componenteMemo")


print("\n" + "=" * 20, "4. MUDANDO A DEPENDÊNCIA (COUNT)", "=" * 20)
# Simulando a chamada de `set_count(5)`
__react_internal_memory["componenteMemo"][0] = 1000
render(ComponenteComCalculoCaro, "componenteMemo")


print("\n" + "=" * 20, "5. MUDANDO A DEPENDÊNCIA (COUNT)", "=" * 20)
# Simulando a chamada de `set_count(5)`
__react_internal_memory["componenteMemo"][0] = 0
render(ComponenteComCalculoCaro, "componenteMemo")
