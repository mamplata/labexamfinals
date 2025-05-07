import axios from 'axios';
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: { 'Content-Type': 'application/json' }
});
export const fetchUsers = () => api.get('/users/');
export const fetchBooks = () => api.get('/books/');
export const createBook = (data) => api.post('/books/', data);
export const updateBook = (id, data) => api.put(`/books/${id}/`, data);
export const deleteBook = (id) => api.delete(`/books/${id}/`);
export const fetchTransactions = () => api.get('/transactions/');
export const borrowBook = (data) => api.post('/borrow/', data);
export const returnBook = (id, data) => api.post(`/return/${id}/`, data);