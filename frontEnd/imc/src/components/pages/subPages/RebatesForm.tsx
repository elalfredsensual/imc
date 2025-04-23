import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Form, Button } from 'react-bootstrap';
import { toast } from 'react-toastify';
// RebatesForm.tsx
import './PrettyForm.css';


interface Rebate {
  fiscal_year: string;
  quarter: string;
  amount: number;
}

const quarters = ['Q1', 'Q2', 'Q3', 'Q4'];

const RebatesForm: React.FC = () => {
  const [rebates, setRebates] = useState<Rebate[]>([]);
  const [selectedYear, setSelectedYear] = useState('FY25');
  const [selectedQuarter, setSelectedQuarter] = useState('Q1');
  const [amount, setAmount] = useState<number | ''>('');
  const [existingRebate, setExistingRebate] = useState<Rebate | null>(null);

  // Cargar rebates existentes al inicio
  useEffect(() => {
    const fetchRebates = async () => {
      try {
        const response = await axios.get<Rebate[]>('http://localhost:8000/api/rebates/');
        setRebates(response.data);
      } catch (err) {
        toast.error('Failed to fetch existing rebates');
      }
    };

    fetchRebates();
  }, []);

  // Cuando cambian el año o trimestre, buscar si existe ese rebate
  useEffect(() => {
    const existing = rebates.find(r => r.fiscal_year === selectedYear && r.quarter === selectedQuarter);
    if (existing) {
      setAmount(existing.amount);
      setExistingRebate(existing);
    } else {
      setAmount('');
      setExistingRebate(null);
    }
  }, [selectedYear, selectedQuarter, rebates]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const fiscalYearRegex = /^FY\d{2}$/;

    if (!fiscalYearRegex.test(selectedYear)) {
      toast.error('Fiscal year must follow format FYXX, e.g., FY25');
      return;
    }

    if (amount === '') {
      toast.error('Amount cannot be empty');
      return;
    }

    try {
      await axios.post('http://localhost:8000/api/rebates/update/', {
        fiscal_year: selectedYear,
        quarter: selectedQuarter,
        amount,
      });

      toast.success('Rebate saved successfully');

      const updated = [...rebates.filter(r => !(r.fiscal_year === selectedYear && r.quarter === selectedQuarter)), {
        fiscal_year: selectedYear,
        quarter: selectedQuarter,
        amount: Number(amount)
      }];
      setRebates(updated);
      setExistingRebate({
        fiscal_year: selectedYear,
        quarter: selectedQuarter,
        amount: Number(amount)
      });

    } catch (error) {
      toast.error('Failed to save rebate');
    }
  };

  const handleDelete = async () => {
    try {
      await axios.post('http://localhost:8000/api/rebates/delete/', {
        fiscal_year: selectedYear,
        quarter: selectedQuarter
      });

      toast.success('Rebate deleted');

      setRebates(prev => prev.filter(r => !(r.fiscal_year === selectedYear && r.quarter === selectedQuarter)));
      setAmount('');
      setExistingRebate(null);

    } catch (error) {
      toast.error('Failed to delete rebate');
    }
  };

  return (
    <div>
      <h4 className="my-4">Insert or Update Rebate</h4>
      <Form onSubmit={handleSubmit} className="pretty-form">
  <h4>Insert or Update Rebate</h4>

  <div className="form-group" style={{ display: 'flex', gap: '1rem' }}>
  <div style={{ flex: 1 }}>
    <Form.Label>Fiscal Year</Form.Label>
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <span>FY</span>
      <Form.Control
        type="text"
        value={selectedYear.slice(2)}
        onChange={e => {
          const value = e.target.value.replace(/\D/g, '').slice(0, 2);
          setSelectedYear(`FY${value}`);
        }}
        placeholder="e.g., 26"
        maxLength={2}
      />
    </div>
  </div>

  <div style={{ flex: 1 }}>
    <Form.Label>Quarter</Form.Label>
    <Form.Select value={selectedQuarter} onChange={e => setSelectedQuarter(e.target.value)}>
      {['Q1', 'Q2', 'Q3', 'Q4'].map(q => (
        <option key={q} value={q}>{q}</option>
      ))}
    </Form.Select>
  </div>
</div>


    <Form.Group className="form-group">
    <Form.Label>Amount</Form.Label>
    <Form.Control
        type="text"
        inputMode="decimal"
        value={
        amount !== ''
            ? new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            }).format(Number(amount))
            : ''
        }
        onChange={(e) => {
        const raw = e.target.value.replace(/[^0-9.]/g, '');
        setAmount(raw === '' ? '' : Number(raw));
        }}
        placeholder="$0.00"
    />
    </Form.Group>


  <div className="form-actions">
    <Button type="submit">Save</Button>
    {existingRebate && <Button type="button" onClick={handleDelete}>Delete</Button>}
  </div>
</Form>

    </div>
  );
};

export default RebatesForm;
