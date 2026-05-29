// ═══════════════════════════════════════════════════════════════
// UWU TRANSLATOR — текстовая трансформация (общая логика)
// ═══════════════════════════════════════════════════════════════
// Работает и в браузере (window.RW.translator), и в Node (module.exports)
// — последнее нужно для юнит-тестов.
//
// Алгоритм:
//   1. Словарные замены целых слов (Unicode-границы — работают для кириллицы).
//   2. Русская фонетика: р→ль, л→лью, смягчение согласных.
//   3. Английская фонетика: одиночные r/l→w, n+гласная→ny.
//   4. Случайные «звуки» персонажа после знаков препинания.

(function (root, factory) {
    'use strict';
    const api = factory();
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = api;            // Node / тесты
    }
    root.RW = root.RW || {};
    root.RW.translator = api;            // браузер
})(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    function escapeRegExp(s) {
        return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Граница слова без lookbehind (совместимо со старыми Safari):
    // захватываем не-буквенный префикс и возвращаем его при замене.
    // \p{L}\p{N} с флагом u корректно распознают кириллицу.
    function applyDictionary(text, dict) {
        let result = text;
        for (const word in dict) {
            if (!Object.prototype.hasOwnProperty.call(dict, word)) continue;
            const re = new RegExp(
                '(^|[^\\p{L}\\p{N}_])(' + escapeRegExp(word) + ')(?![\\p{L}\\p{N}_])',
                'giu'
            );
            result = result.replace(re, (m, pre) => pre + dict[word]);
        }
        return result;
    }

    function applyRussianPhonetics(text) {
        let r = text;
        r = r.replace(/р/g, 'ль').replace(/Р/g, 'Ль');
        r = r.replace(/л(?![ьюя])/g, 'лью').replace(/Л(?![ьюя])/g, 'Лью');
        r = r.replace(/([внсз])([аеёиоуыэюя])/g, '$1ь$2');
        return r;
    }

    function applyEnglishPhonetics(text) {
        let r = text;
        r = r.replace(/\b([rl])\b/g, 'w');
        r = r.replace(/n([aeiou])/g, 'ny$1');
        return r;
    }

    /**
     * @param {string} text   исходный текст
     * @param {object} opts   { dict, noises, noiseProbability, random }
     * @returns {string}
     */
    function uwuTranslate(text, opts) {
        opts = opts || {};
        const dict = opts.dict || {};
        const noises = opts.noises || [];
        const noiseProbability = typeof opts.noiseProbability === 'number'
            ? opts.noiseProbability : 0.6;
        const random = opts.random || Math.random;

        if (!text || !text.trim()) return '';

        let result = applyDictionary(text, dict);
        result = applyRussianPhonetics(result);
        result = applyEnglishPhonetics(result);

        if (noises.length === 0) return result;

        const segments = result.split(/([.!?…])/);
        const out = [];
        segments.forEach(segment => {
            out.push(segment);
            if (/[.!?…]/.test(segment) && random() < noiseProbability) {
                out.push(noises[Math.floor(random() * noises.length)]);
            }
        });
        return out.join('');
    }

    return { uwuTranslate, applyDictionary, applyRussianPhonetics, applyEnglishPhonetics, escapeRegExp };
});
