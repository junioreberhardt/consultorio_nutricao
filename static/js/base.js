/**
 * SISTEMA NUTRIR MELHOR - INICIALIZAÇÃO GLOBAL
 */

document.addEventListener("DOMContentLoaded", () => {

	// =========================================================
	// LUCIDE
	// =========================================================

	if (typeof lucide !== "undefined") {
		lucide.createIcons();
	} else {
		console.error(
			"A biblioteca Lucide não pôde ser carregada pelo navegador."
		);
	}


	// =========================================================
	// MENU DO USUÁRIO
	// =========================================================

	const botaoPerfil = document.getElementById(
		"hs-dropdown-custom-trigger"
	);

	const menuPerfil = botaoPerfil
		? botaoPerfil.parentElement.querySelector(".hs-dropdown-menu")
		: null;

	if (botaoPerfil && menuPerfil) {

		function abrirMenu() {
			menuPerfil.classList.remove("hidden");

			botaoPerfil.setAttribute(
				"aria-expanded",
				"true"
			);
		}

		function fecharMenu() {
			menuPerfil.classList.add("hidden");

			botaoPerfil.setAttribute(
				"aria-expanded",
				"false"
			);
		}

		function alternarMenu() {
			const estaAberto =
				!menuPerfil.classList.contains("hidden");

			if (estaAberto) {
				fecharMenu();
			} else {
				abrirMenu();
			}
		}

		botaoPerfil.addEventListener(
			"click",
			(event) => {
				event.stopPropagation();
				alternarMenu();
			}
		);

		menuPerfil.addEventListener(
			"click",
			(event) => {
				event.stopPropagation();
			}
		);

		document.addEventListener(
			"click",
			() => {
				fecharMenu();
			}
		);

		document.addEventListener(
			"keydown",
			(event) => {
				if (event.key === "Escape") {
					fecharMenu();
				}
			}
		);
	}

});