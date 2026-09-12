// static/js/usuarios.js

/**
 * Controla dinamicamente a exibição do campo de texto personalizado 
 * quando a opção "Outro..." é selecionada no Cargo Funcional.
 */
function verificarCargoOutro(id) {
    const select = document.getElementById('cargo_' + id);
    const inputOutro = document.getElementById('outro_' + id);
    
    if (select && inputOutro) {
        if (select.value === 'outro') {
            inputOutro.classList.remove('escondido');
            inputOutro.classList.add('exibir-inline');
            inputOutro.required = true;
            inputOutro.focus();
        } else {
            inputOutro.classList.remove('exibir-inline');
            inputOutro.classList.add('escondido');
            inputOutro.required = false;
            inputOutro.value = '';
        }
    }
}

/**
 * Dispara uma caixa de confirmação nativa do navegador para evitar 
 * que o administrador clique no botão de excluir por acidente.
 */
function confirmarExclusao(nomeUsuario) {
    return confirm(
        "⚠️ ALERTA CRÍTICO:\n\n" +
        "Tem certeza absoluta de que deseja excluir permanentemente o funcionário '" + nomeUsuario + "' do sistema?\n\n" +
        "Esta ação apagará as permissões dele do banco de dados do consultório e não poderá ser desfeita!"
    );
}

// Configurações iniciais ao carregar a página
document.addEventListener("DOMContentLoaded", function() {
    console.log("Módulo JS de Usuários operando localmente com sucesso.");
});
