class AudioEngine {
  constructor() {
    this.ctx = null;
    this.masterGain = null;
    this.lastBeatTime = 0;
    this.beatInterval = 1000; // ms

    // Audio nodes
    this.droneOsc = null;
    this.droneGain = null;
    this.windNode = null;
    this.windGain = null;
    this.ritualOsc = null;
    this.ritualGain = null;
  }

  async init() {
    if (this.ctx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContext();
    this.masterGain = this.ctx.createGain();
    this.masterGain.gain.value = 0.3; // Master Volume
    this.masterGain.connect(this.ctx.destination);

    this.startDrone();
    this.startWind();
    console.log("Audio Engine: Initialized");
  }

  startDrone() {
    this.droneOsc = this.ctx.createOscillator();
    this.droneOsc.type = "sine";
    this.droneOsc.frequency.value = 55; // Low A
    this.droneGain = this.ctx.createGain();
    this.droneGain.gain.value = 0.1;
    this.droneOsc.connect(this.droneGain);
    this.droneGain.connect(this.masterGain);
    this.droneOsc.start();
  }

  startWind() {
    const bufferSize = 2 * this.ctx.sampleRate;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
    this.windNode = this.ctx.createBufferSource();
    this.windNode.buffer = buffer;
    this.windNode.loop = true;

    const filter = this.ctx.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.value = 400;

    this.windGain = this.ctx.createGain();
    this.windGain.gain.value = 0.05;
    this.windNode.connect(filter);
    filter.connect(this.windGain);
    this.windGain.connect(this.masterGain);
    this.windNode.start();
  }

  updateAtmosphere(sanity, resonance) {
    if (!this.ctx) return;

    // Resonance Pitch
    const targetPitch = 45 + (resonance / 100) * 20;
    this.droneOsc.frequency.setTargetAtTime(
      targetPitch,
      this.ctx.currentTime,
      2,
    );

    // Heartbeat
    if (sanity < 40) {
      const urgency = 1 - sanity / 40;
      const interval = 1200 - urgency * 800;
      if (Date.now() - this.lastBeatTime > interval) {
        this.playHeartbeat(urgency);
        this.lastBeatTime = Date.now();
      }
    }
  }

  playHeartbeat(urgency) {
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.frequency.value = 50;
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.5 * urgency + 0.1, t + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(t);
    osc.stop(t + 0.2);
  }

  playClick(type) {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    // Specialized sounds
    if (type === "faith") {
      // Chime
      osc.type = "sine";
      osc.frequency.setValueAtTime(800, t);
      osc.frequency.exponentialRampToValueAtTime(400, t + 0.5);
      gain.gain.setValueAtTime(0.1, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.5);
    } else if (type === "doubt") {
      // Dull Thud
      osc.type = "square";
      osc.frequency.value = 100;
      gain.gain.setValueAtTime(0.1, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
    } else if (type === "resolve") {
      // Sharp strike
      osc.type = "triangle";
      osc.frequency.value = 400;
      gain.gain.setValueAtTime(0.1, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
    } else {
      // Generic
      osc.frequency.value = 600;
      gain.gain.setValueAtTime(0, t);
      gain.gain.linearRampToValueAtTime(0.1, t + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
    }

    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(t);
    osc.stop(t + 0.5);
  }

  playAscend() {
    if (!this.ctx) return;
    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(100, t);
    osc.frequency.exponentialRampToValueAtTime(800, t + 2);
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.3, t + 1);
    gain.gain.linearRampToValueAtTime(0, t + 4);
    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(t);
    osc.stop(t + 4);
  }
}

const audio = new AudioEngine();
