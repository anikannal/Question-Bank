import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
});

export const getTasks = async (skip = 0, limit = 100) => {
    const response = await api.get(`/tasks/?skip=${skip}&limit=${limit}`);
    return response.data;
};

export const createTask = async (userId, task) => {
    const response = await api.post(`/users/${userId}/tasks/`, task);
    return response.data;
};

export const updateTask = async (taskId, task) => {
    const response = await api.put(`/tasks/${taskId}`, task);
    return response.data;
};

export const getUsers = async () => {
    const response = await api.get('/users/');
    return response.data;
}

export const createUser = async (user) => {
    const response = await api.post('/users/', user);
    return response.data;
}
