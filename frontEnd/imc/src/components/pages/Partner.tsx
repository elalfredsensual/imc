import React from 'react';
import UploadForm from './subPages/UploadForm';
import Last10Partners from './subPages/Last10Partners';

const Partners = () => {
  return (
    <div className="partners-page">
      <UploadForm endpoint="http://localhost:8000/api/upload-partner/" title="Upload Partner File" />
      <Last10Partners />
    </div>
  );
};

export default Partners;
