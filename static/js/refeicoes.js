/**
 * SISTEMA NUTRIR MELHOR - GERENCIADOR VISUAL DE REFEIÇÕES
 */

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================================
    // ELEMENTOS
    // ==========================================================

    const btnNovaRefeicao =
        document.getElementById("btn-nova-refeicao");

    const painelAddRef =
        document.getElementById("painel-add-ref");

    const btnAddRefeicao =
        document.getElementById("btn-add-refeicao-inline");

    const inputNome =
        document.getElementById("nova-ref-nome");

    const inputHorario =
        document.getElementById("nova-ref-horario");

    const wrapperRefeicoes =
        document.getElementById("wrapper-refeicoes");


    let refeicoesSalvas = [];


    // ==========================================================
    // MÁSCARA AUTOMÁTICA DE HORÁRIO
    // ==========================================================

    if (inputHorario) {

        inputHorario.addEventListener("input", (e) => {

            let valor =
                e.target.value
                    .replace(/\D/g, "")
                    .slice(0, 4);


            if (valor.length > 2) {

                valor =
                    valor.slice(0, 2) +
                    ":" +
                    valor.slice(2);
            }


            e.target.value = valor;
        });
    }


    // ==========================================================
    // RENDERIZADOR DE REFEIÇÕES
    // ==========================================================

    function renderizarRefeicoes() {

        if (!wrapperRefeicoes) {
            return;
        }


        wrapperRefeicoes.innerHTML = "";


        refeicoesSalvas
            .sort((a, b) =>
                a.horario.localeCompare(b.horario)
            )
            .forEach((ref) => {

                const cardHtml = `

                    <div class="border border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50 rounded-xl p-4 shadow-sm hover:shadow-md transition duration-200">

                        <div class="flex items-center justify-between mb-3">

                            <span class="text-sm font-bold text-gray-700 dark:text-gray-300 flex items-center gap-x-2">

                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>

                                ${ref.nome}

                            </span>


                            <span class="inline-flex items-center gap-x-1 py-0.5 px-2 rounded-full text-xs font-mono font-medium bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-100/40">

                                ⏰ ${ref.horario}

                            </span>

                        </div>


                        <div class="border border-dashed border-gray-200 dark:border-gray-700 rounded-xl p-4 text-center text-xs text-gray-400 hover:text-emerald-600 hover:bg-white dark:hover:bg-gray-800 transition cursor-pointer flex items-center justify-center gap-x-2">

                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="14"
                                height="14"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            >
                                <circle
                                    cx="12"
                                    cy="12"
                                    r="10"
                                />

                                <line
                                    x1="12"
                                    y1="8"
                                    x2="12"
                                    y2="16"
                                />

                                <line
                                    x1="8"
                                    y1="12"
                                    x2="16"
                                    y2="12"
                                />
                            </svg>

                            Clique para buscar e adicionar alimentos a esta refeição.

                        </div>

                    </div>
                `;


                wrapperRefeicoes.insertAdjacentHTML(
                    "beforeend",
                    cardHtml
                );
            });
    }


    // ==========================================================
    // NOVA REFEIÇÃO — ABRIR FORMULÁRIO
    // ==========================================================

    if (btnNovaRefeicao) {

        btnNovaRefeicao.addEventListener("click", () => {

            if (!painelAddRef) {
                return;
            }


            painelAddRef.classList.remove("hidden");

            inputNome?.focus();
        });
    }


    // ==========================================================
    // ADICIONAR REFEIÇÃO
    // ==========================================================

    if (btnAddRefeicao) {

        btnAddRefeicao.addEventListener("click", () => {

            const nome =
                inputNome?.value.trim();

            let horario =
                inputHorario?.value.trim();


            if (!nome || !horario) {

                alert(
                    "Preencha o nome e o horário da refeição."
                );

                return;
            }


            // Corrige 8:00 para 08:00
            if (
                horario.length === 4 &&
                horario.indexOf(":") === 1
            ) {

                horario =
                    `0${horario}`;
            }


            refeicoesSalvas.push({
                nome,
                horario
            });


            renderizarRefeicoes();


            if (inputNome) {
                inputNome.value = "";
            }


            if (inputHorario) {
                inputHorario.value = "";
            }


            painelAddRef?.classList.add("hidden");

        });
    }


    // ==========================================================
    // REFEIÇÃO INICIAL
    // ==========================================================

    refeicoesSalvas.push({
        nome: "Café da Manhã",
        horario: "08:00"
    });


    renderizarRefeicoes();

});