/* ============================================================
   AI Philosophy Courtroom — Frontend Logic
   ============================================================ */

const API_BASE = '/api';
const MAX_ROUNDS = 5;

/* ---------- State ---------- */
const state = {
    round: 0,
    totalRounds: MAX_ROUNDS,
    userScoreTotal: 0,
    aiScoreTotal: 0,
    debateHistory: [],
    currentTopic: 'free-will',
    currentPhilosopher: 'balanced',
    isProcessing: false,
    debateStarted: false,
};

/* ---------- DOM Refs ---------- */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const dom = {
    // Entry
    entryOverlay: $('#entryOverlay'),
    enterBtn: $('#enterBtn'),

    // App
    app: $('#app'),

    // Header
    topicSelect: $('#topicSelect'),
    roundNumber: $('#roundNumber'),
    resetBtn: $('#resetBtn'),

    // Panels
    userMessages: $('#userMessages'),
    aiMessages: $('#aiMessages'),

    // Judge
    gavelContainer: $('#gavelContainer'),
    judgeStatus: $('#judgeStatus'),
    verdictCard: $('#verdictCard'),
    userLogicBar: $('#userLogicBar'),
    aiLogicBar: $('#aiLogicBar'),
    userLogicScore: $('#userLogicScore'),
    aiLogicScore: $('#aiLogicScore'),
    verdictWinner: $('#verdictWinner'),
    verdictFeedback: $('#verdictFeedback'),

    // Scores
    userScore: $('#userScore'),
    aiScore: $('#aiScore'),

    // Input
    argumentInput: $('#argumentInput'),
    charCount: $('#charCount'),
    sendBtn: $('#sendBtn'),
    objectionBtn: $('#objectionBtn'),
    typingIndicator: $('#typingIndicator'),
    inputHint: $('#inputHint'),

    // Overlays
    objectionOverlay: $('#objectionOverlay'),
    finalOverlay: $('#finalOverlay'),
    finalScores: $('#finalScores'),
    finalWinner: $('#finalWinner'),
    finalSummary: $('#finalSummary'),
    newCaseBtn: $('#newCaseBtn'),

    // Particles
    particles: $('#particles'),
};

/* ---------- Initialization ---------- */
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    bindEvents();
});

/* ---------- Entry Animation ---------- */
function enterCourtroom() {
    dom.entryOverlay.classList.add('exit');
    setTimeout(() => {
        dom.entryOverlay.style.display = 'none';
        dom.app.classList.remove('hidden');
    }, 800);
}

/* ---------- Particles ---------- */
function initParticles() {
    const symbols = ['Φ', 'Ψ', 'Ω', 'Σ', 'Δ', 'Π', 'λ', '∞', '∃', '∀', '⊃', '≡', '¬', '∧', '∨', '⊢'];
    const container = dom.particles;

    for (let i = 0; i < 25; i++) {
        const particle = document.createElement('span');
        particle.className = 'particle';
        particle.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        particle.style.left = Math.random() * 100 + '%';
        particle.style.fontSize = (0.8 + Math.random() * 1.2) + 'rem';
        particle.style.animationDuration = (15 + Math.random() * 25) + 's';
        particle.style.animationDelay = (Math.random() * 20) + 's';
        container.appendChild(particle);
    }
}

/* ---------- Event Bindings ---------- */
function bindEvents() {
    // Entry
    dom.enterBtn.addEventListener('click', enterCourtroom);

    // Input
    dom.argumentInput.addEventListener('input', onInputChange);
    dom.argumentInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitArgument();
        }
    });

    dom.sendBtn.addEventListener('click', submitArgument);
    dom.objectionBtn.addEventListener('click', triggerObjection);

    // Topic
    dom.topicSelect.addEventListener('change', (e) => {
        state.currentTopic = e.target.value;
    });

    // Philosopher chips
    $$('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            $$('.chip').forEach(c => c.classList.remove('chip-active'));
            chip.classList.add('chip-active');
            state.currentPhilosopher = chip.dataset.philosopher;
        });
    });

    // Reset
    dom.resetBtn.addEventListener('click', resetDebate);
    dom.newCaseBtn.addEventListener('click', () => {
        dom.finalOverlay.classList.add('hidden');
        resetDebate();
    });
}

/* ---------- Input Handling ---------- */
function onInputChange() {
    const len = dom.argumentInput.value.length;
    dom.charCount.textContent = `${len}/500`;
}

