document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("form-busca-pacientes");

    const campoBusca =
        document.getElementById("campo-busca-pacientes");

    const areaPacientes =
        document.getElementById("area-pacientes");

    if (!form || !campoBusca || !areaPacientes) {
        return;
    }

    let temporizador = null;
    let requisicaoAtual = null;

    function obterSelectQuantidade() {
        return document.getElementById("quantidade-pacientes");
    }

    function obterQuantidadeAtual() {

        const selectQuantidade =
            obterSelectQuantidade();

        if (!selectQuantidade) {
            return "20";
        }

        return selectQuantidade.value;
    }

    async function atualizarPacientes(
        url,
        manterFocus = true
    ) {

        if (requisicaoAtual) {
            requisicaoAtual.abort();
        }

        requisicaoAtual =
            new AbortController();

        const posicaoScroll =
            window.scrollY;

        try {

            const resposta =
                await fetch(
                    url,
                    {
                        method: "GET",
                        headers: {
                            "X-Requested-With":
                                "XMLHttpRequest"
                        },
                        signal:
                            requisicaoAtual.signal
                    }
                );

            if (!resposta.ok) {
                throw new Error(
                    "Não foi possível carregar os pacientes."
                );
            }

            const html =
                await resposta.text();

            const documento =
                new DOMParser().parseFromString(
                    html,
                    "text/html"
                );

            const novaArea =
                documento.getElementById(
                    "area-pacientes"
                );

            if (!novaArea) {
                throw new Error(
                    "Área de pacientes não encontrada."
                );
            }

            areaPacientes.innerHTML =
                novaArea.innerHTML;

            window.history.replaceState(
                {},
                "",
                url
            );

            configurarPaginacao();
            configurarQuantidade();
            configurarBotaoLimpar();

            window.scrollTo(
                0,
                posicaoScroll
            );

            if (manterFocus) {

                campoBusca.focus();

                const tamanho =
                    campoBusca.value.length;

                campoBusca.setSelectionRange(
                    tamanho,
                    tamanho
                );
            }

        } catch (erro) {

            if (erro.name === "AbortError") {
                return;
            }

            console.error(
                "Erro ao atualizar pacientes:",
                erro
            );
        }
    }

    function criarUrlBusca() {

        const busca =
            campoBusca.value.trim();

        const quantidade =
            obterQuantidadeAtual();

        const url =
            new URL(
                form.action,
                window.location.origin
            );

        if (busca) {

            url.searchParams.set(
                "busca",
                busca
            );
        }

        url.searchParams.set(
            "pagina",
            "1"
        );

        url.searchParams.set(
            "por_pagina",
            quantidade
        );

        return url.toString();
    }

    campoBusca.addEventListener(
        "input",
        () => {

            clearTimeout(
                temporizador
            );

            temporizador =
                setTimeout(
                    () => {

                        atualizarPacientes(
                            criarUrlBusca()
                        );

                    },
                    250
                );
        }
    );

    form.addEventListener(
        "submit",
        (event) => {

            event.preventDefault();

            clearTimeout(
                temporizador
            );

            atualizarPacientes(
                criarUrlBusca()
            );
        }
    );

    function configurarPaginacao() {

        const links =
            areaPacientes.querySelectorAll(
                ".link-paginacao"
            );

        links.forEach((link) => {

            link.addEventListener(
                "click",
                (event) => {

                    event.preventDefault();

                    atualizarPacientes(
                        link.href,
                        false
                    );
                }
            );
        });
    }

    function configurarQuantidade() {

        const selectQuantidade =
            obterSelectQuantidade();

        if (!selectQuantidade) {
            return;
        }

        selectQuantidade.addEventListener(
            "change",
            () => {

                const quantidade =
                    selectQuantidade.value;

                const busca =
                    campoBusca.value.trim();

                const url =
                    new URL(
                        form.action,
                        window.location.origin
                    );

                if (busca) {

                    url.searchParams.set(
                        "busca",
                        busca
                    );
                }

                url.searchParams.set(
                    "pagina",
                    "1"
                );

                url.searchParams.set(
                    "por_pagina",
                    quantidade
                );

                atualizarPacientes(
                    url.toString(),
                    false
                );
            }
        );
    }

    function configurarBotaoLimpar() {

        const botaoLimpar =
            document.getElementById(
                "limpar-busca-pacientes"
            );

        if (!botaoLimpar) {
            return;
        }

        botaoLimpar.addEventListener(
            "click",
            () => {

                campoBusca.value = "";

                const quantidade =
                    obterQuantidadeAtual();

                const url =
                    new URL(
                        form.action,
                        window.location.origin
                    );

                url.searchParams.set(
                    "pagina",
                    "1"
                );

                url.searchParams.set(
                    "por_pagina",
                    quantidade
                );

                atualizarPacientes(
                    url.toString()
                );
            }
        );
    }

    configurarPaginacao();
    configurarQuantidade();
    configurarBotaoLimpar();
});