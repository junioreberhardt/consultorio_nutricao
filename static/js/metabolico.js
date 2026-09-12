/**
 * SISTEMA NUTRIR MELHOR - ENGINE DE CÁLCULO METABÓLICO
 */
document.addEventListener("DOMContentLoaded", () => {
	// Escuta o clique diretamente no botão, impedindo qualquer refresh físico da página
	const btnCalcular = document.getElementById("btn-calcular-metas")
	const painelResultados = document.getElementById("painel-resultados")
	const selectFormula = document.getElementById("formula")
	const grupoMassaMagra = document.getElementById("grupo-massa-magra")
	const inputMassaMagra = document.getElementById("massa-magra")
	const erroMassaMagra = document.getElementById("erro-massa-magra")

	// --- UTILITÁRIOS DE CAPTURA ---
	function numero(id, padrao = 0) {
		const elemento = document.getElementById(id)
		if (!elemento) return padrao
		const valor = elemento.value.trim().replace(/\s/g, "").replace(",", ".")
		if (!valor) return padrao
		const resultado = Number(valor)
		return Number.isFinite(resultado) ? resultado : padrao
	}

	function formatar(valor, casas = 0) {
		return Number(valor).toLocaleString("pt-BR", {
			minimumFractionDigits: casas,
			maximumFractionDigits: casas,
		})
	}

	// --- CONTROLE EXIBIÇÃO KATCH-MCARDLE ---
	function atualizarCampoMassaMagra() {
		if (!selectFormula || !grupoMassaMagra) return
		const katch = selectFormula.value === "katch"

		if (katch) {
			grupoMassaMagra.classList.remove("hidden")
			inputMassaMagra?.setAttribute("required", "required")
		} else {
			grupoMassaMagra.classList.add("hidden")
			inputMassaMagra?.removeAttribute("required")
			if (erroMassaMagra) erroMassaMagra.textContent = ""
			if (inputMassaMagra) inputMassaMagra.value = ""
		}
	}

	if (selectFormula) {
		selectFormula.addEventListener("change", atualizarCampoMassaMagra)
		atualizarCampoMassaMagra()
	}

	// --- EXECUÇÃO LOGICA NO CLICK ---
	if (btnCalcular) {
		btnCalcular.addEventListener("click", (e) => {
			// Trava tripla contra recarregamento
			e.preventDefault()

			const peso = numero("peso")
			const idade = numero("idade")
			const alturaCm = numero("altura")
			const atividade = numero("atividade")
			const sexo = (document.getElementById("genero")?.value || "")
				.trim()
				.toUpperCase()
			const formula = selectFormula?.value || ""
			const objetivo = document.getElementById("objetivo")?.value || ""

			// VALIDAÇÕES AMIGÁVEIS
			if (
				peso <= 0 ||
				idade <= 0 ||
				alturaCm <= 0 ||
				atividade <= 0 ||
				!["M", "F"].includes(sexo)
			) {
				alert(
					"Erro: Não foi possível ler as métricas do paciente. Certifique-se de acessar essa página vindo da lista de pacientes clicando em 'Prescrever'.",
				)
				return
			}

			// EQUAÇÕES
			let tmb
			if (formula === "mifflin") {
				tmb =
					10 * peso + 6.25 * alturaCm - 5 * idade + (sexo === "M" ? 5 : -161)
			} else if (formula === "harris") {
				if (sexo === "M") {
					tmb = 88.362 + 13.397 * peso + 4.799 * alturaCm - 5.677 * idade
				} else {
					tmb = 447.593 + 9.247 * peso + 3.098 * alturaCm - 4.33 * idade
				}
			} else if (formula === "katch") {
				const massaMagra = numero("massa-magra")
				if (massaMagra <= 0) {
					if (erroMassaMagra)
						erroMassaMagra.textContent = "Informe a massa magra para calcular."
					inputMassaMagra?.focus()
					return
				}
				tmb = 21.6 * massaMagra + 370
			}

			const get = tmb * atividade
			let meta = get

			if (objetivo === "emagrecimento") meta -= 500
			else if (objetivo === "hipertrofia") meta += 300

			const proteina = peso * 2
			const gordura = peso
			const carboidrato = Math.max((meta - proteina * 4 - gordura * 9) / 4, 0)

			// INJEÇÃO SEGURA
			if (document.getElementById("res-tmb"))
				document.getElementById("res-tmb").innerText = `${formatar(tmb)} kcal`
			if (document.getElementById("res-get"))
				document.getElementById("res-get").innerText = `${formatar(get)} kcal`
			if (document.getElementById("res-meta"))
				document.getElementById("res-meta").innerText = `${formatar(meta)} kcal`
			if (document.getElementById("res-prot"))
				document.getElementById("res-prot").innerText =
					`${formatar(proteina, 1)} g`
			if (document.getElementById("res-gord"))
				document.getElementById("res-gord").innerText =
					`${formatar(gordura, 1)} g`
			if (document.getElementById("res-carb"))
				document.getElementById("res-carb").innerText =
					`${formatar(carboidrato, 1)} g`

			if (painelResultados) {
				painelResultados.classList.remove("hidden")
			}
		})
	}
})
