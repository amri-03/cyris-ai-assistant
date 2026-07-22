import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

// Preserved 6 core API call methods
export const chat = (payload) => api.post("/chat", payload);
export const getSessions = () => api.get("/sessions");
export const getSessionMessages = (id) => api.get(`/sessions/${id}/messages`);
export const deleteSession = (id) => api.delete(`/sessions/${id}`);
export const getMemoryStatus = () => api.get("/memory-status");
export const deleteMemory = (identity) => api.delete(`/memory/${identity}`);

export default api;