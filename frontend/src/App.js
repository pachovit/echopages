import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AddContentPage from './pages/AddContentPage';
import ConfigPage from './pages/ConfigPage';
import ContentManagementPage from './pages/ContentManagementPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/add-content" element={<AddContentPage />} />
                <Route path="/config" element={<ConfigPage />} />
                <Route path="/content-management" element={<ContentManagementPage />} />
            </Routes>
        </Router>
    );
};

export default App;