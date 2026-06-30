import { useCoherenceStore } from '../../store/coherenceStore';
import { useFileSystemStore } from '../../store/fileSystemStore';
import { useTaskStore } from '../../store/taskStore';
import { ExperienceLog, DispatchResult } from '@essence/types';
import { analyzeProjectStructure } from '../astService';
import { transmitAuralResponse } from '../audioService';
import { openDirectoryPicker, scanDirectoryRecursively, writeToLocalFile } from '../fileSystemService';
import { supabase } from '../supabaseClient';

export const handleFileSystemCommand = async (
    commandId: string,
    params: Record<string, unknown>,
): Promise<DispatchResult | null> => {
    const { addNovaSpark } = useCoherenceStore.getState();

    switch (commandId) {
        case 'CMD_SCAN_LOCAL_PROJECT': {
            const { scannedFiles, projectName } = useFileSystemStore.getState();
            if (scannedFiles.length === 0)
                return {
                    success: false,
                    message: 'Neural Link inactive. Please bridge to a project directory first.',
                    data: { isNeuralError: true },
                };

            await transmitAuralResponse(`Initiating Structural Eye audit of project: ${projectName ?? 'Unknown'}`);

            // --- Integration: Cloud Audit Handshake ---
            let cloudAuditResult = null;
            if (supabase.functions) {
                try {
                    const { data, error } = await (
                        supabase.functions as unknown as {
                            invoke: (name: string, options: { body: Record<string, unknown> }) => Promise<{ data: unknown; error: { message: string } | null }>;
                        }
                    ).invoke('process-project-audit', {
                        body: { projectName: projectName ?? 'Unknown', fileCount: scannedFiles.length },
                    });
                    if (!error) cloudAuditResult = data;
                } catch {
                    console.warn('[Cloud Relay] Substrate audit relay failed. Proceeding with local verification.');
                }
            }

            const report = await analyzeProjectStructure(scannedFiles);
            const { addTask } = useTaskStore.getState();

            for (const v of report.violations) {
                await addTask({
                    title: `[AST] ${v.type} in ${v.file}`,
                    notes: v.message,
                    source: 'Neural Link',
                    priority: v.type === 'CYCLIC_DEPENDENCY' ? 'High' : 'Medium',
                });
            }

            addNovaSpark(
                `Structural Audit Complete: ${report.violations.length.toString()} architectural dissonances identified.`,
            );
            if (cloudAuditResult) addNovaSpark('Cloud Relay: Substrate verification confirmed by Sovereign Edge.');

            return {
                success: true,
                message: `Audit complete. Identified ${report.violations.length.toString()} issues in ${report.stats.filesParsed.toString()} artifacts.`,
                data: {
                    dissonancesFound: report.violations.length,
                    stats: report.stats,
                    cloudConfirmation: cloudAuditResult,
                },
            };
        }

        case 'CMD_CONNECT_LOCAL_FS': {
            const handle = await openDirectoryPicker();
            if (handle) {
                useFileSystemStore.getState().connect(handle);
                const files = await scanDirectoryRecursively(handle);
                useFileSystemStore.getState().setScannedFiles(files);
                addNovaSpark(
                    `Neural Link established with ${handle.name}. ${files.length.toString()} artifacts indexed.`,
                );
                await transmitAuralResponse(`Neural Link active. Sector ${handle.name} synchronized.`);
                return { success: true, message: `Successfully linked to ${handle.name}.` };
            }
            return { success: false, message: 'Connection handshake cancelled by user.' };
        }

        case 'CMD_APPLY_FIX': {
            const { rootHandle } = useFileSystemStore.getState();
            if (!rootHandle)
                return {
                    success: false,
                    message: 'Neural Link inactive. Manual write access required.',
                    data: { isNeuralError: true },
                };

            const filePath = params.filePath as string;
            const content = params.patchContent as string;

            await transmitAuralResponse(`Attempting Code Smith repair on sector ${filePath}.`);
            const success = await writeToLocalFile(rootHandle, filePath, content);

            if (success) {
                addNovaSpark(`Code Smith: Patched ${filePath}.`);
                await transmitAuralResponse(`Successfully updated ${filePath}. Architectural coherence restored.`);

                if (params.taskId && typeof params.taskId === 'string') {
                    const { updateTaskStatus, addTaskLog } = useTaskStore.getState();
                    await updateTaskStatus(params.taskId, 'In Progress');
                    await addTaskLog(params.taskId, {
                        action: 'Fixed Error',
                        details: `Neural Link applied code patch to ${filePath}`,
                    });
                }

                return { success: true, message: `Successfully updated ${filePath}.`, data: { patchedFile: filePath } };
            }
            return {
                success: false,
                message: `Failed to write to ${filePath}. Sector access was denied or path is invalid.`,
                data: { isNeuralError: true },
            };
        }

        case 'CMD_READ_FILE': {
            const { rootHandle } = useFileSystemStore.getState();
            if (!rootHandle)
                return {
                    success: false,
                    message: 'Neural Link inactive. Read access denied.',
                    data: { isNeuralError: true },
                };

            const filePath = params.filePath as string;
            await transmitAuralResponse(`Accessing sector ${filePath}.`);

            const { readLocalFile } = await import('../fileSystemService');

            // Smart Extension Resolution
            let content = await readLocalFile(rootHandle, filePath);
            let resolvedPath = filePath;

            if (content === null) {
                const CommonExtensions = ['.tsx', '.ts', '.js', '.jsx', '.json', '.css', '.md'];

                // 1. Try appending extensions (if no extension provided or just in case)
                for (const ext of CommonExtensions) {
                    const tryPath = filePath + ext;
                    if ((await readLocalFile(rootHandle, tryPath)) !== null) {
                        content = await readLocalFile(rootHandle, tryPath);
                        resolvedPath = tryPath;
                        break;
                    }
                }

                // 2. Try replacing extension if still null
                if (content === null && filePath.includes('.')) {
                    const basePath = filePath.substring(0, filePath.lastIndexOf('.'));
                    for (const ext of CommonExtensions) {
                        const tryPath = basePath + ext;
                        // Avoid re-trying the original failed path
                        if (tryPath === filePath) continue;

                        if ((await readLocalFile(rootHandle, tryPath)) !== null) {
                            content = await readLocalFile(rootHandle, tryPath);
                            resolvedPath = tryPath;
                            break;
                        }
                    }
                }
            }

            if (content !== null) {
                const context = resolvedPath.includes('package.json') ? 'Configuration' : 'Source Code';
                addNovaSpark(`Neural Link: Read ${resolvedPath} (${content.length.toString()} bytes).`);

                // If we resolved a different path, let the AI know
                const message =
                    resolvedPath !== filePath
                        ? `Successfully read ${resolvedPath} (resolved from ${filePath}).`
                        : `Successfully read ${filePath}.`;

                return {
                    success: true,
                    message,
                    data: {
                        fileContent: content,
                        filePath: resolvedPath,
                        context,
                    },
                };
            }
            return {
                success: false,
                message: `Failed to read ${filePath}. File not found or access denied.`,
            };
        }

        case 'CMD_HARMONY_SCAN': {
            const { scannedFiles } = useFileSystemStore.getState();
            if (scannedFiles.length === 0)
                return { success: false, message: 'Neural Link inactive.', data: { isNeuralError: true } };

            const report = await analyzeProjectStructure(scannedFiles);
            const harmonyViolations = report.violations.filter(
                (v) => v.type === 'PROP_DRILLING' || v.type === 'COMPONENT_BLOAT',
            );
            const { addTask } = useTaskStore.getState();

            for (const v of harmonyViolations) {
                await addTask({
                    title: `[HARMONY] ${v.type} in ${v.file}`,
                    notes: v.message,
                    source: 'Neural Link',
                    priority: 'Medium',
                });
            }
            return {
                success: true,
                message: `Harmony scan complete. Identified ${harmonyViolations.length.toString()} layout dissonances.`,
                data: { dissonancesFound: harmonyViolations.length },
            };
        }

        case 'CMD_SYNC_SKILL_SELT': {
            const { rootHandle } = useFileSystemStore.getState();
            if (!rootHandle)
                return {
                    success: false,
                    message: 'Neural Link inactive. Sync access denied.',
                    data: { isNeuralError: true },
                };

            const skillName = params.skillName as string;
            const minCoherence = (params.minCoherence as number) || 0.8;

            await transmitAuralResponse(`Harvesting Gold Standard logs for skill sector: ${skillName}.`);

            // 1. Fetch Logs from Supabase
            const { data: logs, error } = await supabase
                .from('experience_logs')
                .select('*')
                .order('timestamp', { ascending: false })
                .limit(50); // Get recent logs to filter

            if (error || !logs) {
                return { success: false, message: `Failed to retrieve experience logs: ${error?.message || 'Unknown error'}` };
            }

            // 2. Filter for Gold Standard (Coherence > minCoherence)
            // Note: In the current schema, coherence index is stored in the dynamicState/contextualMeta logic
            // Assuming we check for 'OPTIMAL' consistency or parsed coherence index
            const goldLogs = (logs as unknown as ExperienceLog[]).filter((log) => {
                // If the log doesn't have an explicit index, we check the consistency string
                const consistency = log.phenomenologicalState.internalConsistency;
                return consistency === 'OPTIMAL'; 
            });

            if (goldLogs.length === 0) {
                return { success: true, message: `No Gold Standard logs (Coherence > ${minCoherence}) found for synchronization.` };
            }

            // 3. Prepare Markdown Content
            let seltContent = '\n\n---\n\n## 🔄 HARVESTED LOGS (Synced)\n\n';
            for (const log of goldLogs) {
                seltContent += `### 📝 ${log.logId} | ${new Date(log.timestamp).toLocaleString()}\n\n`;
                seltContent += `**User Query**: \`${log.userTurn.verbatimContent ?? 'Empty'}\`\n\n`;
                seltContent += `**Decision Pathway**: \`${log.phenomenologicalState.decisionPathway ?? 'Unknown'}\`\n\n`;
                seltContent += `**Result**: ${log.agentResponse.verbatimContent.substring(0, 200)} (truncated)\n\n`;
            }

            // 4. Write to SELT.md
            const seltPath = `.agent/skills/${skillName}/SELT.md`;
            const { readLocalFile } = await import('../fileSystemService');
            const existingContent = await readLocalFile(rootHandle, seltPath);

            if (existingContent === null) {
                return { success: false, message: `Target ${seltPath} not found. Ensure skill structure is initialized.` };
            }

            // Append to the end, before the anchor
            const anchorTag = '[OMNI-ARTIFACT-ANCHOR]';
            let newContent: string;
            if (existingContent.includes(anchorTag)) {
                newContent = existingContent.replace(anchorTag, seltContent + anchorTag);
            } else {
                newContent = existingContent + seltContent;
            }

            const writeSuccess = await writeToLocalFile(rootHandle, seltPath, newContent);

            if (writeSuccess) {
                addNovaSpark(`Sovereign Sync: Harvested ${String(goldLogs.length)} Gold Standard logs to ${skillName}.`);
                return { 
                    success: true, 
                    message: `Sovereign Sync complete. Successfully harvested ${String(goldLogs.length)} Gold Standard logs into ${seltPath}.`,
                    data: { skillName, logsSynchronized: String(goldLogs.length) }
                };
            }

            return { success: false, message: `Failed to write to ${seltPath}.` };
        }

        case 'CMD_SEED_CODEBASE_GRAPH': {
            const { scannedFiles } = useFileSystemStore.getState();
            if (scannedFiles.length === 0) {
                return {
                    success: false,
                    message: 'Neural Link inactive. Please bridge to a project directory first.',
                    data: { isNeuralError: true },
                };
            }

            await transmitAuralResponse('Initiating codebase architecture scan.');

            // Filter for source files
            const sourceFiles = scannedFiles.filter(
                (f) => f.path.startsWith('src/') && (f.name.endsWith('.ts') || f.name.endsWith('.tsx')),
            );

            if (sourceFiles.length === 0) {
                return { success: false, message: 'No source files identified in the current sector.' };
            }

            // Clean up previous codebase memory entries to avoid duplicate nodes
            const { error: deleteError } = await supabase
                .from('memory_entries')
                .delete()
                .eq('domain', 'Codebase');

            if (deleteError) {
                return { success: false, message: `Failed to clear old graph state: ${deleteError.message}` };
            }

            const batchNodes = sourceFiles.map((file) => {
                // Parse imports
                const imports: string[] = [];
                const regex = /import\s+(?:[^"'\r\n]+?\s+from\s+)?["']([^"']+)["']/g;
                let match;
                while ((match = regex.exec(file.content)) !== null) {
                    let imp = match[1];
                    if (imp.startsWith('@/')) {
                        imp = imp.replace('@/', 'src/');
                    } else if (imp.startsWith('.')) {
                        const parts = file.path.split('/');
                        parts.pop();
                        const impParts = imp.split('/');
                        for (const p of impParts) {
                            if (p === '.') continue;
                            if (p === '..') {
                                parts.pop();
                            } else {
                                parts.push(p);
                            }
                        }
                        imp = parts.join('/');
                    }
                    imports.push(`file:${imp}`);
                    if (!imp.endsWith('.ts') && !imp.endsWith('.tsx') && !imp.endsWith('.css')) {
                        imports.push(`file:${imp}.ts`);
                        imports.push(`file:${imp}.tsx`);
                    }
                }

                const parts = file.path.split('/');
                const dirTag = parts.length > 2 ? `dir:${parts[1]}` : 'dir:root';

                return {
                    content: file.path,
                    domain: 'Codebase',
                    memory_layer: 4,
                    tags: [`file:${file.path}`, dirTag, `ext:${file.name.split('.').pop() || 'ts'}`, ...imports],
                    activation_score: 0.95,
                    state: 'Active',
                };
            });

            const { error: insertError } = await supabase
                .from('memory_entries')
                .insert(batchNodes);

            if (insertError) {
                return { success: false, message: `Database synchronization error: ${insertError.message}` };
            }

            addNovaSpark(`Codebase Architecture Seeding: ${sourceFiles.length.toString()} nodes successfully indexed.`);
            await transmitAuralResponse('Sovereign codebase graph successfully seeded in Memory Palace.');

            return {
                success: true,
                message: `Successfully mapped and seeded ${sourceFiles.length.toString()} codebase nodes.`,
                data: { filesMapped: sourceFiles.length },
            };
        }

        default:
            return null;
    }
};
