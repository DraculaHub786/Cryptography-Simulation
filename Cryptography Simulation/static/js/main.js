document.addEventListener('DOMContentLoaded', () => {
    const cipherSelect = document.getElementById('cipher-select');
    const keyGroup = document.getElementById('key-group');
    const keyLabel = document.getElementById('key-label');
    const keyInput = document.getElementById('key-input');
    const operationGroup = document.getElementById('operation-group');
    const inputText = document.getElementById('input-text');
    const processBtn = document.getElementById('process-btn');
    const simArea = document.getElementById('simulation-area');
    const finalOutput = document.getElementById('final-output');
    const speedSlider = document.getElementById('speed-slider');
    
    // Operation radios
    const opRadios = document.querySelectorAll('input[name="operation"]');
    
    function updateUIForAlgorithm(value) {
        // Reset defaults
        keyGroup.style.display = 'flex';
        operationGroup.style.display = 'flex';
        
        const currentOp = document.querySelector('input[name="operation"]:checked').value;
        const btnText = processBtn.querySelector('.btn-text');
        btnText.textContent = `Simulate ${currentOp === 'encrypt' ? 'Encryption' : 'Decryption'}`;

        if (value === 'caesar') {
            keyLabel.textContent = 'Shift Value (Number)';
            keyInput.placeholder = 'e.g., 3';
            keyInput.value = '3';
        } else if (value === 'vigenere') {
            keyLabel.textContent = 'Key Phrase (Letters only)';
            keyInput.placeholder = 'e.g., SECRET';
            keyInput.value = 'SECRET';
        } else if (value === 'aes') {
            keyLabel.textContent = 'Key (16 chars for AES-128)';
            keyInput.placeholder = 'e.g., 16_byte_key_here';
            keyInput.value = 'sixteen byte key'; // Exactly 16 chars
        } else if (value === 'md5' || value === 'sha256') {
            // Hashes don't need a key here, and they only "hash" (encrypt route)
            keyGroup.style.display = 'none';
            operationGroup.style.display = 'none'; // Lock operation to hash visually
            // Force encrypt selection logically
            document.getElementById('encrypt-radio').checked = true;
            btnText.textContent = 'Simulate Hashing';
        }
    }

    // Init UI
    updateUIForAlgorithm(cipherSelect.value);

    // Update UI on select change
    cipherSelect.addEventListener('change', (e) => {
        updateUIForAlgorithm(e.target.value);
    });
    
    // Handle operation toggle text update
    opRadios.forEach(radio => {
        radio.addEventListener('change', () => {
             // Only matters if we aren't hashing, but change handler exists
            const value = cipherSelect.value;
            if(value !== 'md5' && value !== 'sha256') {
                 const op = document.querySelector('input[name="operation"]:checked').value;
                 processBtn.querySelector('.btn-text').textContent = op === 'encrypt' ? 'Simulate Encryption' : 'Simulate Decryption';
            }
        });
    });

    processBtn.addEventListener('click', async () => {
        const text = inputText.value;
        const cipher = cipherSelect.value;
        const key = keyInput.value;
        const operation = document.querySelector('input[name="operation"]:checked').value;
        
        if (!text) {
            alert("Please enter some data to process.");
            return;
        }

        if ((cipher === 'caesar' || cipher === 'vigenere' || cipher === 'aes') && !key) {
            alert("Please enter a key.");
            return;
        }

        // Prepare UI for simulation
        processBtn.disabled = true;
        simArea.innerHTML = ''; // Clear previous simulation
        finalOutput.textContent = 'Processing...';
        finalOutput.style.color = 'var(--text-secondary)';

        try {
            // For hashes, backend only expects /encrypt route technically because it only moves one way.
            const endPoint = operation === 'encrypt' ? '/api/encrypt' : '/api/decrypt';
            
            const response = await fetch(endPoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text, cipher, key })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'API Error');
            }

            // Start Animation Sequence
            await runSimulation(data.steps, data.cipher, data.result);
            
            finalOutput.style.color = 'var(--neon-cyan)';
            finalOutput.textContent = data.result;

        } catch (error) {
            console.error(error);
            simArea.innerHTML = `<div class="sim-step" style="border-left-color: var(--error-red);">
                <span style="color: var(--error-red);">Error: ${error.message}</span>
            </div>`;
            finalOutput.style.color = 'var(--error-red)';
            finalOutput.textContent = 'Transaction Failed.';
        } finally {
            processBtn.disabled = false;
        }
    });

    async function runSimulation(steps, cipherType, finalResult) {
        let speed = parseInt(speedSlider.value, 10);
        
        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            const stepElement = document.createElement('div');
            stepElement.className = 'sim-step';
            
            if (cipherType === 'md5' || cipherType === 'sha256') {
                stepElement.classList.add('hash-step');
            }
            
            speed = parseInt(speedSlider.value, 10); // Check speed dynamically slider
            
            if (cipherType === 'caesar') {
                stepElement.innerHTML = buildCaesarStepHTML(step);
            } else if (cipherType === 'vigenere') {
                stepElement.innerHTML = buildVigenereStepHTML(step);
            } else if (cipherType === 'aes') {
                stepElement.innerHTML = buildAESStepHTML(step);
            } else if (cipherType === 'md5' || cipherType === 'sha256') {
                stepElement.innerHTML = buildHashStepHTML(step);
            }
            
            simArea.appendChild(stepElement);
            simArea.scrollTop = simArea.scrollHeight; // Auto scroll
            
            // Wait before next frame
            await new Promise(resolve => setTimeout(resolve, speed));
        }
        
        // Final completion flash
        simArea.innerHTML += `<div class="sim-step" style="border-left-color: var(--success-green); text-align: center; color: var(--success-green); font-weight: bold; background: rgba(16, 185, 129, 0.1);">
            Simulation Complete
        </div>`;
        simArea.scrollTop = simArea.scrollHeight;
    }

    function buildCaesarStepHTML(step) {
        if (!step.isAlpha) {
            return `<div class="step-details">
                <span class="char-box">${step.char === ' ' ? 'SPC' : step.char}</span>
                <span class="arrow">PASS</span>
                <span class="char-box result">${step.newChar === ' ' ? 'SPC' : step.newChar}</span>
            </div>`;
        }
        return `<div class="step-details">
            <span class="char-box highlight">${step.char}</span>
            <span class="arrow">SHIFT [${step.shift > 0 ? '+'+step.shift : step.shift}] ➔</span>
            <span class="char-box result">${step.newChar}</span>
            <span class="formula">${step.formula}</span>
        </div>`;
    }

    function buildVigenereStepHTML(step) {
         if (!step.isAlpha) {
            return `<div class="step-details">
                <span class="char-box">${step.char === ' ' ? 'SPC' : step.char}</span>
                <span class="arrow">PASS</span>
                <span class="char-box result">${step.newChar === ' ' ? 'SPC' : step.newChar}</span>
            </div>`;
        }
        return `<div class="step-details">
            <span class="char-box highlight">${step.char}</span>
            <span class="arrow">⊕</span>
            <div style="text-align:center; font-size:0.75rem;">
                <span class="char-box" style="width:2.5rem;height:2.5rem;border-color:var(--neon-purple);color:var(--neon-purple);">${step.keyChar}</span>
            </div>
            <span class="arrow">➔</span>
            <span class="char-box result">${step.newChar}</span>
            <span class="formula">${step.formula}</span>
        </div>`;
    }
    
    function buildAESStepHTML(step) {
        let html = `<div class="data-block-container">
            <div class="data-block-header">${step.action}</div>
            <div class="hex-data">${step.blockHex_in}</div>`;
            
        if (step.complex_params && step.complex_params.length > 0) {
            html += `<div class="complex-params-container">`;
            step.complex_params.forEach(round => {
                html += `<div class="complex-param-group">
                    <span class="param-title">Virtual Round ${round.round} Approximation</span>
                    <div class="param-grid">`;
                
                for (const [key, value] of Object.entries(round)) {
                    if(key !== 'round') {
                        let displayKey = key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                        html += `<div class="param-grid-item">
                            <span class="param-grid-key">${displayKey}</span>
                            <span class="param-grid-val">${value}</span>
                        </div>`;
                    }
                }
                html += `</div></div>`;
            });
            html += `</div>`;
        }

        html += `<div class="arrow text-center" style="margin: 0 auto; margin-top: 10px;">▼</div>
            <div class="hex-data output">${step.blockHex_out}</div>
        </div>`;
        return html;
    }
    
    function buildHashStepHTML(step) {
        let html = `<div class="data-block-container">
            <div class="data-block-header">${step.action}</div>
            <div class="process-detail">${step.detail}</div>`;
            
        if (step.complex_params) {
            html += `<div class="complex-params-container param-grid">`;
            for (const [key, value] of Object.entries(step.complex_params)) {
               html += `<div class="param-grid-item" style="border-left-color: var(--neon-pink);">
                    <span class="param-grid-key">${key}</span>
                    <span class="param-grid-val">${value}</span>
                </div>`;
            }
            html += `</div>`;
        }
            
        if (step.chunk_hex) {
            html += `<div style="margin-top: 5px; font-size: 0.8rem; color: var(--text-secondary);">Chunk Data:</div>`;
            html += `<div class="hex-data">${step.chunk_hex}</div>`;
        }
        
        if (step.final_hash) {
            html += `<div class="arrow text-center" style="margin: 0 auto; color: var(--neon-pink);">▼ FINAL DIGEST ▼</div>`;
            html += `<div class="hex-data output" style="border-left-color: var(--neon-pink); color: var(--neon-pink);">${step.final_hash}</div>`;
        }
        
        html += `</div>`;
        return html;
    }
});
