/**
 * SISTEMA NUTRIR MELHOR - GERENCIADOR DE TEMA
 */

document.addEventListener("DOMContentLoaded", () => {
	const htmlElement = document.documentElement

	const botaoTema = document.getElementById("theme-toggle")

	const textoTema = document.getElementById("theme-toggle-text")

	function atualizarTemaVisual(isDark) {
		if (botaoTema) {
			const icone = botaoTema.querySelector("svg, i")

			if (icone) {
				icone.setAttribute("data-lucide", isDark ? "sun" : "moon")
			}

			botaoTema.setAttribute(
				"title",
				isDark ? "Mudar para Modo Claro" : "Mudar para Modo Escuro",
			)
		}

		if (textoTema) {
			textoTema.textContent = isDark ? "Tema claro" : "Tema escuro"
		}

		if (typeof lucide !== "undefined") {
			lucide.createIcons()
		}
	}

	function salvarTema(tema) {
		fetch("/atualizar/tema", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				tema: tema,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error(`Erro HTTP ${response.status}`)
				}

				return response.json()
			})
			.then((data) => {
				console.log("Preferência de tema salva no banco:", data.tema)
			})
			.catch((error) => {
				console.error("Falha ao salvar tema no servidor:", error)
			})
	}

	function alternarTema() {
		htmlElement.classList.toggle("dark")

		const isDark = htmlElement.classList.contains("dark")

		const tema = isDark ? "escuro" : "claro"

		atualizarTemaVisual(isDark)
		salvarTema(tema)
	}

	const temaInicial = htmlElement.classList.contains("dark")

	atualizarTemaVisual(temaInicial)

	if (botaoTema) {
		botaoTema.addEventListener("click", alternarTema)
	}
})
