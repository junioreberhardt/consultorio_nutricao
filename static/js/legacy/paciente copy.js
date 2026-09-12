/**
 * SISTEMA NUTRIR MELHOR - GERENCIADOR DE ABAS DO PRONTUÁRIO
 */
document.addEventListener("DOMContentLoaded", () => {
    const botoes = document.querySelectorAll("[data-hs-tab]");
    const paineis = document.querySelectorAll('[role="tabpanel"]');

    botoes.forEach(botao => {
        botao.addEventListener("click", () => {
            // 1. Limpa o visual ativo de todos os botões da lista
            botoes.forEach(b => {
                b.classList.remove("active", "font-semibold", "border-emerald-600", "text-emerald-600");
                b.setAttribute("aria-selected", "false");
            });

            // 2. Aplica as cores ativas esmeralda no botão clicado
            botao.classList.add("active", "font-semibold", "border-emerald-600", "text-emerald-600");
            botao.setAttribute("aria-selected", "true");

            // 3. Adiciona a classe hidden para sumir com todos os painéis
            paineis.forEach(p => p.classList.add("hidden"));

            // 4. Captura o seletor ID (ex: #painel-cadastro) e exibe na tela
            const alvoId = botao.getAttribute("data-hs-tab");
            const painelAlvo = document.querySelector(alvoId);
            if (painelAlvo) {
                painelAlvo.classList.remove("hidden");
            }
        });
    });

    // Inicialização forçada do Preline caso esteja ativo em outro escopo
    if (typeof HSStaticMethods !== 'undefined') {
        HSStaticMethods.autoInit();
    }
});
