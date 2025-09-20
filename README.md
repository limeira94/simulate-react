# How React Hooks Work under the hood

This project implements a simple React application to demonstrate how hooks work in React. It includes examples of `useState`, `useEffect`, and custom hooks.
The idea is understand how hooks work in React under the hood.
I'm using python for create `useState` and others hooks.

### A lógica por tras do `useState` no React

o useState resolve em componentes de funçoes é como manter um valor (estado) entre as renderizações
Toda vez que a função é renderizado inicia do zero.

Como o React faz para persistir o estado?
1. Memória fora do componente - o React mantém uma estrutura de dados interna "cédula de memória" para cada componente
2. Associação por Ordem - quando você chama useState, o react não sabe o nome da sua variável de estado, em vez disso ele confia na ordem em que os hooks são chamados.
	- Por isso existe as regras dos hooks: não chame hooks dentro de laços, condições ou funções aninhadas.
3. A função `setState` - a segunda parte do array retornado por `useState` é uma função que faz duas coisas.
	- atualiza o valor do estado naquele "slot" na memória interna do React.
	- enfileira uma nova renderização para o componente, garantido que a interface do usuário seja atualizada com o novo valor.

## Lógica por trás do `useEffect` 
O useffect é formado por um `setup code` o return `cleanup code`  e uma `list dependencies`

O `useState` é a memória de um componente, o `useEffect` é a sua lista de tarefas pós renderização.

O `useEffect` permite agendar uma função (efeito) para ser executada depois que o componente ja foi renderizado na tela.
Os três principais uso:
- `useEffect(function, [])` - A lista vazia diz "Execute esta tarefa apenas uma vez, depois da primeira renderização".
- `useEffect(function, [var1, var2]` - a lista com dependência diz "execute esta tarefa depois da primeira render, e depois só execute novamente var1 ou var 2 se tiveram mudado"
- `useEffect(function)` - Sem lista, executa tarefa depois de toda e qualquer renderização

## Como funciona o `useRef`
Pense como uma caixa de ferramenta que você pode anexar seu componente.
O que quer que você guarde dentro dela, permanecerá lá entre as renderizações, o componente pode ser renderização diversas vezes mas o conteúdo continuará os mesmo.
Mudar um valor dentro do `useRef` não causa uma nova renderização

O `useRef` retorna um objeto com uma única propriedade `.current` é dentro do `ref.current` que o seu valor é armazenado

** Dois principais casos de uso**
1. Acessar elementos do DOM
2. Guardar valores mutáveis sem re-renderizar

### Tabela Comparativa: `useState` vs. `useRef`

| Característica              | `useState` (O Quadro Branco)                        | `useRef` (A Gaveta Secreta)                             |
| :-------------------------- | :-------------------------------------------------- | :------------------------------------------------------ |
| **Aciona Re-renderização?** | **Sim**, ao chamar a função `set...()`              | **Não**, ao modificar a propriedade `.current`          |
| **Como o valor é atualizado?**| Indiretamente, através da função `setState()`       | Diretamente, modificando `ref.current = novoValor`      |
| **Principal Caso de Uso** | Dados que afetam diretamente a interface (UI)       | Referências a elementos DOM ou dados internos (timers)  |
| **Valor Retornado** | Um array: `[valor, funcaoParaMudarOValor]`          | Um objeto: `{ current: valor }`                         |
| **Natureza** | Declarativa (pede ao React para mudar e re-renderizar)| Imperativa (muda o valor diretamente, sem avisar o React)|


## Lógica por trás do `useMemo`
O objetivo é otimização de desempenho

Imagine um componente precisa filtrar 10mil itens ou fazer cálculos pesados. Se esse cálculo for refeito toda vez que re renderizar a aplicação se tornará lentra.
Aplica o conceito de memoization
1. execute uma função e guarde o resultado
2. da próxima vez que a função for chamada com os mesmo argumentos simplesmente retorna o que guardou.


## Lógica `useCallback`
é um hook que memoiza a própria função

Retorna a mesma instância (o mesmo objeto) da função entre as renderizações a menos que uma de suas dependências tenha mudado.

```
// useCallback memoiza a função `minhaFuncao`
const memoizedCallback = useCallback(minhaFuncao, [a, b]);

// useMemo pode fazer a mesma coisa, mas memoizando o *retorno* da função externa,
// que neste caso é a própria `minhaFuncao`.
const memoizedCallback = useMemo(() => minhaFuncao, [a, b]);
```

Mesmo funcionamento por debaixo dos panos com o useMemo

A melhor forma de decidir é se perguntar:  O que eu estou tentando impedir que seja recriado a cada nova renderização?

### Tabela de Decisão Rápida: `useMemo` vs. `useCallback`

| Se você precisa... | Use `useMemo` | Use `useCallback` |
| :--- | :--- | :--- |
| Otimizar um **cálculo que demora**? | ✅ **Sim** | ❌ Não |
| Passar uma **função** para um filho com `React.memo`? | ❌ Não (sintaxe errada para isso) | ✅ **Sim** |
| O que você quer "salvar"? | O **resultado** de uma função (um valor, objeto, array) | A **própria função** (sua referência na memória) |

Cenários `useMemo`:
- Filtrar, ordenar ou mapear listas muito grandes
- Cálculos matemáticos ou de dados pesados
- gerar objetos ou arrays complexos

Cenários `useCallback`:
- Passar funções para componentes filhos otimizados com `React.memo`
- quando a função é uma dependência de outro hook como `useEffect`