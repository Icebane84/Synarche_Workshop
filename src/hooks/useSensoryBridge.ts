// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { useEffect, useRef } from 'react';
import { useCoherenceStore } from '../store/coherenceStore';
import { fetchEnvironmentalData, getSystemTime } from '../services/sensoryService';

/**
 * A hook that activates the Neural Sensory Bridge.
 * It manages the clock tick, initiates the environmental data handshake,
 * and performs dynamic system adjustments based on the environment (Bio-Feedback).
 */
export const useSensoryBridge = () => {
    const updateSensoryData = useCoherenceStore(state => state.updateSensoryData);
    const setCognitiveFocus = useCoherenceStore(state => state.setCognitiveFocus);
    const addNovaSpark = useCoherenceStore(state => state.addNovaSpark);
    
    // Use a ref to prevent re-running the bio-feedback loop unnecessarily
    const hasCalibratedRef = useRef(false);

    useEffect(() => {
        // 1. Initialize Clock
        const timeInterval = setInterval(() => {
            updateSensoryData({ 
                timestamp: Date.now(), 
                timeString: getSystemTime() 
            });
        }, 1000);

        // 2. Initialize Environmental Sensors (Location/Weather)
        const initSensors = async () => {
            if (hasCalibratedRef.current) return;
            
            updateSensoryData({ status: 'calibrating' });
            const data = await fetchEnvironmentalData();
            updateSensoryData(data);
            hasCalibratedRef.current = true;

            // 3. Bio-Feedback Loop: Adjust Cognitive State based on Environment
            if (data.weather) {
                const { conditionCode, isDay, conditionText } = data.weather;
                const currentFocus = useCoherenceStore.getState().cognitiveFocus;

                // Protocol: Storm Guard
                // If severe weather (Thunderstorm), shift to Security Audit to "protect" system integrity.
                if (conditionCode >= 95) {
                    if (currentFocus !== 'Security Audit') {
                        setCognitiveFocus('Security Audit');
                        addNovaSpark(`⚠️ ATMOSPHERIC ALERT: ${conditionText} detected. System automatically shifted to Security Audit protocols.`);
                    }
                }
                
                // Protocol: Nocturnal Synthesis
                // If it is night and the system is standard, suggest Creative Ideation.
                else if (!isDay) {
                    addNovaSpark("Nocturnal cycle detected. Environmental parameters are conducive to Creative Ideation.");
                    // We don't force switch here to be less intrusive, but we acknowledge it.
                }

                // Protocol: Clarity
                else if (conditionCode === 0 && isDay) {
                     addNovaSpark("Solar interference nominal. Operational clarity at peak levels.");
                }
            }
        };

        initSensors();

        return () => { clearInterval(timeInterval); };
    }, [updateSensoryData, setCognitiveFocus, addNovaSpark]);
};