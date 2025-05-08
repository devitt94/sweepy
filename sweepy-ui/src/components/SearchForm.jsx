import React, { useState } from 'react';

function SearchForm({lookupSweepstake}) {

  const [searchTerm, setSearchTerm] = useState('');

  const onSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm) {
      try {
        lookupSweepstake(searchTerm);
      } catch (error) {
        console.error('Error looking up sweepstake:', error);
      }
    }
  };
  
  return (
    <form className="search-form" onSubmit={onSearchSubmit}>
      <input
        type="text"
        placeholder="Sweepstake ID"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
    </form>
  );
}

export default SearchForm;