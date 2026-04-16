const form = document.getElementById("search-form");
const stopButton = document.getElementById("stop-button");
const telegramEnabled = document.getElementById("telegram-enabled");
const telegramFields = document.getElementById("telegram-fields");
const telegramBadge = document.getElementById("telegram-badge");
const notificationState = document.getElementById("notification-state");
const runStatus = document.getElementById("run-status");
const runMeta = document.getElementById("run-meta");
const attemptCount = document.getElementById("attempt-count");
const startedAt = document.getElementById("started-at");
const finishedAt = document.getElementById("finished-at");
const statusEcho = document.getElementById("status-echo");
const statusPill = document.getElementById("status-pill");
const logOutput = document.getElementById("log-output");
const toggleLogBtn = document.getElementById("toggle-log-btn");
const logShell = document.getElementById("log-shell");
const runningLoader = document.getElementById("running-loader");
const webNotificationEnabled = document.getElementById("web-notification-enabled");
const webNotificationStatus = document.getElementById("web-notification-status");
const howItWorksTrigger = document.getElementById("how-it-works-trigger");
const howItWorksModal = document.getElementById("how-it-works-modal");
const ticketFoundModal = document.getElementById("ticket-found-modal");
const soundEnabled = document.getElementById("sound-enabled");
const delaySlider = document.getElementById("delay-slider");
const delayInput = document.getElementById("delay-input");

let lastLogId = 0;
let previouslyFound = false;
let swRegistration = null;
let audioContextRef = null;
let audioUnlocked = false;
let notificationCooldownUntil = 0;

const FOUND_NOTIFICATION_TAG = "tcdd-bilet-bulundu";
const FOUND_NOTIFICATION_TITLE = "TCDD Bilet Alarmi";
const FOUND_NOTIFICATION_BODY = "Uygun bilet bulundu. Satin alma icin TCDD eBilet'i kontrol et.";

function setTextIfPresent(element, value) {
  if (element) {
    element.textContent = value;
  }
}

function updateNotificationIndicator() {
  const totalOptions = 3;
  const activeOptions = [
    telegramEnabled.checked,
    webNotificationEnabled.checked,
    soundEnabled.checked,
  ].filter(Boolean).length;

  telegramBadge.classList.remove("state-off", "state-partial", "state-on");

  if (activeOptions === 0) {
    telegramBadge.textContent = "Kapali";
    telegramBadge.classList.add("state-off");
    setTextIfPresent(notificationState, "Kapali");
    return;
  }

  if (activeOptions === totalOptions) {
    telegramBadge.textContent = "Acık";
    telegramBadge.classList.add("state-on");
    setTextIfPresent(notificationState, "Acık");
    return;
  }

  telegramBadge.textContent = "Kısmen Acık";
  telegramBadge.classList.add("state-partial");
  setTextIfPresent(notificationState, "Kısmen Acık");
}

function setTodayDefaults() {
  const dateField = form.elements.tarih;
  const timeField = form.elements.saat;
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  const hh = String(now.getHours()).padStart(2, "0");
  const min = String(now.getMinutes()).padStart(2, "0");

  const todayIso = `${yyyy}-${mm}-${dd}`;
  dateField.min = todayIso;
  if (!dateField.value) {
    dateField.value = todayIso;
  }
  if (!timeField.value) {
    timeField.value = `${hh}:${min}`;
  }
}

function updateTelegramState() {
  const enabled = telegramEnabled.checked;
  telegramFields.classList.toggle("is-hidden", !enabled);
  updateNotificationIndicator();
}

function syncDelayControls(fromSlider) {
  if (fromSlider) {
    delayInput.value = delaySlider.value;
  } else {
    const numeric = Math.min(60, Math.max(1, Number(delayInput.value || 1)));
    delayInput.value = numeric;
    delaySlider.value = String(numeric);
  }
}

function updateWebNotificationState() {
  if (!("Notification" in window)) {
    webNotificationEnabled.checked = false;
    webNotificationEnabled.disabled = true;
    webNotificationStatus.textContent = "Tarayici bildirimi: Desteklenmiyor";
    updateNotificationIndicator();
    return;
  }

  if (Notification.permission === "granted") {
    webNotificationStatus.textContent = "Tarayici bildirimi: Acik ve arka planda gosterilebilir";
    webNotificationEnabled.checked = true;
    webNotificationEnabled.disabled = true;
  } else if (Notification.permission === "denied") {
    webNotificationStatus.textContent = "Tarayici bildirimi: Tarayicidan engelli";
    webNotificationEnabled.checked = false;
    webNotificationEnabled.disabled = true;
  } else {
    webNotificationStatus.textContent = "Tarayici bildirimi: Kapali";
    webNotificationEnabled.disabled = false;
  }
  updateNotificationIndicator();
}

