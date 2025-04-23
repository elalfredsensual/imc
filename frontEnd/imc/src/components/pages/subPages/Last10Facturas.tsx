// Last10Facturas.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './Last10Quotes.css'; // Puedes seguir reutilizando el CSS

interface Factura {
  Date: string;
  Num: string;
  Partner: string;
  Pais: string;
  Territory: string;
  Memo_Description: string;
  Amount: number;
  INVOICE_TYPE: string;
}

const Last10Facturas: React.FC = () => {
  const [facturas, setFacturas] = useState<Factura[]>([]);

  useEffect(() => {
    const fetchFacturas = async () => {
      try {
        const response = await axios.get<Factura[]>('http://157.245.242.171/api/get-last-10-facturas/');
        setFacturas(response.data);
      } catch (err) {
        toast.error('Error al obtener las facturas.');
      }
    };

    fetchFacturas();
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  return (
    <div className="last-10-quotes">
      <ToastContainer />
      <h3 className="text-center my-4">Últimas 10 Facturas</h3>
      <Table className="pretty-table" striped bordered hover responsive>
        <thead>
          <tr>
            <th>Date</th>
            <th>Num</th>
            <th>Partner</th>
            <th>Pais</th>
            <th>Territory</th>
            <th>Memo</th>
            <th>Amount</th>
            <th>Invoice Type</th>
          </tr>
        </thead>
        <tbody>
          {facturas.map((factura, index) => (
            <tr key={index}>
              <td>{factura.Date}</td>
              <td>{factura.Num}</td>
              <td>{factura.Partner}</td>
              <td>{factura.Pais}</td>
              <td>{factura.Territory}</td>
              <td>{factura.Memo_Description}</td>
              <td>{formatCurrency(factura.Amount)}</td>
              <td>{factura.INVOICE_TYPE}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Last10Facturas;
