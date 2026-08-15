interface SpeechRecognitionEvent extends Event {
  readonly resultIndex: number;
  readonly results: SpeechRecognitionResultList;
}

interface SpeechRecognitionErrorEvent extends Event {
  readonly error: string;
  readonly message: string;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: (event: SpeechRecognitionEvent) => void;
  onerror: (event: SpeechRecognitionErrorEvent) => void;
  onend: () => void;
  start: () => void;
  stop: () => void;
  abort: () => void;
}

interface Window {
  webkitSpeechRecognition: new () => SpeechRecognition;
  SpeechRecognition: new () => SpeechRecognition;
}

// --- OMEGA ASCENSION v3.0 PATCH: Tarot Card Module ---

interface TarotCardMetadata {
  id: string;
  name: string;
  number: number;
  keywords: string[];
  archetype: string;
  suits: string[];
  astrology: string | null;
  mythology: string | null;
}

interface TarotCardBody {
  imagery: string;
  symbolism: string;
  storytelling: string;
  shadow_aspect: string;
  modern_application: string;
}

interface TarotCardEntry {
  metadata: TarotCardMetadata;
  body: TarotCardBody;
  [key: string]: any;
}

interface TarotForgeContext {
  deck: TarotCardEntry[];
  loadDeck: (path: string) => Promise<void>;
  saveCard: (card: TarotCardEntry) => Promise<void>;
  manifestCard: (
    name: string,
    number: number,
    concept: string,
  ) => Promise<TarotCardEntry>;
}