/* ---------- Submit Argument ---------- */
async function submitArgument() {
    const text = dom.argumentInput.value.trim();
    if (!text || state.isProcessing) return;
    if (state.round >= state.totalRounds) return;

    state.isProcessing = true;
    state.debateStarted = true;
    state.round++;

    // UI updates
    setInputEnabled(false);
    dom.roundNumber.textContent = state.round;
    dom.roundNumber.classList.add('score-pop');
    setTimeout(() => dom.roundNumber.classList.remove('score-pop'), 500);

    // Clear empty states on first round
    if (state.round === 1) {
        clearEmptyStates();
    }

    // Add user message
    addMessage('user', text, state.round);
    dom.argumentInput.value = '';
    dom.charCount.textContent = '0/500';

    // Show typing
    showTyping(true);

    try {
        // Get AI response
        const aiResponse = await fetchAIResponse(text);
        showTyping(false);

        // Add AI message
        addMessage('ai', aiResponse, state.round);

        // Store in history
        state.debateHistory.push({
            round: state.round,
            user: text,
            ai: aiResponse,
        });

        // Get judge verdict
        showJudgeThinking();
        const verdict = await fetchJudgeVerdict(text, aiResponse, state.round);

        // Display verdict
        displayVerdict(verdict);

        // Update scores
        updateScores(verdict);

        // Check if final round
        if (state.round >= state.totalRounds) {
            setTimeout(() => showFinalVerdict(), 2000);
        }

    } catch (error) {
        showTyping(false);
        console.error('Debate error:', error);
        addMessage('ai', '⚠ The court apologizes — a technical difficulty has occurred. Please try your argument again.', state.round);
        state.round--;
        dom.roundNumber.textContent = state.round || 1;
    }

    state.isProcessing = false;
    setInputEnabled(true);
    dom.argumentInput.focus();
}

