// ═══════════════════════════════════════════════════════════════
// LLM API — интеграция с OpenAI-совместимым бэкендом (LM Studio и др.)
// ═══════════════════════════════════════════════════════════════
// Настройки читаются из config.js (window.*) с разумными значениями
// по умолчанию. В прокси-режиме ключ не используется на фронте: его
// добавляет nginx из .env. В прямом режиме можно задать window.API_KEY.

window.RW = window.RW || {};

window.RW.api = (function () {
    'use strict';

    function getConfig() {
        const w = (typeof window !== 'undefined') ? window : {};
        return {
            baseUrl: w.API_BASE_URL || '/api/llm',
            model: w.MODEL_NAME || 'google/gemma-4-e2b',
            apiKey: w.API_KEY || '',
            // '' => omit reasoning_effort (gemma puts reasoning in a separate
            // field; sending 'none' makes it bleed into content). Forced-reasoning
            // Qwen3 builds instead NEED 'none' or content comes back empty.
            reasoningEffort: (w.REASONING_EFFORT === undefined) ? '' : w.REASONING_EFFORT,
            maxTokens: w.MAX_TOKENS || 600,
            historyLimit: w.CHAT_HISTORY_LIMIT || 20,
            timeoutMs: w.REQUEST_TIMEOUT_MS || 60000,
            temperature: (w.TEMPERATURE === undefined) ? 0.85 : w.TEMPERATURE
        };
    }

    function authHeaders(cfg) {
        const h = { 'Content-Type': 'application/json' };
        if (cfg.apiKey) h['Authorization'] = 'Bearer ' + cfg.apiKey;
        return h;
    }

    // Убираем reasoning-теги, если модель встроила их в content.
    function stripThink(text) {
        return (text || '')
            .replace(/<think>[\s\S]*?<\/think>/gi, '')
            .replace(/<\|?think\|?>[\s\S]*?<\/?\|?think\|?>/gi, '')
            .trim();
    }

    function extractAssistantMessage(data) {
        const choice = data && Array.isArray(data.choices) ? data.choices[0] : null;
        const content = stripThink(choice && choice.message ? choice.message.content : '');
        if (!content) {
            const err = new Error('Модель вернула пустой ответ (reasoning съел весь бюджет токенов?)');
            err.code = 'EMPTY';
            return Promise.reject(err);
        }
        return content;
    }

    async function checkApiStatus() {
        const cfg = getConfig();
        const controller = new AbortController();
        const t = setTimeout(() => controller.abort(), 5000);
        try {
            const res = await fetch(cfg.baseUrl + '/v1/models', {
                method: 'GET',
                headers: authHeaders(cfg),
                signal: controller.signal
            });
            return res.ok;
        } catch (e) {
            return false;
        } finally {
            clearTimeout(t);
        }
    }

    // history: [{role:'user'|'assistant', content}]
    async function callAI(systemPrompt, history) {
        const cfg = getConfig();
        const messages = [{ role: 'system', content: systemPrompt }].concat(history || []);

        const body = {
            model: cfg.model,
            messages: messages,
            temperature: cfg.temperature,
            max_tokens: cfg.maxTokens,
            stream: false
        };
        // Пустая строка => параметр не отправляем (по умолчанию для gemma).
        // 'none' отключает «размышления» у Qwen3 (иначе пустой content).
        if (cfg.reasoningEffort) body.reasoning_effort = cfg.reasoningEffort;

        const controller = new AbortController();
        const t = setTimeout(() => controller.abort(), cfg.timeoutMs);
        try {
            const res = await fetch(cfg.baseUrl + '/v1/chat/completions', {
                method: 'POST',
                headers: authHeaders(cfg),
                signal: controller.signal,
                body: JSON.stringify(body)
            });
            if (!res.ok) {
                const errText = await res.text().catch(() => '');
                throw new Error('HTTP ' + res.status + (errText ? ': ' + errText.slice(0, 200) : ''));
            }
            const data = await res.json();
            return await extractAssistantMessage(data);
        } catch (e) {
            if (e.name === 'AbortError') throw new Error('Таймаут запроса к LLM');
            throw e;
        } finally {
            clearTimeout(t);
        }
    }

    return { getConfig, checkApiStatus, callAI, stripThink };
})();
