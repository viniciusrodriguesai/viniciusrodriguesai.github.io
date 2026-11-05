'use strict';
const copyButton = document.querySelector('#copy-email');
const copyStatus = document.querySelector('#copy-status');
let statusTimer;
if (copyButton && copyStatus) {
  copyButton.addEventListener('click', async () => {
    clearTimeout(statusTimer);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText('viniciusmangueira04@gmail.com');
      copyStatus.textContent = 'E-mail copiado!';
      copyButton.setAttribute('aria-label', 'E-mail copiado. Copiar novamente');
    } catch {
      copyStatus.textContent = 'Selecione o endereço para copiar ou clique nele para enviar um e-mail.';
    }
    statusTimer = setTimeout(() => {
      copyStatus.textContent = '';
      copyButton.setAttribute('aria-label', 'Copiar endereço de e-mail');
    }, 6000);
  });
}
