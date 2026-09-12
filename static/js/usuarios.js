document.addEventListener('DOMContentLoaded', () => {

    // =========================================================
    // TOGGLE DE STATUS
    // =========================================================

    const togglesStatus = document.querySelectorAll(
        '.form-toggle-status .toggle-input'
    );

    togglesStatus.forEach(toggle => {

        toggle.addEventListener('change', () => {

            const formulario = toggle.closest('form');

            if (!formulario) {
                return;
            }

            formulario.submit();
        });

    });


    // =========================================================
    // TOGGLES DE PERMISSÕES
    // =========================================================

    const togglesPermissoes = document.querySelectorAll(
        '.form-toggle-permissao .toggle-input'
    );

    togglesPermissoes.forEach(toggle => {

        toggle.addEventListener('change', () => {

            const formulario = toggle.closest('form');

            if (!formulario) {
                return;
            }

            formulario.submit();
        });

    });


    // =========================================================
    // CARGO PERSONALIZADO
    // =========================================================

    const selectsCargo = document.querySelectorAll(
        'select[name="cargo"]'
    );

    selectsCargo.forEach(select => {

        const usuarioId = select.id.replace('cargo_', '');

        const campoOutro = document.getElementById(
            `outro_${usuarioId}`
        );

        if (!campoOutro) {
            return;
        }

        const atualizarCampoOutro = () => {

            if (select.value === 'outro') {

                campoOutro.classList.remove('hidden');

                campoOutro.focus();

            } else {

                campoOutro.classList.add('hidden');

                campoOutro.value = '';

            }

        };

        select.addEventListener(
            'change',
            atualizarCampoOutro
        );

        atualizarCampoOutro();

    });


    // =========================================================
    // CONFIRMAÇÃO DE EXCLUSÃO
    // =========================================================

    const formulariosExclusao = document.querySelectorAll(
        '.form-excluir-usuario'
    );

    formulariosExclusao.forEach(formulario => {

        formulario.addEventListener('submit', event => {

            const nomeUsuario =
                formulario.dataset.nomeUsuario || 'este usuário';

            const confirmar = window.confirm(
                `Tem certeza que deseja excluir ${nomeUsuario}?`
            );

            if (!confirmar) {
                event.preventDefault();
            }

        });

    });


    const selectCargo = document.getElementById('cargo');
    const campoOutro = document.getElementById('campo-cargo-outro');
    const inputOutro = document.getElementById('cargo_personalizado');

    if (selectCargo && campoOutro && inputOutro) {
        function atualizarCargo() {
            if (selectCargo.value === 'outro') {
                campoOutro.classList.remove('hidden');
            } else {
                campoOutro.classList.add('hidden');
                inputOutro.value = '';
            }
        }

        selectCargo.addEventListener(
            'change',
            atualizarCargo
        );

        atualizarCargo();
    }

});