import axios from 'axios';
export const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
export const api = axios.create({baseURL:API, timeout:30000});
export const amount = n => new Intl.NumberFormat('en-US',{maximumFractionDigits:2}).format(n);
export const compact = n => new Intl.NumberFormat('en-US',{notation:'compact',maximumFractionDigits:1}).format(n);
export const errorText = e => typeof e.response?.data?.detail === 'string' ? e.response.data.detail : 'Something went wrong. Please try again.';