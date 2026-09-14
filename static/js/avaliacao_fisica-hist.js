
(function () {

    let avaliacaoEmEdicao = null;


    function esconderTodasAsEdicoes() {

        const elementosEdicao =
            document.querySelectorAll("[data-edit]");


        elementosEdicao.forEach(function (elemento) {

            elemento.classList.add("hidden");

        });


        const elementosVisualizacao =
            document.querySelectorAll("[data-view]");


        elementosVisualizacao.forEach(function (elemento) {

            elemento.classList.remove("hidden");

        });

    }


    function removerObservacaoDinamica() {

        const linhas =
            document.querySelectorAll(
                "[data-observacoes-row-dinamica]"
            );


        linhas.forEach(function (linha) {

            linha.remove();

        });

    }


    function criarObservacaoDinamica(avaliacaoId) {

        removerObservacaoDinamica();


        const modelo =
            document.getElementById(
                "modelo-observacao-avaliacao"
            );


        const linhaAvaliacao =
            document.getElementById(
                "avaliacao-" + avaliacaoId
            );


        const formulario =
            document.getElementById(
                "form-editar-avaliacao-" + avaliacaoId
            );


        if (!modelo || !linhaAvaliacao || !formulario) {

            return null;

        }


        const linha =
            modelo.content.cloneNode(true);


        const linhaReal =
            linha.querySelector(
                "[data-observacoes-row-dinamica]"
            );


        const textarea =
            linha.querySelector(
                "[data-observacao-textarea]"
            );


        if (!linhaReal || !textarea) {

            return null;

        }


        textarea.id =
            "observacoes-" + avaliacaoId;


        textarea.name =
            "observacoes_clinicas";


        textarea.setAttribute(
            "form",
            "form-editar-avaliacao-" + avaliacaoId
        );


        linhaAvaliacao.after(linha);


        return document.getElementById(
            "observacoes-" + avaliacaoId
        );

    }


    function encontrarObservacaoExistente(avaliacaoId) {

        return document.querySelector(
            '[data-observacoes-row="' + avaliacaoId + '"]'
        );

    }


    function atualizarImcEdicao(avaliacaoId) {

        const inputPeso =
            document.getElementById(
                "peso-edicao-" + avaliacaoId
            );


        const inputAltura =
            document.getElementById(
                "altura-edicao-" + avaliacaoId
            );


        const campoImc =
            document.getElementById(
                "imc-edicao-" + avaliacaoId
            );


        if (!inputPeso || !inputAltura || !campoImc) {

            return;

        }


        const peso =
            parseFloat(inputPeso.value);


        const alturaCm =
            parseFloat(inputAltura.value);


        if (
            !Number.isFinite(peso) ||
            !Number.isFinite(alturaCm) ||
            peso <= 0 ||
            alturaCm <= 0
        ) {

            campoImc.textContent = "—";

            return;

        }


        const alturaMetros =
            alturaCm / 100;


        const imc =
            peso / (alturaMetros * alturaMetros);


        if (!Number.isFinite(imc)) {

            campoImc.textContent = "—";

            return;

        }


        campoImc.textContent =
            imc.toFixed(1);

    }


    function abrirEdicao(avaliacaoId) {

        esconderTodasAsEdicoes();


        removerObservacaoDinamica();


        const observacaoExistente =
            encontrarObservacaoExistente(
                avaliacaoId
            );


        let textarea = null;


        if (observacaoExistente) {

            const elementosVisualizacao =
                observacaoExistente.querySelectorAll(
                    "[data-view]"
                );


            elementosVisualizacao.forEach(function (elemento) {

                elemento.classList.add("hidden");

            });


            const elementosEdicao =
                observacaoExistente.querySelectorAll(
                    "[data-edit]"
                );


            elementosEdicao.forEach(function (elemento) {

                elemento.classList.remove("hidden");

            });


            textarea =
                observacaoExistente.querySelector(
                    "textarea"
                );

        } else {

            textarea =
                criarObservacaoDinamica(
                    avaliacaoId
                );

        }


        const elementosVisualizacao =
            document.querySelectorAll(
                '[data-view="' + avaliacaoId + '"]'
            );


        elementosVisualizacao.forEach(function (elemento) {

            elemento.classList.add("hidden");

        });


        const elementosEdicao =
            document.querySelectorAll(
                '[data-edit="' + avaliacaoId + '"]'
            );


        elementosEdicao.forEach(function (elemento) {

            elemento.classList.remove("hidden");

        });


        avaliacaoEmEdicao =
            avaliacaoId;


        atualizarImcEdicao(
            avaliacaoId
        );


        if (textarea) {

            textarea.focus();

        }


        const linha =
            document.getElementById(
                "avaliacao-" + avaliacaoId
            );


        if (linha) {

            linha.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

        }

    }


    function cancelarEdicao(avaliacaoId) {

        const observacaoExistente =
            encontrarObservacaoExistente(
                avaliacaoId
            );


        if (observacaoExistente) {

            const textarea =
                observacaoExistente.querySelector(
                    "textarea"
                );


            if (textarea) {

                textarea.value =
                    textarea.defaultValue;

            }

        }


        esconderTodasAsEdicoes();


        removerObservacaoDinamica();


        avaliacaoEmEdicao = null;

    }


    document.addEventListener(
        "input",
        function (evento) {

            const elemento =
                evento.target;


            if (
                elemento.matches(
                    "[data-imc-peso]"
                ) ||
                elemento.matches(
                    "[data-imc-altura]"
                )
            ) {

                const avaliacaoId =
                    elemento.dataset.imcPeso ||
                    elemento.dataset.imcAltura;


                if (avaliacaoId) {

                    atualizarImcEdicao(
                        avaliacaoId
                    );

                }

            }

        }
    );


    document.addEventListener(
        "click",
        function (evento) {

            const botaoEditar =
                evento.target.closest(
                    "[data-editar-avaliacao]"
                );


            if (botaoEditar) {

                evento.preventDefault();


                const avaliacaoId =
                    botaoEditar.dataset.editarAvaliacao;


                abrirEdicao(avaliacaoId);


                return;

            }


            const botaoCancelar =
                evento.target.closest(
                    "[data-cancelar-avaliacao]"
                );


            if (botaoCancelar) {

                evento.preventDefault();


                const avaliacaoId =
                    botaoCancelar.dataset.cancelarAvaliacao;


                cancelarEdicao(avaliacaoId);

            }

        }
    );

})();