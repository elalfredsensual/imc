import React from 'react';
import GetRebates from './subPages/GetRebates';
import RebatesForm from './subPages/RebatesForm';

const Rebates = () => {
  return (
    <div className="rebates-page">
      <h2>Rebates Management</h2>
      <RebatesForm />
      <hr />
      <GetRebates />
    </div>
  );
};

export default Rebates;
