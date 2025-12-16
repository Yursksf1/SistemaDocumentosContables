import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="text-xl font-bold">
                Sistema de Documentos Contables
              </Link>
            </div>
            <div className="flex space-x-4">
              <Link
                to="/"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/')
                    ? 'bg-blue-700'
                    : 'hover:bg-blue-500'
                }`}
              >
                Dashboard
              </Link>
              <Link
                to="/documentos"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/documentos')
                    ? 'bg-blue-700'
                    : 'hover:bg-blue-500'
                }`}
              >
                Documentos
              </Link>
              <Link
                to="/empresas"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  isActive('/empresas')
                    ? 'bg-blue-700'
                    : 'hover:bg-blue-500'
                }`}
              >
                Empresas
              </Link>
            </div>
          </div>
        </div>
      </nav>
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;