/* ---------- API Calls ---------- */
async function fetchAIResponse(userArgument) {
    const res = await fetch(`${API_BASE}/debate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            argument: userArgument,
            topic: state.currentTopic,
            philosopher: state.currentPhilosopher,
            history: state.debateHistory,
            round: state.round,
        }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || 'Failed to get AI response');
    }

    const data = await res.json();
    return data.response;
}

async function fetchJudgeVerdict(userArg, aiArg, round) {
    try {
        const res = await fetch(`${API_BASE}/judge`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_argument: userArg,
                ai_argument: aiArg,
                topic: state.currentTopic,
                round: round,
                history: state.debateHistory,
            }),
        });

        const data = await res.json();
        // Ensure we always have valid scores
        return {
            user_score: parseFloat(data.user_score) || 6.0,
            ai_score: parseFloat(data.ai_score) || 6.5,
            feedback: data.feedback || 'The judge has noted both arguments.',
        };
    } catch (err) {
        console.warn('Judge API error, using fallback scores:', err);
        return {
            user_score: 6.0,
            ai_score: 6.5,
            feedback: 'The judge encountered a delay. Provisional scores assigned.',
        };
    }
}

/* ---------- Objection System ---------- */
function triggerObjection() {
    if (state.isProcessing || state.debateHistory.length === 0) return;

    // Show overlay
    dom.objectionOverlay.classList.remove('hidden');

    // Auto-hide after 1.5s
    setTimeout(() => {
        dom.objectionOverlay.classList.add('hidden');
    }, 1500);

    // Insert objection text into input
    const lastAI = state.debateHistory[state.debateHistory.length - 1]?.ai || '';
    dom.argumentInput.value = `OBJECTION! I challenge your claim. `;
    dom.argumentInput.focus();
    onInputChange();
}

/* ---------- Message Rendering ---------- */
function addMessage(type, text, round) {
    const container = type === 'user' ? dom.userMessages : dom.aiMessages;

    const msg = document.createElement('div');
    msg.className = `message message-${type}`;
    msg.innerHTML = `
        <div class="message-round">Round ${round}</div>
        <div class="message-text"></div>
    `;

    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;

    // Typewriter effect for AI messages
    const textEl = msg.querySelector('.message-text');
    if (type === 'ai') {
        typewriterEffect(textEl, text);
    } else {
        textEl.textContent = text;
    }
}

function typewriterEffect(element, text, speed = 18) {
    let i = 0;
    element.textContent = '';
    const timer = setInterval(() => {
        element.textContent += text[i];
        i++;
        if (i >= text.length) clearInterval(timer);
    }, speed);
}

/* ---------- Judge UI ---------- */
function showJudgeThinking() {
    dom.judgeStatus.innerHTML = '<p class="judge-waiting">⚖ The judge is deliberating...</p>';
    dom.verdictCard.classList.add('hidden');

    // Gavel animation
    const gavel = dom.gavelContainer.querySelector('.gavel');
    gavel.classList.add('strike');
    setTimeout(() => gavel.classList.remove('strike'), 600);
}

function displayVerdict(verdict) {
    const userScore = parseFloat(verdict.user_score) || 0;
    const aiScore = parseFloat(verdict.ai_score) || 0;

    dom.judgeStatus.innerHTML = '';
    dom.verdictCard.classList.remove('hidden');

    // Animate bars
    setTimeout(() => {
        dom.userLogicBar.style.width = `${userScore * 10}%`;
        dom.aiLogicBar.style.width = `${aiScore * 10}%`;
    }, 200);

    dom.userLogicScore.textContent = userScore.toFixed(1);
    dom.aiLogicScore.textContent = aiScore.toFixed(1);

    // Winner
    if (userScore > aiScore) {
        dom.verdictWinner.textContent = '🏆 Round Winner: You (Defense)';
    } else if (aiScore > userScore) {
        dom.verdictWinner.textContent = '🏆 Round Winner: AI (Prosecution)';
    } else {
        dom.verdictWinner.textContent = '⚖ This round is a draw';
    }

    // Feedback
    dom.verdictFeedback.textContent = verdict.feedback || '';

    // Gavel strike
    const gavel = dom.gavelContainer.querySelector('.gavel');
    gavel.classList.add('strike');
    setTimeout(() => gavel.classList.remove('strike'), 600);
}

function updateScores(verdict) {
    const userScore = parseFloat(verdict.user_score) || 0;
    const aiScore = parseFloat(verdict.ai_score) || 0;

    state.userScoreTotal += userScore;
    state.aiScoreTotal += aiScore;

    const userAvg = (state.userScoreTotal / state.round).toFixed(1);
    const aiAvg = (state.aiScoreTotal / state.round).toFixed(1);

    dom.userScore.textContent = userAvg;
    dom.aiScore.textContent = aiAvg;

    // Pop animation
    dom.userScore.classList.add('score-pop');
    dom.aiScore.classList.add('score-pop');
    setTimeout(() => {
        dom.userScore.classList.remove('score-pop');
        dom.aiScore.classList.remove('score-pop');
    }, 500);
}

/* ---------- Final Verdict ---------- */
function showFinalVerdict() {
    const userAvg = (state.userScoreTotal / state.totalRounds).toFixed(1);
    const aiAvg = (state.aiScoreTotal / state.totalRounds).toFixed(1);

    dom.finalScores.innerHTML = `
        <div class="final-score-block">
            <span class="final-score-num user-color">${userAvg}</span>
            <span class="final-score-label">Your Average</span>
        </div>
        <div class="final-score-block">
            <span class="final-score-num ai-color">${aiAvg}</span>
            <span class="final-score-label">AI Average</span>
        </div>
    `;

    if (parseFloat(userAvg) > parseFloat(aiAvg)) {
        dom.finalWinner.textContent = '🏆 Victory! The Defense prevails!';
    } else if (parseFloat(aiAvg) > parseFloat(userAvg)) {
        dom.finalWinner.textContent = '⚖ The Prosecution wins this case.';
    } else {
        dom.finalWinner.textContent = '⚖ The case ends in a perfect draw.';
    }

    dom.finalSummary.textContent = `Over ${state.totalRounds} rounds of philosophical debate on "${getTopicName(state.currentTopic)}", the court has reached its final verdict.`;

    dom.finalOverlay.classList.remove('hidden');
}

/* ---------- Helpers ---------- */
function setInputEnabled(enabled) {
    dom.argumentInput.disabled = !enabled;
    dom.sendBtn.disabled = !enabled;
    dom.objectionBtn.disabled = !enabled;
}

function showTyping(show) {
    dom.typingIndicator.classList.toggle('hidden', !show);
    dom.inputHint.classList.toggle('hidden', show);
}

function clearEmptyStates() {
    dom.userMessages.innerHTML = '';
    dom.aiMessages.innerHTML = '';
}

function resetDebate() {
    state.round = 0;
    state.userScoreTotal = 0;
    state.aiScoreTotal = 0;
    state.debateHistory = [];
    state.isProcessing = false;
    state.debateStarted = false;

    dom.roundNumber.textContent = '1';
    dom.userScore.textContent = '0.0';
    dom.aiScore.textContent = '0.0';

    dom.userMessages.innerHTML = `
        <div class="empty-state">
            <span class="empty-icon">💭</span>
            <p>Present your opening argument below...</p>
        </div>
    `;
    dom.aiMessages.innerHTML = `
        <div class="empty-state">
            <span class="empty-icon">🧠</span>
            <p>Preparing counter-arguments...</p>
        </div>
    `;

    dom.judgeStatus.innerHTML = '<p class="judge-waiting">Awaiting arguments from both parties...</p>';
    dom.verdictCard.classList.add('hidden');
    dom.userLogicBar.style.width = '0%';
    dom.aiLogicBar.style.width = '0%';
    dom.userLogicScore.textContent = '—';
    dom.aiLogicScore.textContent = '—';

    dom.finalOverlay.classList.add('hidden');

    dom.argumentInput.value = '';
    dom.charCount.textContent = '0/500';
    setInputEnabled(true);
    showTyping(false);
    dom.argumentInput.focus();
}

function getTopicName(value) {
    const map = {
        'free-will': 'Free Will vs Determinism',
        'ethics': 'Ethics & Morality',
        'consciousness': 'Nature of Consciousness',
        'existentialism': 'Existentialism',
        'simulation': 'Simulation Theory',
        'epistemology': 'Epistemology',
        'justice': 'Justice & Fairness',
        'absurdism': 'Absurdism & Meaning of Life',
    };
    return map[value] || value;
}
