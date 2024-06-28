import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './Last10Quotes.css'; // Reuse the same CSS file for consistency

interface Partner {
  IMC_PO: string;
  PARTNER_PO: string;
  MONTO_PARTNER_PO: number;
}

const Last10Partners = () => {
  const [partners, setPartners] = useState<Partner[]>([]);

  useEffect(() => {
    const fetchPartners = async () => {
      try {
        const response = await axios.get<Partner[]>('http://localhost:8000/api/get-last-10-partners/');
        setPartners(response.data);
      } catch (err) {
        toast.error('Failed to fetch partners');
      }
    };

    fetchPartners();
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
      <h3 className="text-center my-4">Last 10 Partner Records</h3>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>IMC PO</th>
            <th>Partner PO</th>
            <th>Monto Partner PO</th>
          </tr>
        </thead>
        <tbody>
          {partners.map((partner, index) => (
            <tr key={index}>
              <td>{partner.IMC_PO}</td>
              <td>{partner.PARTNER_PO}</td>
              <td>{formatCurrency(partner.MONTO_PARTNER_PO)}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Last10Partners;
