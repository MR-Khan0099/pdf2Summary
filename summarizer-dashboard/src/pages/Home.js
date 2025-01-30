import React, { useState } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import ModelSelector from '../components/ModelSelector';
import SummaryDisplay from '../components/SummaryDisplay';

const Home = () => {
    const [file, setFile] = useState(null);
    const [model, setModel] = useState('bart');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if (!file) return alert('Upload a PDF first!');

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model', model);

        try {
            const response = await axios.post('http://localhost:8000/upload', formData);
            setSummary(response.data.summary);
        } catch (error) {
            alert('Error summarizing document');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>PDF Summarizer</h1>
            <FileUpload onFileSelect={setFile} />
            <ModelSelector model={model} setModel={setModel} />
            <button onClick={handleSubmit} disabled={loading}>{loading ? "Summarizing..." : "Generate Summary"}</button>
            <SummaryDisplay summary={summary} />
        </div>
    );
};

export default Home;
 