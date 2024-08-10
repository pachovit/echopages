import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import NavBar from '../components/NavBar';
import { getContent } from '../services/api';
import ReactMarkdown from 'react-markdown';
import '../styles/ContentManagementPage.css';

const ContentManagementPage = () => {
    const [content, setContent] = useState([]);
    const [filteredContent, setFilteredContent] = useState([]);
    const [sourceFilter, setSourceFilter] = useState('');
    const [authorFilter, setAuthorFilter] = useState('');
    const [expandedItem, setExpandedItem] = useState(null); // Track which item is expanded

    useEffect(() => {
        const fetchContent = async () => {
            try {
                const response = await getContent();
                const sortedContent = response.data.sort((a, b) => b.id - a.id); // Sort by ID in reverse order
                setContent(sortedContent);
                setFilteredContent(sortedContent);
            } catch (error) {
                console.error('Error fetching content:', error);
                alert('Failed to load content.');
            }
        };

        fetchContent();
    }, []);

    useEffect(() => {
        applyFilters();
    }, [sourceFilter, authorFilter]);

    const applyFilters = () => {
        let filtered = content;

        if (sourceFilter) {
            filtered = filtered.filter(item => item.source.toLowerCase().includes(sourceFilter.toLowerCase()));
        }

        if (authorFilter) {
            filtered = filtered.filter(item => item.author.toLowerCase().includes(authorFilter.toLowerCase()));
        }

        setFilteredContent(filtered);
    };

    const toggleExpand = (index) => {
        setExpandedItem(expandedItem === index ? null : index); // Toggle the expanded item
    };

    const getSampleText = (text) => {
        return text.length > 50 ? `${text.substring(0, 50)}...` : text;
    };

    return (
        <div>
            <NavBar />
            <div className="content-management-container">
                <h2>Content Management</h2>
                <div className="filters">
                    <input
                        type="text"
                        placeholder="Filter by Source"
                        value={sourceFilter}
                        onChange={(e) => setSourceFilter(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Filter by Author"
                        value={authorFilter}
                        onChange={(e) => setAuthorFilter(e.target.value)}
                    />
                    <Link to="/add-content" className="add-content-button">
                        Add New Content
                    </Link>
                </div>
                <div className="content-list">
                    {filteredContent.length > 0 ? (
                        <div className="accordion">
                            {filteredContent.map((item, index) => (
                                <div key={index} className="accordion-item">
                                    <div className="accordion-header" onClick={() => toggleExpand(index)}>
                                        <div className="accordion-header-info">
                                            <strong>
                                                {item.source || '(No source)'} ({item.author || 'No author'}) - {item.location || '(No location)'}
                                            </strong>: 
                                            <em>{getSampleText(item.text)}</em>
                                        </div>
                                        <div className="accordion-toggle">
                                            {expandedItem === index ? '▲' : '▼'}
                                        </div>
                                    </div>
                                    {expandedItem === index && (
                                        <div className="accordion-content">
                                            <ReactMarkdown>{item.text}</ReactMarkdown>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p>No content found.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ContentManagementPage;