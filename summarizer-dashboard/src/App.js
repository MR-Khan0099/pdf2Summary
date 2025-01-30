import React, { useState } from 'react';
import axios from 'axios';

const SummarizerDashboard = () => {
    const [file, setFile] = useState(null);
    const [model, setModel] = useState('bart');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleModelChange = (e) => {
        setModel(e.target.value);
    };

    const handleSubmit = async () => {
        if (!file) {
            alert('Please upload a PDF!');
            return;
        }
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model', model);

        try {
            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSummary(response.data.summary);
        } catch (error) {
            console.error(error);
            alert('Error generating summary!');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard">
            <h1>PDF Summarizer</h1>
            
            <input type="file" onChange={handleFileChange} />
            
            <select value={model} onChange={handleModelChange}>
                <option value="bart">BART</option>
                <option value="t5">T5</option>
                <option value="gpt">GPT-3/4</option>
                <option value="deepseek">DeepSeek</option>
            </select>
            
            <button onClick={handleSubmit} disabled={loading}>
                {loading ? 'Summarizing...' : 'Generate Summary'}
            </button>
            
            {summary && (
                <div>
                    <h3>Summary</h3>
                    <p>{summary}</p>
                </div>
            )}
        </div>
    );
};

export default SummarizerDashboard;