async function requestWebNotificationPermission() {
  if (!("Notification" in window)) {
    return;
  }
  if (!webNotificationEnabled.checked) {
    return;
  }
  if (Notification.permission !== "default") {
    updateWebNotificationState();
    return;
  }
  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    webNotificationEnabled.checked = false;
  }
  if (permission === "granted") {
    await ensureServiceWorker();
  }
  updateWebNotificationState();
}

function openModal(modalElement) {
  if (!modalElement) {
    return;
  }
  modalElement.classList.remove("is-hidden");
  modalElement.setAttribute("aria-hidden", "false");
}

function closeModal(modalElement) {
  if (!modalElement) {
    return;
  }
  modalElement.classList.add("is-hidden");
  modalElement.setAttribute("aria-hidden", "true");
}

function applyStatusTone(data) {
  const rawStatus = (data.status || "Hazir").toLowerCase();
  let tone = "idle";

  if (data.running) {
    tone = "running";
  } else if (data.found || rawStatus.includes("bulundu")) {
    tone = "success";
  } else if (
    rawStatus.includes("hata") ||
    rawStatus.includes("durdur") ||
    rawStatus.includes("tamam")
  ) {
    tone = "warning";
  }

  statusPill.className = `status-pill ${tone}`;
  statusPill.textContent = data.status || "Hazir";
}

async function ensureServiceWorker() {
  if (!("serviceWorker" in navigator)) {
    return null;
  }
  if (swRegistration) {
    return swRegistration;
  }
  try {
    swRegistration = await navigator.serviceWorker.register("/sw.js");
    await navigator.serviceWorker.ready;
    return swRegistration;
  } catch (_error) {
    return null;
  }
}

async function showFoundNotification() {
  if (!("Notification" in window)) {
    return;
  }
  if (!webNotificationEnabled.checked) {
    return;
  }
  if (Notification.permission !== "granted") {
    return;
  }
  const options = {
    body: FOUND_NOTIFICATION_BODY,
    icon: "/favicon.ico",
    badge: "/favicon.ico",
    tag: FOUND_NOTIFICATION_TAG,
    renotify: true,
    requireInteraction: true,
    vibrate: [300, 150, 300, 150, 700],
  };

  const registration = await ensureServiceWorker();
  if (registration && "showNotification" in registration) {
    await registration.showNotification(FOUND_NOTIFICATION_TITLE, options);
    return;
  }

  const notification = new Notification(FOUND_NOTIFICATION_TITLE, options);
  notification.onclick = () => {
    window.focus();
    notification.close();
  };
}

function getAudioContext() {
  if (!audioContextRef) {
    audioContextRef = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContextRef;
}

async function unlockAudio() {
  if (!soundEnabled.checked) {
    return;
  }
  try {
    const audioContext = getAudioContext();
    if (audioContext.state === "suspended") {
      await audioContext.resume();
    }
    audioUnlocked = audioContext.state === "running";
  } catch (_error) {
    audioUnlocked = false;
  }
}

function scheduleTone(audioContext, frequency, startAt, duration, volume) {
  const osc = audioContext.createOscillator();
  const gain = audioContext.createGain();

  osc.type = "sine";
  osc.frequency.setValueAtTime(frequency, audioContext.currentTime + startAt);
  gain.gain.setValueAtTime(0.0001, audioContext.currentTime + startAt);
  gain.gain.exponentialRampToValueAtTime(volume, audioContext.currentTime + startAt + 0.03);
  gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + startAt + duration);

  osc.connect(gain);
  gain.connect(audioContext.destination);
  osc.start(audioContext.currentTime + startAt);
  osc.stop(audioContext.currentTime + startAt + duration + 0.04);
}

async function playFoundSound() {
  if (!soundEnabled.checked) {
    return;
  }
  try {
    await unlockAudio();
    if (!audioUnlocked) {
      return;
    }

    const now = Date.now();
    if (now < notificationCooldownUntil) {
      return;
    }
    notificationCooldownUntil = now + 12000;

    const audioContext = getAudioContext();
    const pattern = [
      { startAt: 0.0, duration: 0.42, frequency: 880, volume: 0.22 },
      { startAt: 0.6, duration: 0.42, frequency: 988, volume: 0.22 },
      { startAt: 1.2, duration: 0.42, frequency: 880, volume: 0.24 },
      { startAt: 1.8, duration: 0.55, frequency: 1046, volume: 0.25 },
      { startAt: 2.7, duration: 0.42, frequency: 880, volume: 0.22 },
      { startAt: 3.3, duration: 0.42, frequency: 988, volume: 0.22 },
      { startAt: 3.9, duration: 0.42, frequency: 880, volume: 0.24 },
      { startAt: 4.5, duration: 0.75, frequency: 1174, volume: 0.26 },
    ];

    pattern.forEach(({ startAt, duration, frequency, volume }) => {
      scheduleTone(audioContext, frequency, startAt, duration, volume);
    });
  } catch (_error) {
    // Ignore audio errors on unsupported browsers.
  }
}

