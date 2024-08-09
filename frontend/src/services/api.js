import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Replace with your backend URL

export const addContent = async (data) => {
    return axios.post(`${API_BASE_URL}/add_content`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  };

export const getConfig = () => {
    return axios.get(`${API_BASE_URL}/get_config`);
};

export const setConfig = (config) => {
    return axios.post(`${API_BASE_URL}/set_config`, config, {
        headers: {
            'Content-Type': 'application/json',
        },
    });
};