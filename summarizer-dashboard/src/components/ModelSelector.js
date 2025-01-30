import React from 'react';

const ModelSelector = ({ model, setModel }) => {
    return (
        <select value={model} onChange={(e) => setModel(e.target.value)}>
            <option value="bart">BART</option>
            <option value="t5">T5</option>
            <option value="gpt">GPT-3/4</option>
            {/* <option value="deepseek">DeepSeek</option> */}
        </select>
    );
};

export default ModelSelector;
