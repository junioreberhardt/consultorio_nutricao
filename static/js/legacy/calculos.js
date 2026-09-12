// static/js/calculos.js

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================================
    // ELEMENTOS
    // ==========================================================

    const formMetabolico =
        document.getElementById("form-metabolico");

    const painelResultados =
        document.getElementById("painel-resultados");

    const selectFormula =
        document.getElementById("formula");

    const grupoMassaMagra =
        document.getElementById("grupo-massa-magra");

    const inputMassaMagra =
        document.getElementById("massa-magra");

    const erroMassaMagra =
        document.getElementById("erro-massa-magra");

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
    // UTILITÁRIOS
    // ==========================================================

    function numero(id, padrao = 0) {

        const elemento =
            document.getElementById(id);

        if (!elemento) {
            return padrao;
        }

        const valor =
            elemento.value
                .trim()
                .replace(/\s/g, "")
                .replace(",", ".");

        if (!valor) {
            return padrao;
        }

        const resultado = Number(valor);

        return Number.isFinite(resultado)
            ? resultado
            : padrao;
    }


    function formatar(valor, casas = 0) {

        return Number(valor).toLocaleString("pt-BR", {
            minimumFractionDigits: casas,
            maximumFractionDigits: casas
        });
    }


    // ==========================================================
    // MÁSCARA DE HORÁRIO
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
    // KATCH — MASSA MAGRA
    // ==========================================================

    function atualizarCampoMassaMagra() {

        if (!selectFormula || !grupoMassaMagra) {
            return;
        }

        const katch =
            selectFormula.value === "katch";

        grupoMassaMagra.style.display =
            katch ? "block" : "none";

        if (!katch) {

            if (erroMassaMagra) {
                erroMassaMagra.textContent = "";
            }

            if (inputMassaMagra) {
                inputMassaMagra.value = "";
            }
        }
    }


    if (selectFormula) {

        selectFormula.addEventListener(
            "change",
            atualizarCampoMassaMagra
        );

        atualizarCampoMassaMagra();
    }


    // Limpa o aviso enquanto o usuário digita
    if (inputMassaMagra) {

        inputMassaMagra.addEventListener("input", () => {

            if (erroMassaMagra) {
                erroMassaMagra.textContent = "";
            }
        });
    }


    // ==========================================================
    // CÁLCULO METABÓLICO
    // ==========================================================

    if (formMetabolico) {

        formMetabolico.addEventListener("submit", (e) => {

            e.preventDefault();


            const peso =
                numero("peso");

            const idade =
                numero("idade");

            // O banco fornece a altura em centímetros
            const alturaCm =
                numero("altura");

            const atividade =
                numero("atividade");


            const sexo =
                (
                    document.getElementById("genero")?.value || ""
                )
                    .trim()
                    .toUpperCase();


            const formula =
                selectFormula?.value || "";


            const objetivo =
                document.getElementById("objetivo")?.value || "";


            // --------------------------------------------------
            // VALIDAÇÕES
            // --------------------------------------------------

            if (peso <= 0) {

                alert("Peso inválido.");
                return;
            }

            if (idade <= 0) {

                alert("Idade inválida.");
                return;
            }

            if (alturaCm <= 0) {

                alert("Altura inválida.");
                return;
            }

            if (!["M", "F"].includes(sexo)) {

                alert("Sexo do paciente não identificado.");
                return;
            }

            if (atividade <= 0) {

                alert("Fator de atividade inválido.");
                return;
            }


            // --------------------------------------------------
            // TMB
            // --------------------------------------------------

            let tmb;


            // Mifflin-St Jeor
            if (formula === "mifflin") {

                tmb =
                    (10 * peso) +
                    (6.25 * alturaCm) -
                    (5 * idade) +
                    (sexo === "M" ? 5 : -161);
            }


            // Harris-Benedict
            else if (formula === "harris") {

                if (sexo === "M") {

                    tmb =
                        88.362 +
                        (13.397 * peso) +
                        (4.799 * alturaCm) -
                        (5.677 * idade);

                } else {

                    tmb =
                        447.593 +
                        (9.247 * peso) +
                        (3.098 * alturaCm) -
                        (4.330 * idade);
                }
            }


            // Katch-McArdle
            else if (formula === "katch") {

                const massaMagra =
                    numero("massa-magra");


                if (massaMagra <= 0) {

                    if (erroMassaMagra) {

                        erroMassaMagra.textContent =
                            "Informe a massa magra para calcular com Katch-McArdle.";
                    }

                    inputMassaMagra?.focus();

                    return;
                }


                if (erroMassaMagra) {
                    erroMassaMagra.textContent = "";
                }


                tmb =
                    (21.6 * massaMagra) +
                    370;
            }


            else {

                alert("Selecione uma fórmula metabólica.");
                return;
            }


            // --------------------------------------------------
            // GET
            // --------------------------------------------------

            const get =
                tmb * atividade;


            // --------------------------------------------------
            // META
            // --------------------------------------------------

            let meta =
                get;


            if (objetivo === "emagrecimento") {

                meta -= 500;

            } else if (objetivo === "hipertrofia") {

                meta += 300;
            }


            // --------------------------------------------------
            // MACRONUTRIENTES
            // --------------------------------------------------

            const proteina =
                peso * 2;

            const gordura =
                peso;

            const carboidrato =
                Math.max(
                    (
                        meta -
                        (proteina * 4) -
                        (gordura * 9)
                    ) / 4,
                    0
                );


            // --------------------------------------------------
            // RESULTADOS
            // --------------------------------------------------

            document.getElementById("res-tmb").innerText =
                `${formatar(tmb)} kcal`;

            document.getElementById("res-get").innerText =
                `${formatar(get)} kcal`;

            document.getElementById("res-meta").innerText =
                `${formatar(meta)} kcal`;

            document.getElementById("res-prot").innerText =
                `${formatar(proteina, 1)} g`;

            document.getElementById("res-gord").innerText =
                `${formatar(gordura, 1)} g`;

            document.getElementById("res-carb").innerText =
                `${formatar(carboidrato, 1)} g`;


            if (painelResultados) {
                painelResultados.style.display = "block";
            }

        });
    }


    // ==========================================================
    // REFEIÇÕES
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
                    <div class="card-refeicao-item">

                        <div class="topo-refeicao">

                            <span class="titulo-refeicao-nome">
                                ${ref.nome}
                            </span>

                            <span class="horario-refeicao-badge">
                                ${ref.horario}
                            </span>

                        </div>

                        <div class="corpo-refeicao-vazio">

                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="icon-nav"
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

                            Clique para buscar e adicionar
                            alimentos a esta refeição.

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
    // NOVA REFEIÇÃO
    // ==========================================================

    if (btnNovaRefeicao) {

        btnNovaRefeicao.addEventListener("click", () => {

            if (!painelAddRef) {
                return;
            }

            painelAddRef.classList.remove("escondido");

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


            inputNome.value = "";
            inputHorario.value = "";


            painelAddRef?.classList.add(
                "escondido"
            );

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