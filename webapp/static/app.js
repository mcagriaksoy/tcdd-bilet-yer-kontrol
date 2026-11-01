const form = document.getElementById("search-form");
const stopButton = document.getElementById("stop-button");
const telegramEnabled = document.getElementById("telegram-enabled");
const telegramFields = document.getElementById("telegram-fields");
const telegramBadge = document.getElementById("telegram-badge");
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
const captchaModal = document.getElementById("captcha-modal");
const soundEnabled = document.getElementById("sound-enabled");
const delaySlider = document.getElementById("delay-slider");
const delayInput = document.getElementById("delay-input");

let lastLogId = 0;
let previouslyFound = false;
let captchaDismissed = false;
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

let stationList = [];
const stationDataElement = document.getElementById("station-data");
if (stationDataElement) {
  try {
    stationList = JSON.parse(stationDataElement.textContent || "[]");
  } catch (_error) {
    stationList = [];
  }
}

function normalizeStation(value) {
  return (value || "")
    .toLocaleLowerCase("tr-TR")
    .replace(/ı/g, "i")
    .replace(/ş/g, "s")
    .replace(/ğ/g, "g")
    .replace(/ü/g, "u")
    .replace(/ö/g, "o")
    .replace(/ç/g, "c")
    .replace(/â/g, "a")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function setupStationPicker(picker) {
  const input = picker.querySelector("input");
  const list = picker.querySelector(".station-options");
  if (!input || !list) {
    return;
  }

  let visibleStations = [];
  let activeIndex = -1;

  function updateActiveOption() {
    const options = list.querySelectorAll(".station-option");
    options.forEach((option, index) => {
      const isActive = index === activeIndex;
      option.classList.toggle("is-active", isActive);
      option.setAttribute("aria-selected", String(isActive));
      if (isActive) {
        option.scrollIntoView({ block: "nearest" });
      }
    });
  }

  function chooseStation(index) {
    const station = visibleStations[index];
    if (!station) {
      return;
    }
    input.value = station;
    input.dataset.selected = station;
    closeList();
    input.focus();
    input.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function renderList() {
    list.replaceChildren();
    if (!visibleStations.length) {
      const empty = document.createElement("div");
      empty.className = "station-empty";
      empty.textContent = "Eşleşen istasyon bulunamadı";
      list.appendChild(empty);
      return;
    }

    visibleStations.forEach((station, index) => {
      const option = document.createElement("button");
      option.type = "button";
      option.className = "station-option";
      option.setAttribute("role", "option");
      option.textContent = station;
      option.addEventListener("mousedown", (event) => event.preventDefault());
      option.addEventListener("click", () => chooseStation(index));
      option.addEventListener("mouseenter", () => {
        activeIndex = index;
        updateActiveOption();
      });
      list.appendChild(option);
    });
  }

  function openList(filterText = "") {
    const query = normalizeStation((filterText || "").trim());
    visibleStations = query
      ? stationList.filter((station) => normalizeStation(station).includes(query))
      : stationList.slice();

    renderList();
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");

    const selected = visibleStations.indexOf(input.dataset.selected || input.value);
    activeIndex = selected >= 0 ? selected : visibleStations.length ? 0 : -1;
    updateActiveOption();
  }

  function closeList() {
    list.hidden = true;
    input.setAttribute("aria-expanded", "false");
    activeIndex = -1;
  }

  input.addEventListener("focus", () => openList(""));
  input.addEventListener("click", () => {
    if (list.hidden) {
      openList("");
    }
  });
  input.addEventListener("input", () => {
    input.dataset.selected = "";
    openList(input.value);
  });
  input.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (list.hidden) {
        openList(input.value);
        return;
      }
      activeIndex = Math.min(visibleStations.length - 1, activeIndex + 1);
      updateActiveOption();
      return;
    }
    if (event.key === "ArrowUp") {
      event.preventDefault();
      if (list.hidden) {
        openList(input.value);
        return;
      }
      activeIndex = Math.max(0, activeIndex - 1);
      updateActiveOption();
      return;
    }
    if (event.key === "Enter" && !list.hidden) {
      event.preventDefault();
      chooseStation(activeIndex);
      return;
    }
    if (event.key === "Escape") {
      closeList();
      return;
    }
    if (event.key === "Tab") {
      closeList();
    }
  });

  document.addEventListener("pointerdown", (event) => {
    if (!picker.contains(event.target)) {
      closeList();
    }
  });
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
    return;
  }

  if (activeOptions === totalOptions) {
    telegramBadge.textContent = "Acık";
    telegramBadge.classList.add("state-on");
    return;
  }

  telegramBadge.textContent = "Kısmen Acık";
  telegramBadge.classList.add("state-partial");
}

function pad2(value) {
  return String(value).padStart(2, "0");
}

