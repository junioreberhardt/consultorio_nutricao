document.addEventListener("DOMContentLoaded", () => {

    const telefone = document.getElementById("telefone");

    if (!telefone) return;


    function somenteNumeros(valor) {
        return valor.replace(/\D/g, "").slice(0, 11);
    }


    function formatarTelefone(numeros) {

        if (!numeros) {
            return "";
        }

        // Apenas DDD
        if (numeros.length <= 2) {
            return `(${numeros}`;
        }

        // DDD + início do número
        if (numeros.length <= 6) {
            return `(${numeros.slice(0, 2)}) ${numeros.slice(2)}`;
        }

        // Telefone fixo
        if (numeros.length <= 10) {
            return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 6)}-${numeros.slice(6)}`;
        }

        // Celular
        return `(${numeros.slice(0, 2)}) ${numeros.slice(2, 7)}-${numeros.slice(7)}`;
    }


    function quantidadeDeNumerosAntesDoCursor(valor, posicao) {

        return valor
            .slice(0, posicao)
            .replace(/\D/g, "")
            .length;
    }


    function posicaoDoCursor(valorFormatado, quantidadeNumeros) {

        if (quantidadeNumeros <= 0) {
            return 0;
        }

        let encontrados = 0;

        for (let i = 0; i < valorFormatado.length; i++) {

            if (/\d/.test(valorFormatado[i])) {
                encontrados++;

                if (encontrados === quantidadeNumeros) {
                    return i + 1;
                }
            }
        }

        return valorFormatado.length;
    }


    telefone.addEventListener("input", () => {

        const valorAnterior = telefone.value;

        const cursorAnterior = telefone.selectionStart;

        // Quantos números existiam antes do cursor
        const numerosAntesDoCursor =
            quantidadeDeNumerosAntesDoCursor(
                valorAnterior,
                cursorAnterior
            );

        // Remove tudo que não for número
        const numeros = somenteNumeros(valorAnterior);

        // Aplica a máscara
        const valorFormatado = formatarTelefone(numeros);

        telefone.value = valorFormatado;

        // Reposiciona o cursor
        const novaPosicao = posicaoDoCursor(
            valorFormatado,
            numerosAntesDoCursor
        );

        telefone.setSelectionRange(
            novaPosicao,
            novaPosicao
        );

    });


    // Formata o telefone existente ao abrir a edição
    if (telefone.value) {

        const numeros = somenteNumeros(telefone.value);

        telefone.value = formatarTelefone(numeros);

    }

});