__react_internal_memory = {}
# __effect_memory = {}
# {'id_componente': {hook_index: {'callback': callback, 'dependencies': [...]}}}
__previous_dependencies = {}
__cleanup_functions = {}
__memo_cache = {}
__current_component_id = None
__hook_index = 0


def useState(initial_value):
    global __hook_index
    component_states = __react_internal_memory.setdefault(__current_component_id, {})

    if __hook_index not in component_states:
        component_states[__hook_index] = initial_value

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


def useCallback(callback_function, dependencies):
    global __hook_index
    component_data = __react_internal_memory.setdefault(__current_component_id, {})
    callback_data = component_data.get(__hook_index)

    if callback_data is None:
        component_data[__hook_index] = {
            "callback": callback_function,
            "dependencies": dependencies,
        }
        value_to_return = callback_function
    else:
        last_callback = callback_data["callback"]
        last_dependencies = callback_data["dependencies"]
        if dependencies == last_dependencies:
            value_to_return = last_callback
        else:
            component_data[__hook_index] = {
                "callback": callback_function,
                "dependencies": dependencies,
            }
            value_to_return = callback_function

    __hook_index += 1
    return value_to_return


def render(component_function, component_id):
    global __current_component_id, __hook_index
    __current_component_id = component_id
    __hook_index = 0

    print(f"\n--- Renderizando componente '{component_id}' ---")
    component_function()
    print(f"--- Renderização de '{component_id}' concluída ---\n")


# --- OTIMIZADOR `MEMO` SIMULADO ---
def memo(component_function):
    def memoized_component(props):
        component_id = props["component_id"]
        last_props = __memo_cache.get(component_id)

        # Compara as props atuais com as anteriores.
        # NOTA: Esta é uma comparação simples. O React faz uma comparação rasa (shallow compare).
        if last_props is not None and last_props == props:
            print(
                f"   [Memo] Componente Filho '{component_id}' pulou a renderização!"
            )
            return

        __memo_cache[component_id] = props
        component_function(props)

    return memoized_component


def Botao(props):
    """O componente filho que queremos otimizar."""
    print(f"   -- Botão '{props['text']}' renderizado.")


BotaoMemoizado = memo(Botao)


def PainelDeControle():
    """O componente pai que controla o estado."""
    count, _ = useState(0)
    theme, _ = useState("claro")

    print(f"   PAI renderizado. Tema: {theme}, Contagem: {count}")

    # Esta função é um NOVO objeto a cada renderização do PainelDeControle
    def handle_clique_normal():
        pass

    # Esta função só será um NOVO objeto se `count` mudar
    handle_clique_otimizado = useCallback(
        lambda: print("Callback otimizado executado!"), [count]
    )

    print(f"   ID da função normal:    {id(handle_clique_normal)}")
    print(f"   ID da função otimizada: {id(handle_clique_otimizado)}")

    BotaoMemoizado(
        {
            "component_id": "botao_normal",
            "text": "Sem Callback",
            "onClick": handle_clique_normal,
        }
    )
    BotaoMemoizado(
        {
            "component_id": "botao_otimizado",
            "text": "Com Callback",
            "onClick": handle_clique_otimizado,
        }
    )


# --- A SIMULAÇÃO ---
print("=" * 20, "1. RENDERIZAÇÃO INICIAL", "=" * 20)
render(PainelDeControle, "painel")

print("\n" + "=" * 20, "2. MUDANDO O TEMA (NÃO AFETA O CALLBACK)", "=" * 20)
__react_internal_memory["painel"][1] = "escuro"  # Muda o `theme`
render(PainelDeControle, "painel")

print("\n" + "=" * 20, "3. MUDANDO O CONTADOR (AFETA O CALLBACK)", "=" * 20)
__react_internal_memory["painel"][0] = 1  # Muda o `count`
render(PainelDeControle, "painel")