async function refreshStatus() {
  const response = await fetch("/api/status");
  const data = await response.json();

  setTextIfPresent(runStatus, data.status || "Hazir");
  setTextIfPresent(
    runMeta,
    data.running
      ? "Selenium taramasi arka planda aktif olarak calisiyor."
      : data.found
        ? "Uygun koltuk bulundu, arama sonucu hazir."
        : "Su anda aktif bir tarama yok."
  );
  runningLoader.classList.toggle("is-hidden", !data.running);

  setTextIfPresent(attemptCount, String(data.attempt ?? 0));
  startedAt.textContent = data.started_at || "-";
  finishedAt.textContent = data.finished_at || "-";
  statusEcho.textContent = data.status || "Beklemede";
  applyStatusTone(data);

  if (data.found && !previouslyFound) {
    openModal(ticketFoundModal);
    await showFoundNotification();
    await playFoundSound();
  }
  previouslyFound = Boolean(data.found);
}

async function refreshLogs() {
  const response = await fetch(`/api/logs?after=${lastLogId}`);
  const data = await response.json();

  if (data.items.length) {
    if (logOutput.textContent === "Log bekleniyor...") {
      logOutput.textContent = "";
    }
    for (const item of data.items) {
      logOutput.textContent += `[${item.timestamp}] ${item.message}\n`;
    }
    logOutput.scrollTop = logOutput.scrollHeight;
    lastLogId = data.last_id;
  }
}

function formToPayload() {
  return {
    nereden: form.elements.nereden.value,
    nereye: form.elements.nereye.value,
    tarih: form.elements.tarih.value,
    saat: form.elements.saat.value,
    delay_time: Number(delayInput.value || 1),
    allow_economy: form.elements.allow_economy.checked,
    allow_business: form.elements.allow_business.checked,
    telegram_msg: form.elements.telegram_msg.checked,
    bot_token: form.elements.bot_token.value,
    chat_id: form.elements.chat_id.value,
  };
}

async function startJob(event) {
  event.preventDefault();
  const dateField = form.elements.tarih;
  const todayIso = new Date().toISOString().slice(0, 10);
  if (dateField.value && dateField.value < todayIso) {
    alert("Bugünden daha eski bir tarih seçilemez.");
    return;
  }
  const response = await fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formToPayload()),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    alert(data.error || "Arama baslatilirken bir hata olustu.");
    return;
  }

  previouslyFound = false;
  await refreshStatus();
}

async function stopJob() {
  await fetch("/api/stop", { method: "POST" });
  await refreshStatus();
}

setTodayDefaults();
updateTelegramState();
updateWebNotificationState();
syncDelayControls(false);
ensureServiceWorker();

telegramEnabled.addEventListener("change", updateTelegramState);
delaySlider.addEventListener("input", () => syncDelayControls(true));
delayInput.addEventListener("input", () => syncDelayControls(false));
webNotificationEnabled.addEventListener("change", requestWebNotificationPermission);
soundEnabled.addEventListener("change", async () => {
  updateNotificationIndicator();
  await unlockAudio();
});
form.addEventListener("submit", startJob);
stopButton.addEventListener("click", stopJob);
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    notificationCooldownUntil = 0;
  }
});
document.addEventListener("pointerdown", unlockAudio, { passive: true });
document.addEventListener("keydown", unlockAudio);

if (howItWorksTrigger && howItWorksModal) {
  howItWorksTrigger.addEventListener("click", () => openModal(howItWorksModal));
}

toggleLogBtn.addEventListener("click", () => {
  const hidden = logOutput.classList.toggle("is-hidden");
  logShell.classList.toggle("is-collapsed", hidden);
  toggleLogBtn.textContent = hidden ? "Gunlugu Ac" : "Gunlugu Kapat";
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
  button.addEventListener("click", () => {
    closeModal(howItWorksModal);
    closeModal(ticketFoundModal);
  });
});

document.addEventListener("click", (event) => {
  if (event.target.classList.contains("modal")) {
    closeModal(event.target);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeModal(howItWorksModal);
    closeModal(ticketFoundModal);
  }
});

refreshStatus();
refreshLogs();
setInterval(() => {
  refreshStatus();
  refreshLogs();
}, 3000);
