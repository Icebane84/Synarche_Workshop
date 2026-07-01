// src/system/signalBus.ts
import * as net from 'net';
import { useStore } from '../store';

export class SovereignSignalBusBridge {
    private clientSocket: net.Socket | null = null;
    private targetPort: number = 9999;
    private targetHost: string = '127.0.0.1';

    public initializeVisualHUDConnection(): void {
        this.clientSocket = new net.Socket();

        this.clientSocket.connect(this.targetPort, this.targetHost, () => {
            console.log('[SIGNAL-BUS] Coherence monitoring tunnel stabilized.');
        });

        this.clientSocket.on('data', (incoming_stream) => {
            const individual_lines = incoming_stream.toString().split('\n');
            for (const data_line of individual_lines) {
                if (!data_line.trim()) continue;
                try {
                    const parsed_packet = JSON.parse(data_line);
                    
                    // Route metrics directly to Zustand store array slicing
                    useStore.getState().addLog({
                        id: crypto.randomUUID(),
                        type: parsed_packet.event === 'CREATED' ? 'success' : 'system',
                        message: `[${parsed_packet.domain}] ${parsed_packet.event}: ${parsed_packet.path.replace(/^\.\//, '')}`,
                        timestamp: parsed_packet.timestamp
                    });
                } catch (json_error) {
                    // Prevent frame rendering slips from packet fracturing
                }
            }
        });

        this.clientSocket.on('close', () => {
            console.log('[SIGNAL-BUS] Connection interrupted. Running telemetry recovery path...');
            setTimeout(() => this.initializeVisualHUDConnection(), 2500);
        });

        this.clientSocket.on('error', () => {
            // Absorb silent interface skips when backend daemon is recycling
        });
    }
}