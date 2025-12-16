import api from './api';

export const documentosService = {
  getAll: async (page = 1, size = 10) => {
    const response = await api.get('/documentos', {
      params: { page, size }
    });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/documentos/${id}`);
    return response.data;
  },

  getEstadisticas: async () => {
    const response = await api.get('/documentos/estadisticas');
    return response.data;
  },

  create: async (documento) => {
    const response = await api.post('/documentos', documento);
    return response.data;
  },

  update: async (id, documento) => {
    const response = await api.put(`/documentos/${id}`, documento);
    return response.data;
  },

  patch: async (id, documento) => {
    const response = await api.patch(`/documentos/${id}`, documento);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/documentos/${id}`);
    return response.data;
  },
};
