// ═══════════════════════════════════════════════════════════════
// APP — связывание UI (требует wolves.js, translator.js, api.js)
// ═══════════════════════════════════════════════════════════════
// Компоненты: портал входа, анимированные фоны, звук, переключение
// персонажей/режимов, переводчик, чат (AI + заготовки), тосты.

(function () {
    'use strict';

    const RW = window.RW || {};
    const WOLVES = RW.WOLVES || {};

    // ── Состояние ───────────────────────────────────────────────
    let currentWolf = 'nocturne';
    let currentMode = 'translator';
    let aiMode = false;
    let conversationHistory = [];
    let isTyping = false;
    let apiAvailable = false;

    function trimConversationHistory() {
        const limit = RW.api.getConfig().historyLimit;
        if (conversationHistory.length > limit) {
            conversationHistory = conversationHistory.slice(-limit);
        }
    }

    function pickCanned(wolf) {
        return wolf.responses[Math.floor(Math.random() * wolf.responses.length)];
    }

    document.addEventListener('DOMContentLoaded', function () {
        const body = document.body;
        const entryPortal = document.getElementById('entryPortal');
        const enterBtn = document.getElementById('enterBtn');
        const portalBg = document.getElementById('portalBg');
        const animatedBg = document.getElementById('animatedBg');

        const wolfTitle = document.getElementById('wolfTitle');
        const wolfSubtitle = document.getElementById('wolfSubtitle');
        const inputLabel = document.getElementById('inputLabel');
        const outputLabel = document.getElementById('outputLabel');
        const footerText = document.getElementById('footerText');

        const translatorMode = document.getElementById('translatorMode');
        const chatMode = document.getElementById('chatMode');

        const inputBox = document.getElementById('input');
        const outputBox = document.getElementById('output');
        const transformBtn = document.getElementById('transformBtn');
        const copyBtn = document.getElementById('copyBtn');
        const clearTranslatorBtn = document.getElementById('clearTranslatorBtn');

        const aiToggle = document.getElementById('aiToggle');
        const aiStatus = document.getElementById('aiStatus');
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        const typingIndicator = document.getElementById('typingIndicator');

        const toast = document.getElementById('toast');

        if (!enterBtn || !entryPortal || !portalBg) {
            console.error('Критические элементы не найдены!');
            return;
        }

        // ── Портал входа ────────────────────────────────────────
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'portal-particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.setProperty('--drift', (Math.random() - 0.5) * 100 + 'px');
            particle.style.animationDelay = Math.random() * 3 + 's';
            portalBg.appendChild(particle);
        }

        enterBtn.addEventListener('click', () => {
            playSound('enter');
            entryPortal.classList.add('hidden');
            setTimeout(() => {
                entryPortal.style.display = 'none';
                updateAnimatedBackground(currentWolf);
            }, 800);
        });

        // ── Анимированные фоны ──────────────────────────────────
        function updateAnimatedBackground(wolfId) {
            if (!animatedBg) return;
            animatedBg.innerHTML = '';

            switch (wolfId) {
                case 'nocturne': {
                    const codeLines = [
                        'def uwu_translate(text):', 'import cyberwolf', 'nocturne.process(data)',
                        '>>> executing protocol...', 'if wolf.nocturne:', 'system.hacked()',
                        '0x4E6F6374756E65'
                    ];
                    for (let i = 0; i < 10; i++) {
                        const line = document.createElement('div');
                        line.className = 'code-line';
                        line.textContent = codeLines[Math.floor(Math.random() * codeLines.length)];
                        line.style.top = (i * 10 + 5) + '%';
                        line.style.animationDelay = Math.random() * 15 + 's';
                        animatedBg.appendChild(line);
                    }
                    break;
                }
                case 'rudy':
                    for (let i = 0; i < 5; i++) {
                        const stripe = document.createElement('div');
                        stripe.className = 'bmw-stripe';
                        stripe.style.top = (i * 20 + 10) + '%';
                        stripe.style.animationDelay = (i * 0.8) + 's';
                        animatedBg.appendChild(stripe);
                    }
                    break;
                case 'nick': {
                    const notes = ['♪', '♫', '♩', '♬', '🎵', '🎶'];
                    for (let i = 0; i < 15; i++) {
                        const note = document.createElement('div');
                        note.className = 'music-note';
                        note.textContent = notes[Math.floor(Math.random() * notes.length)];
                        note.style.left = Math.random() * 100 + '%';
                        note.style.animationDelay = Math.random() * 8 + 's';
                        note.style.animationDuration = (5 + Math.random() * 3) + 's';
                        animatedBg.appendChild(note);
                    }
                    break;
                }
                case 'death':
                    for (let i = 0; i < 30; i++) {
                        const fire = document.createElement('div');
                        fire.className = 'fire-particle';
                        fire.style.left = Math.random() * 100 + '%';
                        fire.style.bottom = '-10px';
                        fire.style.animationDelay = Math.random() * 3 + 's';
                        fire.style.animationDuration = (2 + Math.random() * 2) + 's';
                        animatedBg.appendChild(fire);
                    }
                    break;
                case 'felix': {
                    const hearts = ['💕', '💖', '💗', '💘', '💝', '♡', '💓'];
                    for (let i = 0; i < 20; i++) {
                        const heart = document.createElement('div');
                        heart.className = 'heart-particle';
                        heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
                        heart.style.left = Math.random() * 100 + '%';
                        heart.style.animationDelay = Math.random() * 6 + 's';
                        heart.style.animationDuration = (4 + Math.random() * 2) + 's';
                        animatedBg.appendChild(heart);
                    }
                    break;
                }
            }
        }

        // ── Звук (Web Audio API) ────────────────────────────────
        function playSound(type) {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                const presets = { enter: [400, 0.3, 0.3], transform: [300, 0.2, 0.2], message: [500, 0.15, 0.15] };
                const [freq, vol, dur] = presets[type] || presets.message;
                osc.frequency.value = freq;
                gain.gain.setValueAtTime(vol, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + dur);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + dur);
            } catch (e) { /* без звука */ }
        }

        // ── Переключение персонажей ─────────────────────────────
        document.querySelectorAll('.personality-btn').forEach(btn => {
            btn.addEventListener('click', () => switchWolf(btn.dataset.wolf));
        });

        function switchWolf(wolfId) {
            if (!WOLVES[wolfId]) return;
            currentWolf = wolfId;
            const wolf = WOLVES[wolfId];

            playSound('enter');
            body.className = wolfId;
            if (wolfTitle) wolfTitle.textContent = wolf.title;
            if (wolfSubtitle) wolfSubtitle.textContent = wolf.subtitle;
            if (inputLabel) inputLabel.textContent = wolf.inputLabel;
            if (outputLabel) outputLabel.textContent = wolf.outputLabel;
            if (footerText) footerText.textContent = wolf.footer;

            document.querySelectorAll('.personality-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.wolf === wolfId);
            });

            updateAnimatedBackground(wolfId);

            conversationHistory = [];
            if (currentMode === 'chat' && chatMessages) {
                chatMessages.innerHTML = '';
                addSystemMessage(`Переключено на ${wolf.name}. Контекст очищен.`);
            }
            showToast(`Переключено на ${wolf.name}!`);
        }

        // ── Переключение режимов ────────────────────────────────
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => switchMode(btn.dataset.mode));
        });

        function switchMode(mode) {
            currentMode = mode;
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.mode === mode);
            });
            if (mode === 'translator') {
                if (translatorMode) translatorMode.classList.add('active');
                if (chatMode) chatMode.classList.remove('active');
            } else {
                if (translatorMode) translatorMode.classList.remove('active');
                if (chatMode) chatMode.classList.add('active');
                if (chatMessages && chatMessages.children.length === 0) {
                    addSystemMessage(WOLVES[currentWolf].greeting);
                }
            }
        }

        // ── Переводчик ──────────────────────────────────────────
        function transform() {
            if (!inputBox || !outputBox) return;
            const input = inputBox.value;
            if (!input.trim()) {
                outputBox.value = WOLVES[currentWolf].noises[0] + ' Пусто...';
                return;
            }
            const wolf = WOLVES[currentWolf];
            outputBox.value = RW.translator.uwuTranslate(input, { dict: wolf.dict, noises: wolf.noises });
        }

        let autoConvertTimeout;
        if (inputBox) {
            inputBox.addEventListener('input', () => {
                clearTimeout(autoConvertTimeout);
                autoConvertTimeout = setTimeout(transform, 500);
            });
        }
        if (transformBtn) {
            transformBtn.addEventListener('click', () => { playSound('transform'); transform(); });
        }
        if (copyBtn) {
            copyBtn.addEventListener('click', async () => {
                if (!outputBox) return;
                const text = outputBox.value;
                if (!text.trim()) { showToast('Нечего копировать!'); return; }
                try {
                    await navigator.clipboard.writeText(text);
                    showToast('✓ Скопировано!');
                } catch (err) {
                    outputBox.select();
                    document.execCommand('copy');
                    showToast('✓ Скопировано!');
                }
            });
        }
        if (clearTranslatorBtn) {
            clearTranslatorBtn.addEventListener('click', () => {
                if (inputBox) inputBox.value = '';
                if (outputBox) outputBox.value = '';
                showToast('Очищено!');
            });
        }

        // ── AI-режим и статус API ───────────────────────────────
        if (aiToggle) {
            aiToggle.addEventListener('click', () => {
                if (!apiAvailable && !aiMode) {
                    showToast('⚠️ LLM-сервер сейчас недоступен');
                    return;
                }
                aiMode = !aiMode;
                aiToggle.classList.toggle('active', aiMode);
                playSound('transform');
                showToast(aiMode ? 'Режим AI включён' : 'Заготовленные ответы');
            });
        }

        function updateApiStatus(available) {
            if (!aiStatus) return;
            const indicator = aiStatus.querySelector('.status-indicator');
            const text = aiStatus.querySelector('span');
            if (indicator && text) {
                indicator.classList.toggle('online', available);
                indicator.classList.toggle('offline', !available);
                text.textContent = available ? 'LLM доступен' : 'LLM недоступен';
            }
        }

        async function refreshApiStatus() {
            apiAvailable = await RW.api.checkApiStatus();
            updateApiStatus(apiAvailable);
            if (!apiAvailable && aiMode) {
                aiMode = false;
                if (aiToggle) aiToggle.classList.remove('active');
            }
        }
        refreshApiStatus();
        setInterval(refreshApiStatus, 30000);

        // ── Чат ─────────────────────────────────────────────────
        function addMessage(content, role) {
            if (!chatMessages) return;
            const msg = document.createElement('div');
            msg.className = `chat-message ${role}`;
            msg.textContent = content;
            chatMessages.appendChild(msg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        function addSystemMessage(content) { addMessage(content, 'system'); }

        function showTypingIndicator() {
            if (typingIndicator) {
                typingIndicator.classList.add('active');
                if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
        function hideTypingIndicator() {
            if (typingIndicator) typingIndicator.classList.remove('active');
        }

        async function sendMessage() {
            if (!chatInput || !sendBtn) return;
            const userMessage = chatInput.value.trim();
            if (!userMessage || isTyping) return;

            const wolf = WOLVES[currentWolf];
            addMessage(userMessage, 'user');
            conversationHistory.push({ role: 'user', content: userMessage });
            trimConversationHistory();

            chatInput.value = '';
            chatInput.style.height = 'auto';
            isTyping = true;
            sendBtn.disabled = true;
            showTypingIndicator();

            let assistantMessage;
            try {
                if (aiMode && apiAvailable) {
                    try {
                        assistantMessage = await RW.api.callAI(wolf.systemPrompt, conversationHistory);
                    } catch (err) {
                        // Нейронка не ответила — мягко падаем на заготовку, чат не молчит.
                        console.warn('AI fallback:', err);
                        assistantMessage = pickCanned(wolf);
                    }
                } else {
                    await new Promise(r => setTimeout(r, 800 + Math.random() * 800));
                    assistantMessage = pickCanned(wolf);
                }

                hideTypingIndicator();
                addMessage(assistantMessage, 'assistant');
                conversationHistory.push({ role: 'assistant', content: assistantMessage });
                trimConversationHistory();
                playSound('message');
            } catch (error) {
                hideTypingIndicator();
                addSystemMessage(`❌ Ошибка: ${error.message}`);
                console.error('Chat Error:', error);
            } finally {
                isTyping = false;
                if (sendBtn) sendBtn.disabled = false;
                if (chatInput) chatInput.focus();
            }
        }

        if (sendBtn) sendBtn.addEventListener('click', sendMessage);
        if (chatInput) {
            chatInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
            });
            chatInput.addEventListener('input', () => {
                chatInput.style.height = 'auto';
                chatInput.style.height = Math.min(chatInput.scrollHeight, 150) + 'px';
            });
        }

        // ── Тосты ───────────────────────────────────────────────
        function showToast(message) {
            if (!toast) return;
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2500);
        }
    });
})();
