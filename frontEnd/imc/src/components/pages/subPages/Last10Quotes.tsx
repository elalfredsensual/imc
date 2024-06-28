import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './Last10Quotes.css'; // Import custom CSS for styling

interface Quote {
  Date: string;
  Num: string;
  Partner: string;
  Pais: string;
  Territory: string;
  Memo_Description: string;
  Amount: number;
  Product_Family: string;
  Order_Type: string;
}

const Last10Quotes: React.FC = () => {
  const [quotes, setQuotes] = useState<Quote[]>([]);

  useEffect(() => {
    const fetchQuotes = async () => {
      try {
        const response = await axios.get<Quote[]>('http://localhost:8000/api/get-last-10-quotes/');
        setQuotes(response.data);
      } catch (err) {
        toast.error('Failed to fetch quotes');
      }
    };

    fetchQuotes();
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  return (
    <div className="mt-4">
      <ToastContainer />
      <h3 className="text-center">Last 10 Quotes</h3>
      <Table striped bordered hover className="pretty-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Num</th>
            <th>Partner</th>
            <th>Pais</th>
            <th>Territory</th>
            <th>Memo Description</th>
            <th>Amount</th>
            <th>Product Family</th>
            <th>Order Type</th>
          </tr>
        </thead>
        <tbody>
          {quotes.map((quote, index) => (
            <tr key={index}>
              <td>{quote.Date}</td>
              <td>{quote.Num}</td>
              <td>{quote.Partner}</td>
              <td>{quote.Pais}</td>
              <td>{quote.Territory}</td>
              <td>{quote.Memo_Description}</td>
              <td>{formatCurrency(quote.Amount)}</td>
              <td>{quote.Product_Family}</td>
              <td>{quote.Order_Type}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Last10Quotes;
