// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { useCoherenceStore } from '../../store/coherenceStore';
import { DispatchResult } from '@essence/types';
import { autoRepairApprovedTasks } from '../repairService';

export const handleUtilityCommand = async (
    commandId: string,
    params: Record<string, unknown>,
): Promise<DispatchResult | null> => {
    const { addNovaSpark, maintenanceMode } = useCoherenceStore.getState();

    switch (commandId) {
        case 'CMD_INITIATE_AUTO_REPAIR': {
            const isSovereign = maintenanceMode === 'Sovereign';
            addNovaSpark(`Initiating ${isSovereign ? 'Sovereign' : 'Permissioned'} Repair Cycle...`);
            
            try {
                const result = await autoRepairApprovedTasks(isSovereign);
                return {
                    success: true,
                    message: `Autonomous agents deployed. Successfully resolved ${result.count} dissonances.`,
                };
            } catch (error) {
                const msg = error instanceof Error ? error.message : String(error);
                return { success: false, message: `Repair Fault: ${msg}` };
            }
        }

        case 'CMD_EXECUTE_DIRECTIVE': {
            // This is a placeholder for the future LLM-integrated directive engine.
            const instruction = params.instruction as string;
            addNovaSpark(`Directive Received: ${instruction}`);
            return {
                success: true,
                message: `The directive has been parsed and transmitted to the Cognitive Core.`,
            };
        }

        default:
            return null;
    }
};
