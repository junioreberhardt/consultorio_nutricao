(function () {

    /* ===================================================== */
    /* ESTADO DA EDIÇÃO                                      */
    /* ===================================================== */

    let avaliacaoEmEdicao = null;


    /* ===================================================== */
    /* EDIÇÃO DE AVALIAÇÕES                                  */
    /* ===================================================== */

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


    /* ===================================================== */
    /* EVOLUÇÃO ANTROPOMÉTRICA                               */
    /* ===================================================== */

    const dadosContainer =
        document.getElementById(
            "dados-avaliacao-fisica"
        );


    const periodoSelect =
        document.getElementById(
            "periodo-evolucao"
        );


    const dataInicialSelect =
        document.getElementById(
            "data-inicial-evolucao"
        );


    const dataFinalSelect =
        document.getElementById(
            "data-final-evolucao"
        );


    const erroContainer =
        document.getElementById(
            "erro-evolucao"
        );


    const resumoContainer =
        document.getElementById(
            "resumo-evolucao"
        );


    const graficoContainer =
        document.getElementById(
            "grafico-evolucao"
        );


    const botoesIndicadores =
        document.querySelectorAll(
            ".indicador-evolucao"
        );


    const configuracoes = {

        peso: {
            nome: "Peso",
            unidade: "kg",
            casas: 1
        },

        imc: {
            nome: "IMC",
            unidade: "",
            casas: 1
        },

        gordura: {
            nome: "Gordura",
            unidade: "%",
            casas: 1
        },

        massa_magra: {
            nome: "Massa magra",
            unidade: "%",
            casas: 1
        },

        cintura: {
            nome: "Cintura",
            unidade: "cm",
            casas: 1
        }

    };


    let indicadorSelecionado = "peso";


    function formatarNumero(valor, casas) {

        return Number(valor).toLocaleString(
            "pt-BR",
            {
                minimumFractionDigits: casas,
                maximumFractionDigits: casas
            }
        );

    }


    function formatarValor(indicador, valor) {

        const configuracao =
            configuracoes[indicador];


        if (
            !configuracao ||
            !Number.isFinite(valor)
        ) {

            return "—";

        }


        const numero =
            formatarNumero(
                valor,
                configuracao.casas
            );


        if (configuracao.unidade === "") {

            return numero;

        }


        return (
            numero +
            " " +
            configuracao.unidade
        );

    }


    function mostrarErro(mensagem) {

        if (!erroContainer) {

            return;

        }


        erroContainer.textContent =
            mensagem;


        erroContainer.classList.remove(
            "hidden"
        );

    }


    function limparErro() {

        if (!erroContainer) {

            return;

        }


        erroContainer.textContent =
            "";


        erroContainer.classList.add(
            "hidden"
        );

    }


    function converterNumero(valor) {

        if (
            valor === null ||
            valor === undefined ||
            valor === ""
        ) {

            return null;

        }


        const numero =
            Number(valor);


        if (!Number.isFinite(numero)) {

            return null;

        }


        return numero;

    }


    function carregarAvaliacoes() {

        if (!dadosContainer) {

            return [];

        }


        const elementos =
            dadosContainer.querySelectorAll(
                ".avaliacao-grafico"
            );


        const avaliacoes = [];


        elementos.forEach(function (elemento) {

            const avaliacao = {

                data:
                    elemento.dataset.date,

                dataLabel:
                    elemento.dataset.dateLabel,

                peso:
                    converterNumero(
                        elemento.dataset.peso
                    ),

                imc:
                    converterNumero(
                        elemento.dataset.imc
                    ),

                gordura:
                    converterNumero(
                        elemento.dataset.gordura
                    ),

                massa_magra:
                    converterNumero(
                        elemento.dataset.massaMagra
                    ),

                cintura:
                    converterNumero(
                        elemento.dataset.cintura
                    )

            };


            avaliacoes.push(
                avaliacao
            );

        });


        avaliacoes.sort(function (a, b) {

            return a.data.localeCompare(
                b.data
            );

        });


        return avaliacoes;

    }


    const avaliacoes =
        carregarAvaliacoes();


    function preencherSelectDatas() {

        if (
            !dataInicialSelect ||
            !dataFinalSelect
        ) {

            return;

        }


        dataInicialSelect.innerHTML =
            "";


        dataFinalSelect.innerHTML =
            "";


        avaliacoes.forEach(function (avaliacao) {

            const opcaoInicial =
                document.createElement(
                    "option"
                );


            opcaoInicial.value =
                avaliacao.data;


            opcaoInicial.textContent =
                avaliacao.dataLabel;


            dataInicialSelect.appendChild(
                opcaoInicial
            );


            const opcaoFinal =
                document.createElement(
                    "option"
                );


            opcaoFinal.value =
                avaliacao.data;


            opcaoFinal.textContent =
                avaliacao.dataLabel;


            dataFinalSelect.appendChild(
                opcaoFinal
            );

        });


        if (avaliacoes.length > 1) {

            dataInicialSelect.value =
                avaliacoes[0].data;


            dataFinalSelect.value =
                avaliacoes[
                    avaliacoes.length - 1
                ].data;

        }

    }


    function obterAvaliacoesPeriodo() {

        if (!periodoSelect) {

            return [];

        }


        if (
            periodoSelect.value ===
            "inicio"
        ) {

            return avaliacoes;

        }


        const dataInicial =
            dataInicialSelect.value;


        const dataFinal =
            dataFinalSelect.value;


        if (
            !dataInicial ||
            !dataFinal
        ) {

            return [];

        }


        const resultado = [];


        avaliacoes.forEach(function (avaliacao) {

            if (
                avaliacao.data >= dataInicial &&
                avaliacao.data <= dataFinal
            ) {

                resultado.push(
                    avaliacao
                );

            }

        });


        return resultado;

    }


    function obterAvaliacoesComIndicador(
        avaliacoesPeriodo
    ) {

        const resultado = [];


        avaliacoesPeriodo.forEach(
            function (avaliacao) {

                const valor =
                    avaliacao[
                    indicadorSelecionado
                    ];


                if (Number.isFinite(valor)) {

                    resultado.push(
                        avaliacao
                    );

                }

            }
        );


        return resultado;

    }


    function atualizarEstadoDatas() {

        if (
            !periodoSelect ||
            !dataInicialSelect ||
            !dataFinalSelect
        ) {

            return;

        }


        const personalizado =
            periodoSelect.value ===
            "personalizado";


        if (personalizado) {

            dataInicialSelect.classList.remove(
                "hidden"
            );


            dataFinalSelect.classList.remove(
                "hidden"
            );


            dataInicialSelect.disabled =
                false;


            dataFinalSelect.disabled =
                false;

        } else {

            dataInicialSelect.classList.add(
                "hidden"
            );


            dataFinalSelect.classList.add(
                "hidden"
            );


            dataInicialSelect.disabled =
                true;


            dataFinalSelect.disabled =
                true;

        }


        atualizarGrafico();

    }


    function atualizarIndicadorVisual() {

        botoesIndicadores.forEach(
            function (botao) {

                const indicador =
                    botao.dataset.indicador;


                botao.classList.remove(

                    "bg-[var(--color-primary)]",

                    "text-white",

                    "border-[var(--color-primary)]",

                    "bg-[var(--color-surface)]",

                    "text-[var(--color-text-muted)]",

                    "border-[var(--color-border)]"

                );


                if (
                    indicador ===
                    indicadorSelecionado
                ) {

                    botao.classList.add(

                        "bg-[var(--color-primary)]",

                        "text-white",

                        "border-[var(--color-primary)]"

                    );

                } else {

                    botao.classList.add(

                        "bg-[var(--color-surface)]",

                        "text-[var(--color-text-muted)]",

                        "border-[var(--color-border)]"

                    );

                }

            }
        );

    }


    function criarGrafico(
        avaliacoesPeriodo
    ) {

        if (!graficoContainer) {

            return;

        }


        const configuracao =
            configuracoes[
            indicadorSelecionado
            ];


        if (!configuracao) {

            graficoContainer.innerHTML =
                "";


            return;

        }


        const avaliacoesComDados =
            obterAvaliacoesComIndicador(
                avaliacoesPeriodo
            );


        if (
            avaliacoesComDados.length < 2
        ) {

            graficoContainer.innerHTML =
                "";


            return;

        }


        const largura = 900;
        const altura = 320;

        const margemEsquerda = 60;
        const margemDireita = 25;
        const margemSuperior = 25;
        const margemInferior = 55;


        const larguraGrafico =
            largura -
            margemEsquerda -
            margemDireita;


        const alturaGrafico =
            altura -
            margemSuperior -
            margemInferior;


        let minimo = Infinity;
        let maximo = -Infinity;


        avaliacoesComDados.forEach(
            function (avaliacao) {

                const valor =
                    avaliacao[
                    indicadorSelecionado
                    ];


                if (!Number.isFinite(valor)) {

                    return;

                }


                if (valor < minimo) {

                    minimo = valor;

                }


                if (valor > maximo) {

                    maximo = valor;

                }

            }
        );


        if (
            !Number.isFinite(minimo) ||
            !Number.isFinite(maximo)
        ) {

            graficoContainer.innerHTML =
                "";


            mostrarErro(
                "Não existem dados suficientes para montar o gráfico."
            );


            return;

        }


        if (minimo === maximo) {

            minimo -= 1;
            maximo += 1;

        }


        const diferenca =
            maximo - minimo;


        minimo -=
            diferenca * 0.08;


        maximo +=
            diferenca * 0.08;


        function obterX(indice) {

            if (
                avaliacoesComDados.length === 1
            ) {

                return margemEsquerda;

            }


            return (
                margemEsquerda +
                (
                    indice /
                    (
                        avaliacoesComDados.length -
                        1
                    )
                ) *
                larguraGrafico
            );

        }


        function obterY(valor) {

            return (
                margemSuperior +
                (
                    1 -
                    (
                        (valor - minimo) /
                        (maximo - minimo)
                    )
                ) *
                alturaGrafico
            );

        }


        let svg = `
            <svg
                viewBox="0 0 ${largura} ${altura}"
                width="100%"
                height="320"
                role="img"
                aria-label="Evolução de ${configuracao.nome}"
                preserveAspectRatio="none"
            >
        `;


        for (
            let i = 0;
            i <= 4;
            i++
        ) {

            const y =
                margemSuperior +
                (i / 4) *
                alturaGrafico;


            const valor =
                maximo -
                (i / 4) *
                (maximo - minimo);


            svg += `
                <line
                    x1="${margemEsquerda}"
                    y1="${y}"
                    x2="${largura - margemDireita}"
                    y2="${y}"
                    stroke="var(--color-border)"
                    stroke-width="1"
                />

                <text
                    x="${margemEsquerda - 10}"
                    y="${y + 4}"
                    text-anchor="end"
                    font-size="10"
                    fill="var(--color-text-muted)"
                >
                    ${formatarNumero(
                valor,
                configuracao.casas
            )}${configuracao.unidade}
                </text>
            `;

        }


        avaliacoesComDados.forEach(
            function (avaliacao, indice) {

                const x =
                    obterX(indice);


                svg += `
                    <text
                        x="${x}"
                        y="${altura - 18}"
                        text-anchor="middle"
                        font-size="10"
                        fill="var(--color-text-muted)"
                    >
                        ${avaliacao.dataLabel}
                    </text>
                `;

            }
        );


        let caminho = "";


        avaliacoesComDados.forEach(
            function (avaliacao, indice) {

                const valor =
                    avaliacao[
                    indicadorSelecionado
                    ];


                if (!Number.isFinite(valor)) {

                    return;

                }


                const x =
                    obterX(indice);


                const y =
                    obterY(valor);


                if (caminho === "") {

                    caminho =
                        `M ${x} ${y}`;

                } else {

                    caminho +=
                        ` L ${x} ${y}`;

                }

            }
        );


        svg += `
            <path
                d="${caminho}"
                fill="none"
                stroke="var(--color-primary)"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
        `;


        avaliacoesComDados.forEach(
            function (avaliacao, indice) {

                const valor =
                    avaliacao[
                    indicadorSelecionado
                    ];


                if (!Number.isFinite(valor)) {

                    return;

                }


                const x =
                    obterX(indice);


                const y =
                    obterY(valor);


                svg += `
                    <circle
                        cx="${x}"
                        cy="${y}"
                        r="4"
                        fill="var(--color-surface)"
                        stroke="var(--color-primary)"
                        stroke-width="2"
                    >
                        <title>
                            ${configuracao.nome} —
                            ${avaliacao.dataLabel} —
                            ${formatarValor(
                    indicadorSelecionado,
                    valor
                )}
                        </title>
                    </circle>
                `;

            }
        );


        svg += `
            </svg>
        `;


        graficoContainer.innerHTML =
            svg;

    }


    function atualizarResumo(
        avaliacoesPeriodo
    ) {

        if (!resumoContainer) {

            return;

        }


        resumoContainer.innerHTML =
            "";


        const configuracao =
            configuracoes[
            indicadorSelecionado
            ];


        const avaliacoesComDados =
            obterAvaliacoesComIndicador(
                avaliacoesPeriodo
            );


        if (
            avaliacoesComDados.length < 2
        ) {

            return;

        }


        const primeiro =
            avaliacoesComDados[0][
            indicadorSelecionado
            ];


        const ultimo =
            avaliacoesComDados[
            avaliacoesComDados.length - 1
            ][
            indicadorSelecionado
            ];


        const primeiroExibido =
            Number(
                primeiro.toFixed(
                    configuracao.casas
                )
            );


        const ultimoExibido =
            Number(
                ultimo.toFixed(
                    configuracao.casas
                )
            );


        const diferencaExibida =
            Number(
                (
                    ultimoExibido -
                    primeiroExibido
                ).toFixed(
                    configuracao.casas
                )
            );


        let variacao = "—";


        if (diferencaExibida > 0) {

            variacao =
                `↑ ${formatarValor(
                    indicadorSelecionado,
                    diferencaExibida
                )}`;

        } else if (diferencaExibida < 0) {

            variacao =
                `↓ ${formatarValor(
                    indicadorSelecionado,
                    Math.abs(
                        diferencaExibida
                    )
                )}`;

        }


        const bloco =
            document.createElement(
                "div"
            );


        bloco.className = `
            rounded-lg
            border
            border-[var(--color-border)]
            bg-[var(--color-surface)]
            px-3
            py-3
        `;


        bloco.innerHTML = `
            <div class="
                flex
                flex-col
                sm:flex-row
                sm:items-center
                sm:justify-between
                gap-2
            ">
                <div>
                    <span class="
                        text-[10px]
                        font-semibold
                        uppercase
                        tracking-wide
                        text-[var(--color-text-muted)]
                    ">
                        ${configuracao.nome}
                    </span>

                    <div class="
                        mt-1
                        flex
                        items-baseline
                        gap-2
                    ">
                        <span class="
                            text-sm
                            font-semibold
                            text-[var(--color-text)]
                        ">
                            ${formatarValor(
            indicadorSelecionado,
            primeiro
        )}
                        </span>

                        <span class="
                            text-[10px]
                            text-[var(--color-text-subtle)]
                        ">
                            →
                        </span>

                        <span class="
                            text-sm
                            font-semibold
                            text-[var(--color-text)]
                        ">
                            ${formatarValor(
            indicadorSelecionado,
            ultimo
        )}
                        </span>
                    </div>
                </div>

                <div class="
                    text-left
                    sm:text-right
                ">
                    <p class="
                        text-[10px]
                        text-[var(--color-text-muted)]
                    ">
                        Variação no período
                    </p>

                    <p class="
                        mt-0.5
                        text-xs
                        font-medium
                        text-[var(--color-text)]
                    ">
                        ${variacao}
                    </p>
                </div>
            </div>
        `;


        resumoContainer.appendChild(
            bloco
        );

    }


    function atualizarGrafico() {

        if (
            !graficoContainer ||
            !periodoSelect
        ) {

            return;

        }


        limparErro();


        const avaliacoesPeriodo =
            obterAvaliacoesPeriodo();


        if (
            periodoSelect.value ===
            "personalizado" &&
            dataInicialSelect.value >=
            dataFinalSelect.value
        ) {

            if (resumoContainer) {

                resumoContainer.innerHTML =
                    "";

            }


            graficoContainer.innerHTML =
                "";


            mostrarErro(
                "A data inicial precisa ser anterior à data final."
            );


            return;

        }


        const avaliacoesComDados =
            obterAvaliacoesComIndicador(
                avaliacoesPeriodo
            );


        if (
            avaliacoesComDados.length < 2
        ) {

            if (resumoContainer) {

                resumoContainer.innerHTML =
                    "";

            }


            graficoContainer.innerHTML =
                "";


            const configuracao =
                configuracoes[
                indicadorSelecionado
                ];


            if (configuracao) {

                mostrarErro(
                    `Não há avaliações suficientes com dados de ${configuracao.nome} no período selecionado. É necessário ter pelo menos duas avaliações com esse indicador preenchido.`
                );

            }


            return;

        }


        atualizarResumo(
            avaliacoesPeriodo
        );


        criarGrafico(
            avaliacoesPeriodo
        );

    }


    /* ===================================================== */
    /* EVENTOS                                               */
    /* ===================================================== */

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


                abrirEdicao(
                    avaliacaoId
                );


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


                cancelarEdicao(
                    avaliacaoId
                );

            }

        }
    );


    /* ===================================================== */
    /* EVENTOS DA EVOLUÇÃO                                   */
    /* ===================================================== */

    botoesIndicadores.forEach(
        function (botao) {

            botao.addEventListener(
                "click",
                function () {

                    indicadorSelecionado =
                        botao.dataset.indicador;


                    limparErro();


                    atualizarIndicadorVisual();


                    atualizarGrafico();

                }
            );

        }
    );


    if (periodoSelect) {

        periodoSelect.addEventListener(
            "change",
            atualizarEstadoDatas
        );

    }


    if (dataInicialSelect) {

        dataInicialSelect.addEventListener(
            "change",
            atualizarGrafico
        );

    }


    if (dataFinalSelect) {

        dataFinalSelect.addEventListener(
            "change",
            atualizarGrafico
        );

    }


    /* ===================================================== */
    /* INICIALIZAÇÃO                                         */
    /* ===================================================== */

    if (
        periodoSelect &&
        avaliacoes.length > 1
    ) {

        preencherSelectDatas();


        atualizarIndicadorVisual();


        atualizarEstadoDatas();

    } else if (
        botoesIndicadores.length > 0
    ) {

        atualizarIndicadorVisual();

    }


})();