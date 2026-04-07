import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const getStoredToken = () => localStorage.getItem("chaitra_token");
export const getStoredUser = () => {
  const raw = localStorage.getItem("chaitra_user");
  return raw ? JSON.parse(raw) : null;
};
export const setAuthSession = (token: string, user: any) => {
  localStorage.setItem("chaitra_token", token);
  localStorage.setItem("chaitra_user", JSON.stringify(user));
};
export const clearAuthSession = () => {
  localStorage.removeItem("chaitra_token");
  localStorage.removeItem("chaitra_user");
};

API.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const sendQuery = async (query: string) => {
  const currentUser = getStoredUser();
  const { data } = await API.post("/query", {
    query,
    user_id: currentUser?.id || "default_user",
    fast_mode: true,
  });
  return data;
};

export const getDashboard = async () => {
  const { data } = await API.get("/dashboard/");
  return data;
};

export const getPredictions = async () => {
  const { data } = await API.get("/predictions/");
  return data;
};

export const getInsights = async () => {
  const { data } = await API.get("/insights/");
  return data;
};

export const getChats = async (userId = "default_user") => {
  const { data } = await API.get(`/chats/${userId}`);
  return data;
};

export const signup = async (payload: { email: string; password: string; full_name?: string; company?: string }) => {
  const { data } = await API.post("/auth/signup", payload);
  return data;
};

export const login = async (payload: { email: string; password: string }) => {
  const { data } = await API.post("/auth/login", payload);
  return data;
};

export const me = async () => {
  const { data } = await API.get("/auth/me");
  return data;
};

export const updateProfile = async (payload: { full_name: string; company: string; role: string }) => {
  const { data } = await API.put("/auth/profile", payload);
  return data;
};

export const getSettings = async () => {
  const { data } = await API.get("/auth/settings");
  return data;
};

export const updateSettings = async (payload: {
  theme: string;
  voice_enabled: boolean;
  chat_mode: string;
  retention: string;
}) => {
  const { data } = await API.put("/auth/settings", payload);
  return data;
};