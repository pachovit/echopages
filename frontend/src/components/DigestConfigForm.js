import React, { useState, useEffect } from 'react';
import { getConfig, setConfig } from '../services/api';
import '../styles/DigestConfigForm.css';

const DigestConfigForm = () => {
    const [numberOfUnits, setNumberOfUnits] = useState(null);
    const [dailyTime, setDailyTime] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const response = await getConfig();
                console.info('Fetched configuration:', response.data);
                setNumberOfUnits(response.data.number_of_units_per_digest);
                setDailyTime(response.data.daily_time_of_digest);
            } catch (error) {
                console.error('Failed to load configuration:', error);
                alert('Failed to load current configuration.');
            } finally {
                setLoading(false);
            }
        };
        fetchConfig();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const config = {
            number_of_units_per_digest: numberOfUnits,
            daily_time_of_digest: dailyTime,
        };

        try {
            await setConfig(config);
            alert('Configuration updated successfully!');
        } catch (error) {
            console.error('Failed to update configuration:', error);
            alert('Failed to update configuration.');
        }
    };

    if (loading) {
        return <div className="loading-indicator">Loading configuration...</div>;
    }

    return (
        <div className="form-container">
            <div className="form-card">
                <h2 className="form-heading">Digest Configuration</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Number of Units per Digest:</label>
                        <input
                            type="number"
                            value={numberOfUnits !== null ? numberOfUnits : ''}
                            onChange={(e) => setNumberOfUnits(Number(e.target.value))}
                            min="1"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Daily Time of Digest:</label>
                        <input
                            type="time"
                            value={dailyTime}
                            onChange={(e) => setDailyTime(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="submit-button" disabled={numberOfUnits === null || dailyTime === ''}>
                        Update Configuration
                    </button>
                </form>
            </div>
        </div>
    );
};

export default DigestConfigForm;