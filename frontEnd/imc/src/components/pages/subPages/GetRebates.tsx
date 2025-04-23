import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './Last10Quotes.css'; // Reutilizamos el mismo CSS para mantener estilo

interface Rebate {
  fiscal_year: string;
  quarter: string;
  amount: number;
}

const GetRebates = () => {
  const [rebates, setRebates] = useState<Rebate[]>([]);

  useEffect(() => {
    const fetchRebates = async () => {
      try {
        const response = await axios.get<Rebate[]>('http://157.245.242.171/api/rebates/');
        setRebates(response.data);
      } catch (err) {
        toast.error('Failed to fetch rebates');
      }
    };


    fetchRebates();
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  return (
    <div className="last-10-quotes">
      <ToastContainer />
      <h3 className="text-center my-4">Current Rebates</h3>
      <Table className="pretty-table">
        <thead>
          <tr>
            <th>Fiscal Year</th>
            <th>Quarter</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {rebates.map((rebate, index) => (
            <tr key={index}>
              <td>{rebate.fiscal_year}</td>
              <td>{rebate.quarter}</td>
              <td>{formatCurrency(rebate.amount)}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default GetRebates;
