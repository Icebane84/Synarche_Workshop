// src/utils/PythonBridge.ts
import * as net from 'net';
import { useStore } from '../store'; // Hook straight into Zustand state core

export class VisualSignalListener {
    private client: net.Socket | null = null;
    private port: number = 9999;
    private host: string = '127.0.0.1';

    public connectEcosystemStream() {
        this.client = new net.Socket();

        this.client.connect(this.port, this.host, () => {
            console.log('[BRIDGE] Real-time visual monitoring channel secure.');
        });

        this.client.on('data', (data) => {
            const lines = data.toString().split('\n');
            for (const line of lines) {
                if (!line.trim()) continue;
                try {
                    const parsedEvent = JSON.parse(line);
                    // Dynamically push event mutations into your central Zustand store logs
                    useStore.getState().addLog({
                        id: crypto.randomUUID(),
                        type: parsedEvent.event === 'MUTATED' ? 'system' : 'success',
                        message: `[${parsedEvent.event}] Plane updated: ${parsedEvent.path}`,
                        timestamp: parsedEvent.timestamp
                    });
                } catch (e) {
                    // Ignore broken fragment splices across high-velocity packets
                }
            }
        });

        this.client.on('close', () => {
            console.log('[BRIDGE] Channel disconnected. Initializing auto-retry pass...');
            setTimeout(() => this.connectEcosystemStream(), 3000);
        });

        this.client.on('error', (err) => {
            // Keep process active if daemon hasn't initialized yet
        });
    }
}