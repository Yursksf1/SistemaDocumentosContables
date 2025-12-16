import api from './api';

export const empresasService = {
  getAll: async () => {
    const response = await api.get('/empresas');
    return response.data;
  },
};
