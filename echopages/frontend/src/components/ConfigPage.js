import React from 'react';
import NavBar from '../components/NavBar';
import DigestConfigForm from '../components/DigestConfigForm';

const ConfigPage = () => {
    return (
        <div>
            <NavBar />
            <div className="page-content">
                <h1>Digest Configuration</h1>
                <DigestConfigForm />
            </div>
        </div>
    );
};

export default ConfigPage;