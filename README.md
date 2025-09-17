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