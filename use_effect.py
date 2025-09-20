"""
1.  A "memória interna" do React, onde será guardado os estados.
A estrutura será :{ 'id_componente': [estado1, estado2, ...] }
"""

__react_internal_memory = {}
__effect_memory = {}
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

    component_effects = __effect_memory.setdefault(__current_component_id, {})

    component_effects[__hook_index] = {
        "callback": callback,
        "dependencies": dependencies,
    }
    __hook_index += 1


def render(component_function, component_id):
    """
    Simula a renderização de um componente React.
    """
    global __current_component_id, __hook_index
    __current_component_id = component_id
    __hook_index = 0

    __effect_memory.pop(component_id, None)

    print(f"\n--- Renderizando componente '{component_id}' ---")
    component_function()
    print(f"--- Renderização de '{component_id}' concluída ---\n")

    effects_to_run = __effect_memory.get(component_id, {})

    component_prev_deps = __previous_dependencies.setdefault(component_id, {})
    component_cleanups = __cleanup_functions.setdefault(component_id, {})

    for index, effect_data in effects_to_run.items():
        callback = effect_data["callback"]
        deps = effect_data["dependencies"]

        old_deps = component_prev_deps.get(index)

        should_run = False
        if old_deps is None:
            should_run = True
            print(f"  -> Efeito no índice {index} será executado (primeira vez).")
        elif deps is None:
            should_run = True
            print(f"  -> Efeito no índice {index} será executado (sem dependências).")
        elif deps != old_deps:
            should_run = True
            print(
                f"  -> Efeito no índice {index} será executado (dependências mudaram)."
            )
        else:
            print(
                f"  -> Efeito no índice {index} não será executado (dependências não mudaram)."
            )

        if should_run:
            if index in component_cleanups:
                print(
                    f"    -> Função de limpeza do efeito no índice {index} será executada."
                )
                component_cleanups[index]()

            print(f"    -> Executando o callback do efeito no índice {index}.")
            cleanup_function = callback()

            if callable(cleanup_function):
                component_cleanups[index] = cleanup_function

            component_prev_deps[index] = deps


def MeuComponenteComEfeitos():
    count, set_count = useState(0)

    print(f"   Componente executado. Estado atual: count = {count}")

    # Efeito 1: Roda apenas uma vez (como um componentDidMount)
    useEffect(
        lambda: print(
            "      >> EFEITO 1: Componente montado! Isto só aparece uma vez."
        ),
        [],  # Lista de dependências vazia
    )

    # Efeito 2: Roda sempre que o `count` mudar
    def efeito_do_contador():
        print(f"      >> EFEITO 2: O contador foi atualizado para {count}.")

        # Este efeito retorna uma função de limpeza
        def cleanup():
            print(
                f"      << CLEANUP 2: Limpando o efeito do contador (quando o valor era {count})."
            )

        return cleanup

    useEffect(
        efeito_do_contador,
        [count],  # Depende do estado `count`
    )


# --- SIMULAÇÃO DO CICLO DE VIDA ---

# 1. PRIMEIRA RENDERIZAÇÃO
print("=" * 20, "PRIMEIRA RENDERIZAÇÃO", "=" * 20)
render(MeuComponenteComEfeitos, "componente1")

# 2. ATUALIZANDO O ESTADO E RENDERIZANDO NOVAMENTE
print("\n" + "=" * 20, "ATUALIZANDO ESTADO PARA 5", "=" * 20)
# Na vida real, chamar set_count(5) agendaria o re-render. Aqui fazemos manualmente.
__react_internal_memory["componente1"][0] = 5
render(MeuComponenteComEfeitos, "componente1")

# 3. RENDERIZANDO DE NOVO SEM MUDAR O ESTADO
print("\n" + "=" * 20, "RENDERIZANDO SEM MUDANÇA", "=" * 20)
render(MeuComponenteComEfeitos, "componente1")
