import React from 'react';

const SummaryDisplay = ({ summary }) => {
    return summary ? (
        <div>
            <h3>Summary:</h3>
            <p>{summary}</p>
        </div>
    ) : null;
};

export default SummaryDisplay;
