import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Documentos from './pages/Documentos';
import Empresas from './pages/Empresas';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/documentos" element={<Documentos />} />
        <Route path="/empresas" element={<Empresas />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}

export default App;
