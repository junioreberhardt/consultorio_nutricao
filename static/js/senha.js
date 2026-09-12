/**
 * SISTEMA NUTRIR MELHOR - CONTROLES DE SENHA E FORMULÁRIOS
 */

document.addEventListener("DOMContentLoaded", () => {
	// =========================================================
	// MOSTRAR / OCULTAR SENHA
	// =========================================================

	const botoesSenha = document.querySelectorAll("[data-toggle-senha]")

	botoesSenha.forEach((botao) => {
		botao.addEventListener("click", () => {
			const idCampo = botao.dataset.target
			const campo = document.getElementById(idCampo)

			if (!campo) {
				return
			}

			const mostrando = campo.type === "text"

			campo.type = mostrando ? "password" : "text"

			botao.setAttribute(
				"aria-label",
				mostrando ? "Mostrar senha" : "Ocultar senha",
			)

			const icone = botao.querySelector("svg")

			if (icone) {
				icone.setAttribute("data-lucide", mostrando ? "eye" : "eye-off")

				icone.setAttribute("width", "16")
				icone.setAttribute("height", "16")
			}

			if (typeof lucide !== "undefined") {
				lucide.createIcons({
					attrs: {
						width: 16,
						height: 16,
					},
				})
			}
		})
	})

	// =========================================================
	// ENVIO AUTOMÁTICO DA FOTO DE PERFIL
	// =========================================================

	const camposFoto = document.querySelectorAll("[data-auto-submit]")

	camposFoto.forEach((campo) => {
		campo.addEventListener("change", () => {
			const formulario = campo.closest("form")

			if (!formulario) {
				return
			}

			formulario.submit()
		})
	})
})
