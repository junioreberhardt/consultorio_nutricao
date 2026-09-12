/**
 * SISTEMA NUTRIR MELHOR - ÍCONES DAS TELAS DE AUTENTICAÇÃO
 */

document.addEventListener("DOMContentLoaded", () => {
	if (typeof lucide !== "undefined") {
		lucide.createIcons()
	} else {
		console.error("A biblioteca Lucide não pôde ser carregada pelo navegador.")
	}
})
