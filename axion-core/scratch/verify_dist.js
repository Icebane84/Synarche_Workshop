const fs = require('fs');
const path = require('path');

// Use the compiled JS files
const { validateMetadata } = require('../out/utils/validation');
const { PRS_001_SCHEMA } = require('../out/constants/schemas');

const REGISTRY_PATH = path.join(__dirname, '..', 'assets', 'PRS-001.json');

const verify = () => {
    try {
        console.log(`[VIGIL] Verifying: ${REGISTRY_PATH}`);
        const data = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
        
        validateMetadata(data, PRS_001_SCHEMA);
        
        console.log('[SUCCESS] PRS-001 integrity verified at the binary level.');
    } catch (error) {
        console.error(`[FAILURE]: ${error.message}`);
        process.exit(1);
    }
};

verify();
