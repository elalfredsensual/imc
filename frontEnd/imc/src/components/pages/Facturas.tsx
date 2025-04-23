import React from 'react';
import UploadForm from './subPages/UploadForm';
import Last10Facturas from './subPages/Last10Facturas';

const Facturas = () => {
  return (
    <div className="rebates-page">
      <div className="partners-page">
      <UploadForm endpoint="http://localhost:8000/api/upload-facturas/" title="Upload Partner File" />
      <Last10Facturas/>
      </div>
    </div>
  );
};

export default Facturas;
