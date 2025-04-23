import React from 'react';
import UploadForm from './subPages/UploadForm';
import Last10Facturas from './subPages/Last10Facturas';

const Facturas = () => {
  return (
    <div className="rebates-page">
      <div className="partners-page">
      <UploadForm endpoint="http://157.245.242.171/api/upload-facturas/" title="Upload Facturas File" />
      <Last10Facturas/>
      </div>
    </div>
  );
};

export default Facturas;
