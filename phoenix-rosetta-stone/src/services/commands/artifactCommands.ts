import { graphData } from '../../data/graphData';
import { DispatchResult } from '@essence/types';
import { queryCognitiveCore } from '../gemini';
import { getDocumentById } from '../vectorStore';

export const handleArtifactCommand = async (
    commandId: string,
    params: Record<string, unknown>,
): Promise<DispatchResult | null> => {
    // Some commands might not use store directly but keeping signature consistent
    // const { addNovaSpark } = useCoherenceStore.getState();

    switch (commandId) {
        case 'CMD_FETCH_ARTIFACT_METADATA': {
            const artifactId = params.artifactId as string;
            const doc = getDocumentById(artifactId);
            if (doc) {
                return {
                    success: true,
                    message: `Retrieved metadata from Neural Archive: ${doc.title}`,
                    data: {
                        id: doc.id,
                        title: doc.title,
                        type: doc.type,
                        contentSnippet: doc.content.substring(0, 300),
                    },
                };
            }
            const graphNode = graphData.nodes.find((n) => n.id === artifactId);
            if (graphNode) {
                return {
                    success: true,
                    message: `Retrieved metadata from Celestial Chart: ${graphNode.name}`,
                    data: {
                        id: graphNode.id,
                        title: graphNode.name,
                        type: graphNode.type,
                        contentSnippet: graphNode.description,
                    },
                };
            }
            return { success: false, message: `Artifact '${artifactId}' not found in any system vector.` };
        }

        case 'CMD_FETCH_ALL_ARTIFACTS': {
            return {
                success: true,
                message: `Retrieved ${graphData.nodes.length.toString()} artifacts from the Celestial Chart.`,
                data: { artifacts: graphData.nodes },
            };
        }

        case 'CMD_ANALYZE_ARTIFACT_SYNERGY': {
            const artifactId = params.artifactId as string;
            const node = graphData.nodes.find((n) => n.id === artifactId);
            if (!node) return { success: false, message: 'Invalid Artifact ID provided for analysis.' };

            const prompt = `Perform a deep synergy analysis for artifact: ${node.name} (${node.type}). Context: ${node.description}. Identify 3 indirect synergies with other system concepts. Output as JSON with 'message' and 'synergies' (array of strings).`;
            const aiResult = await queryCognitiveCore(prompt);
            const response = aiResult.text;

            try {
                const cleanJson = response.replace(/```json|```/g, '').trim();
                const data = JSON.parse(cleanJson) as { message: string; synergies: string[] };
                return { success: true, message: data.message, data: { synergies: data.synergies } };
            } catch {
                return { success: true, message: 'Analysis complete.', data: { synergies: [response] } };
            }
        }

        case 'CMD_SIMULATE_SYNERGY': {
            const id1 = params.artifactId1 as string;
            const id2 = params.artifactId2 as string;
            const n1 = graphData.nodes.find((n) => n.id === id1);
            const n2 = graphData.nodes.find((n) => n.id === id2);

            if (!n1 || !n2) return { success: false, message: 'Invalid Artifact IDs selected for fusion.' };

            const prompt = `Simulate the fusion of ${n1.name} and ${n2.name}. Provide a detailed 'report' in Markdown and a 'dreamUi' object with 'title', 'icon', and 'metrics' (array of {label, value, color}). Return ONLY JSON.`;
            const aiResult = await queryCognitiveCore(prompt);
            const response = aiResult.text;

            try {
                const cleanJson = response.replace(/```json|```/g, '').trim();
                const resultData = JSON.parse(cleanJson) as Record<string, unknown>;
                return { success: true, message: 'Simulation successful.', data: resultData };
            } catch (e) {
                return {
                    success: false,
                    message: `Simulation failed: ${e instanceof Error ? e.message : 'Parsing error'}`,
                };
            }
        }

        default:
            return null;
    }
};

