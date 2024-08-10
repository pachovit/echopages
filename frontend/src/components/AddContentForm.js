import React, { useState } from 'react';
import { addContent } from '../services/api';
import '../styles/AddContentForm.css';

const AddContentForm = () => {
    const [source, setSource] = useState('');
    const [author, setAuthor] = useState('');
    const [location, setLocation] = useState('');
    const [text, setText] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Ensure text is filled out
        if (!text.trim()) {
            alert('Text field is required.');
            return; // Stop form submission if text is empty
        }

        // Prepare the data with empty strings for optional fields
        const data = {
            source: source.trim(),
            author: author.trim(),
            location: location.trim(),
            text: text.trim(),
        };

        try {
            await addContent(data);
            alert('Content added successfully!');
            // Reset form fields after successful submission
            setSource(''); setAuthor(''); setLocation(''); setText('');
        } catch (error) {
            alert('Failed to add content.');
        }
    };

    return (
        <div className="form-container">
            <div className="form-card">
                <h2 className="form-heading">Add New Content</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Source:</label>
                        <input
                            value={source}
                            onChange={(e) => setSource(e.target.value)}
                            placeholder="Enter the source (e.g., Book Name)"
                        />
                    </div>
                    <div className="form-group">
                        <label>Author:</label>
                        <input
                            value={author}
                            onChange={(e) => setAuthor(e.target.value)}
                            placeholder="Enter the author name"
                        />
                    </div>
                    <div className="form-group">
                        <label>Location:</label>
                        <input
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            placeholder="Enter the location (e.g., Chapter 1)"
                        />
                    </div>
                    <div className="form-group">
                        <label>Text: <span className="required">*</span></label>
                        <textarea
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Enter the content text"
                            required
                        />
                    </div>
                    <button type="submit" className="submit-button">
                        Add Content
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AddContentForm;