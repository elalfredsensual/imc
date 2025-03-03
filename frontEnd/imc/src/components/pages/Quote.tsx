import React from 'react';
import UploadForm from './subPages/UploadForm';
import Last10Quotes from './subPages/Last10Quotes';

const Quote = () => {
  return (
    <div className="quote-page">
      <UploadForm endpoint="http://157.245.242.171/api/upload-quote/" title="Upload Quote File" />
      <Last10Quotes />
    </div>
  );
};

export default Quote;