function formatDateDigits(digits) {
  const day = digits.slice(0, 2);
  const month = digits.slice(2, 4);
  const year = digits.slice(4, 8);
  let formatted = day;
  if (month) {
    formatted += `/${month}`;
  }
  if (year) {
    formatted += `/${year}`;
  }
  return formatted;
}

function formatTimeDigits(digits) {
  const hour = digits.slice(0, 2);
  const minute = digits.slice(2, 4);
  return minute ? `${hour}:${minute}` : hour;
}

function parseDateTr(value) {
  const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec((value || "").trim());
  if (!match) {
    return null;
  }
  const day = Number(match[1]);
  const month = Number(match[2]);
  const year = Number(match[3]);
  const parsed = new Date(year, month - 1, day);
  if (
    parsed.getFullYear() !== year ||
    parsed.getMonth() !== month - 1 ||
    parsed.getDate() !== day
  ) {
    return null;
  }
  parsed.setHours(0, 0, 0, 0);
  return parsed;
}

function isValidTimeValue(value) {
  return /^([01]\d|2[0-3]):[0-5]\d$/.test((value || "").trim());
}

function normalizeTimeInput(input) {
  const digits = input.value.replace(/\D/g, "");
  let hour;
  let minute;

  if (digits.length === 3) {
    hour = digits.slice(0, 1);
    minute = digits.slice(1, 3);
  } else {
    hour = digits.slice(0, 2);
    minute = digits.slice(2, 4);
  }

  if (hour && minute) {
    input.value = `${pad2(Number(hour))}:${pad2(Number(minute))}`;
  }
}

function setTodayDefaults() {
  const dateField = form.elements.tarih;
  const timeField = form.elements.saat;
  const now = new Date();

  dateField.value = `${pad2(now.getDate())}/${pad2(now.getMonth() + 1)}/${now.getFullYear()}`;
  timeField.value = `${pad2(now.getHours())}:${pad2(now.getMinutes())}`;
}

function attachDateTimeMasks() {
  const dateField = form.elements.tarih;
  const timeField = form.elements.saat;

  dateField.addEventListener("input", () => {
    const digits = dateField.value.replace(/\D/g, "").slice(0, 8);
    dateField.value = formatDateDigits(digits);
  });

  timeField.addEventListener("input", () => {
    const digits = timeField.value.replace(/\D/g, "").slice(0, 4);
    timeField.value = formatTimeDigits(digits);
  });

  timeField.addEventListener("blur", () => normalizeTimeInput(timeField));
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

function syncCaptchaModal(data) {
  if (!captchaModal) {
    return;
  }
  if (data.captcha) {
    if (!captchaDismissed) {
      openModal(captchaModal);
    }
    return;
  }
  captchaDismissed = false;
  closeModal(captchaModal);
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

  runningLoader.classList.toggle("is-hidden", !data.running);

  setTextIfPresent(attemptCount, String(data.attempt ?? 0));
  startedAt.textContent = data.started_at || "-";
  finishedAt.textContent = data.finished_at || "-";
  statusEcho.textContent = data.status || "Beklemede";
  applyStatusTone(data);
  syncCaptchaModal(data);

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
    nereden: form.elements.nereden.value.trim(),
    nereye: form.elements.nereye.value.trim(),
    tarih: form.elements.tarih.value.trim(),
    saat: form.elements.saat.value.trim(),
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

  const selectedDate = parseDateTr(form.elements.tarih.value);
  if (!selectedDate) {
    alert("Tarihi GG/AA/YYYY formatında girin. Örnek: 01/11/2026");
    form.elements.tarih.focus();
    return;
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  if (selectedDate < today) {
    alert("Bugünden daha eski bir tarih seçilemez.");
    form.elements.tarih.focus();
    return;
  }

  if (!isValidTimeValue(form.elements.saat.value)) {
    alert("Saati 24 saat formatında SS:DD olarak girin. Örnek: 14:30");
    form.elements.saat.focus();
    return;
  }

  const nereden = form.elements.nereden.value.trim();
  const nereye = form.elements.nereye.value.trim();
  if (!stationList.includes(nereden) || !stationList.includes(nereye)) {
    alert("Lütfen kalkış ve varış istasyonlarını listeden seçin.");
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
attachDateTimeMasks();
document.querySelectorAll("[data-station-picker]").forEach(setupStationPicker);
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

document.querySelectorAll("[data-close-captcha]").forEach((button) => {
  button.addEventListener("click", () => {
    captchaDismissed = true;
    closeModal(captchaModal);
  });
});

document.addEventListener("click", (event) => {
  if (event.target.classList.contains("modal")) {
    if (event.target === captchaModal) {
      captchaDismissed = true;
    }
    closeModal(event.target);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    if (captchaModal && !captchaModal.classList.contains("is-hidden")) {
      captchaDismissed = true;
    }
    closeModal(howItWorksModal);
    closeModal(ticketFoundModal);
    closeModal(captchaModal);
  }
});

refreshStatus();
refreshLogs();
setInterval(() => {
  refreshStatus();
  refreshLogs();
}, 3000);
