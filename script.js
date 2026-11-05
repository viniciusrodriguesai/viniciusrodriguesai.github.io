'use strict';

(() => {
  const dictionaries = window.PORTFOLIO_TRANSLATIONS;
  const selector = document.querySelector('#language-select');
  const copyButton = document.querySelector('#copy-email');
  const copyStatus = document.querySelector('#copy-status');
  const storageKey = 'portfolio-language';
  const htmlLanguages = { en: 'en', es: 'es', pt: 'pt-BR', zh: 'zh-Hans' };
  const ogLocales = { en: 'en_US', es: 'es_ES', pt: 'pt_BR', zh: 'zh_CN' };
  let currentLanguage = 'en';
  let statusTimer;

  // The complete English page remains readable if the dictionary cannot load.
  if (!dictionaries?.en) {
    if (selector) selector.disabled = true;
    if (copyButton) copyButton.hidden = true;
    return;
  }

  const sourceKeys = new Map(Object.entries(dictionaries.en).map(([key, value]) => [value, key]));
  const textBindings = [];
  const attributeBindings = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;

  // Keep the existing elements, links, SVGs and expanded details in place.
  // Only the original text nodes and accessible descriptions are translated.
  while ((node = walker.nextNode())) {
    if (node.parentElement?.closest('script, style, noscript, [data-i18n-skip]')) continue;
    const value = node.textContent;
    const marker = node.previousSibling;
    const key = marker?.nodeType === Node.COMMENT_NODE && marker.data.startsWith('i18n:')
      ? marker.data.slice(5)
      : sourceKeys.get(value.trim());
    if (key && Object.hasOwn(dictionaries.en, key)) {
      textBindings.push({
        node,
        key,
        prefix: value.slice(0, value.length - value.trimStart().length),
        suffix: value.slice(value.trimEnd().length),
      });
    }
  }

  document.querySelectorAll('[aria-label], [alt], meta[name="description"], meta[property="og:title"], meta[property="og:description"]').forEach(element => {
    for (const attribute of ['aria-label', 'alt', 'content']) {
      const key = element.getAttribute(`data-i18n-${attribute}`) || sourceKeys.get(element.getAttribute(attribute));
      if (key) attributeBindings.push({ element, attribute, key });
    }
  });

  function normalizeLanguage(value) {
    if (typeof value !== 'string') return null;
    const code = value.toLowerCase();
    const aliases = { 'en-us': 'en', 'en-gb': 'en', 'pt-br': 'pt', 'zh-cn': 'zh', 'zh-hans': 'zh' };
    const language = aliases[code] || code;
    return Object.hasOwn(htmlLanguages, language) && dictionaries[language] ? language : null;
  }

  function initialLanguage() {
    const requested = normalizeLanguage(new URL(window.location.href).searchParams.get('lang'));
    if (requested) return requested;
    try {
      return normalizeLanguage(window.localStorage.getItem(storageKey)) || 'en';
    } catch {
      return 'en';
    }
  }

  function setLanguage(language, persist = false) {
    const locale = normalizeLanguage(language) || 'en';
    const text = dictionaries[locale];
    currentLanguage = locale;
    textBindings.forEach(binding => {
      binding.node.textContent = binding.prefix + text[binding.key] + binding.suffix;
    });
    attributeBindings.forEach(binding => {
      binding.element.setAttribute(binding.attribute, text[binding.key]);
    });
    document.documentElement.lang = htmlLanguages[locale];
    document.title = text.t000;
    const ogLocale = document.querySelector('meta[property="og:locale"]');
    if (ogLocale) ogLocale.content = ogLocales[locale];
    if (selector) selector.value = locale;
    clearTimeout(statusTimer);
    if (copyStatus) copyStatus.textContent = '';
    if (copyButton) copyButton.setAttribute('aria-label', text.t199);
    if (persist) {
      try { window.localStorage.setItem(storageKey, locale); } catch { /* Storage is optional. */ }
      try {
        const url = new URL(window.location.href);
        url.searchParams.set('lang', locale);
        window.history.replaceState(window.history.state, '', url);
      } catch { /* Translation still works with restricted history access. */ }
    }
  }

  setLanguage(initialLanguage());
  selector?.addEventListener('change', event => setLanguage(event.target.value, true));

  if (copyButton && copyStatus) {
    copyButton.addEventListener('click', async () => {
      clearTimeout(statusTimer);
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText('viniciusmangueira04@gmail.com');
        copyStatus.textContent = dictionaries[currentLanguage].emailCopied;
        copyButton.setAttribute('aria-label', dictionaries[currentLanguage].emailCopiedLabel);
      } catch {
        copyStatus.textContent = dictionaries[currentLanguage].emailCopyError;
      }
      statusTimer = setTimeout(() => {
        copyStatus.textContent = '';
        copyButton.setAttribute('aria-label', dictionaries[currentLanguage].t199);
      }, 6000);
    });
  }
})();
