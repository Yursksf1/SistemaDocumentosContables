import React, { useState, useEffect } from 'react';
import { empresasService } from '../services/empresas';

const Empresas = () => {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadEmpresas();
  }, []);

  const loadEmpresas = async () => {
    try {
      setLoading(true);
      const data = await empresasService.getAll();
      setEmpresas(data.items || []);
      setError(null);
    } catch (err) {
      setError('Error al cargar las empresas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-xl text-gray-600">Cargando...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Empresas</h1>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {empresas.map((empresa) => (
          <div key={empresa.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div className="mb-2">
              <span className="text-sm text-gray-500">ID:</span>
              <span className="ml-2 font-semibold">{empresa.id}</span>
            </div>
            <div className="mb-2">
              <span className="text-sm text-gray-500">Identificación:</span>
              <span className="ml-2 font-semibold">{empresa.identificacion}</span>
            </div>
            <div>
              <span className="text-sm text-gray-500">Razón Social:</span>
              <p className="mt-1 text-lg font-bold text-gray-800">{empresa.razon_social}</p>
            </div>
          </div>
        ))}
      </div>

      {empresas.length === 0 && !error && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No hay empresas registradas</p>
        </div>
      )}
    </div>
  );
};

export default Empresas;
