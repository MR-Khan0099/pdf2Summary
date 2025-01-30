// import React, { useState } from 'react';
// import axios from 'axios';

// const FileUploadComponent = () => {
//     const [file, setFile] = useState(null);
//     const [loading, setLoading] = useState(false);
//     const [downloadLink, setDownloadLink] = useState("");

//     const handleFileChange = (e) => {
//         setFile(e.target.files[0]);
//     };

//     const handleSubmit = async () => {
//         const formData = new FormData();
//         formData.append('file', file);

//         setLoading(true);
//         try {
//             const response = await axios.post("http://127.0.0.1:8000/upload", formData, {
//                 headers: {
//                     'Content-Type': 'multipart/form-data',
//                 },
//                 responseType: 'blob',  // To handle binary data (PDF)
//             });

//             // Create a link to download the PDF
//             const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
//             const pdfUrl = URL.createObjectURL(pdfBlob);
//             setDownloadLink(pdfUrl);
//         } catch (error) {
//             console.error("Error uploading file:", error);
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div>
//             <input type="file" onChange={handleFileChange} />
//             <button onClick={handleSubmit} disabled={loading}>
//                 {loading ? 'Processing...' : 'Upload'}
//             </button>
            
//             {downloadLink && (
//                 <div>
//                     <a href={downloadLink} download="summary.pdf">Download Summary PDF</a>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default FileUploadComponent;

import React, { useState } from 'react';
import axios from 'axios';

const FileUploadComponent = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState("");
    const [filename, setFilename] = useState("");

    // Handle file input change
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    // Handle file upload and summary generation
    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        try {
            // Send the file to the backend to get the summary
            const response = await axios.post("http://127.0.0.1:8000/upload", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            // Set the summary text to display
            setSummary(response.data.summary);

            // Store the original filename for PDF generation
            setFilename(response.data.filename);
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            setLoading(false);
        }
    };

    // Handle PDF download
    const handleDownload = async () => {
        if (!summary) return;

        try {
            // Send the summary to the backend for PDF generation
            const response = await axios.post("http://127.0.0.1:8000/download_pdf", {
                summary: summary,
                filename: filename,
            }, {
                responseType: 'blob', // Get the PDF as a Blob
            });

            // Create a link to download the PDF
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${filename.replace('.pdf', '')}_summary.pdf`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (error) {
            console.error("Error downloading PDF:", error);
        }
    };

    return (
        <div>
            <h2>Upload PDF for Summary</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleSubmit} disabled={loading}>
                {loading ? 'Processing...' : 'Upload'}
            </button>
            
            {/* Display the summary */}
            {summary && (
                <div>
                    <h3>Summary</h3>
                    <p>{summary}</p>
                </div>
            )}

            {/* Download button */}
            {summary && (
                <div>
                    <button onClick={handleDownload}>Download PDF</button>
                </div>
            )}
        </div>
    );
};

export default FileUploadComponent;
