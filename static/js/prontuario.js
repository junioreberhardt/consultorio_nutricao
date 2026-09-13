document.addEventListener("DOMContentLoaded", function () {
    configurarAbas();
    configurarEdicaoDadosGerais();
    configurarMascaraTelefone();
});


/* =========================================================
   ABAS
========================================================= */

function configurarAbas() {
    const abas = document.querySelectorAll("[data-hs-tab]");
    const paineis = document.querySelectorAll('[role="tabpanel"]');

    if (!abas.length) {
        return;
    }

    function removerMensagensFlash() {
        const mensagens = document.querySelectorAll(
            "[data-flash-mensagem]"
        );

        mensagens.forEach(function (mensagem) {
            mensagem.remove();
        });
    }

    function ativarAba(aba) {
        const alvo = aba.getAttribute("data-hs-tab");

        if (!alvo) {
            return;
        }

        paineis.forEach(function (painel) {
            painel.classList.add("hidden");
        });

        abas.forEach(function (item) {
            item.classList.remove(
                "text-[var(--color-primary)]",
                "border-[var(--color-primary)]"
            );

            item.classList.add(
                "text-[var(--color-text-muted)]",
                "border-transparent"
            );

            item.setAttribute("aria-selected", "false");
        });

        const painel = document.querySelector(alvo);

        if (painel) {
            painel.classList.remove("hidden");
        }

        aba.classList.remove(
            "text-[var(--color-text-muted)]",
            "border-transparent"
        );

        aba.classList.add(
            "text-[var(--color-primary)]",
            "border-[var(--color-primary)]"
        );

        aba.setAttribute("aria-selected", "true");
    }

    abas.forEach(function (aba) {
        aba.addEventListener("click", function (evento) {
            evento.preventDefault();

            removerMensagensFlash();

            ativarAba(aba);
        });
    });

    ativarAba(abas[0]);
}


/* =========================================================
   EDIÇÃO DOS DADOS GERAIS
========================================================= */

function configurarEdicaoDadosGerais() {
    const visualizacao = document.querySelector(
        "[data-dados-gerais-view]"
    );

    const edicao = document.querySelector(
        "[data-dados-gerais-edit]"
    );

    const botaoEditar = document.querySelector(
        "[data-editar-dados-gerais]"
    );

    const botaoCancelar = document.querySelector(
        "[data-cancelar-dados-gerais]"
    );

    if (
        !visualizacao ||
        !edicao ||
        !botaoEditar ||
        !botaoCancelar
    ) {
        return;
    }

    botaoEditar.addEventListener("click", function () {
        visualizacao.classList.add("hidden");
        edicao.classList.remove("hidden");
    });

    botaoCancelar.addEventListener("click", function () {
        edicao.classList.add("hidden");
        visualizacao.classList.remove("hidden");

        const mensagens = document.querySelectorAll(
            "[data-flash-mensagem]"
        );

        mensagens.forEach(function (mensagem) {
            mensagem.remove();
        });
    });
}


/* =========================================================
   MÁSCARA DE TELEFONE
========================================================= */

function configurarMascaraTelefone() {
    const campoTelefone = document.querySelector(
        "#dados-gerais-telefone"
    );

    if (!campoTelefone) {
        return;
    }

    campoTelefone.addEventListener(
        "input",
        function () {
            let valor = campoTelefone.value;

            valor = valor.replace(/\D/g, "");

            if (valor.length > 11) {
                valor = valor.substring(0, 11);
            }

            if (valor.length <= 10) {
                if (valor.length >= 7) {
                    valor =
                        "(" +
                        valor.substring(0, 2) +
                        ") " +
                        valor.substring(2, 6) +
                        "-" +
                        valor.substring(6);
                } else if (valor.length >= 3) {
                    valor =
                        "(" +
                        valor.substring(0, 2) +
                        ") " +
                        valor.substring(2);
                } else if (valor.length >= 1) {
                    valor = "(" + valor;
                }
            } else {
                valor =
                    "(" +
                    valor.substring(0, 2) +
                    ") " +
                    valor.substring(2, 7) +
                    "-" +
                    valor.substring(7);
            }

            campoTelefone.value = valor;
        }
    );
}