import React, { useState } from 'react';
import CreateForm from './components/CreateForm';
import SearchForm from './components/SearchForm';
import Table from './components/Table';
import Menu from './components/Menu';

const App = () => {
  const [error, setError] = useState(null);
  const [displayMenu, setDisplayMenu] = useState(true);
  const [displaySearchForm, setDisplaySearchForm] = useState(false);
  const [displayCreateForm, setDisplayCreateForm] = useState(false);
  const [sweepstake, setSweepstake] = useState(null);

  const handleApiResponse = (responseData) => {
    setError(null);
    setSweepstake(responseData);
    setDisplayMenu(false);
    setDisplayCreateForm(false);
    setDisplaySearchForm(false);
  };

  const lookupSweepstake = (id) => {
    fetch(`/api/sweepstakes/${id}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setError(null);
        setSweepstake(data);
        setDisplayMenu(false);
        setDisplayCreateForm(false);
        setDisplaySearchForm(false);
      })
      .catch((error) => {
        console.error('Error fetching sweepstake:', error);
        setError(`Could not find sweepstake with that ID (${id})`);
      });
  }

  const mainComponent = () => {
    let component;
    if (displayMenu) {
      console.log("Rendering Menu");
      component = <Menu setDisplayCreateForm={setDisplayCreateForm} setDisplayMenu={setDisplayMenu} setDisplaySearchForm={setDisplaySearchForm}/>;
    } else if (displayCreateForm) {
      console.log("Rendering Create Form");
      component = <CreateForm handleSubmitSuccess={handleApiResponse} />;
    } else if (displaySearchForm) {
      console.log("Rendering Search Form");
      component = <SearchForm lookupSweepstake={lookupSweepstake}/>;
    } else if (sweepstake) {
      console.log("Rendering Table");
      component = <Table data={sweepstake} />;
    }

    return (
      <div>
        {error && <p className="text-red-500">{error}</p>}
        {component}
      </div>
    );
  }

  return (
    
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <button
        className="absolute top-4 left-4 bg-blue-500 text-white px-4 py-2 rounded-lg"
        onClick={() => {
          setDisplayMenu(true);
          setDisplayCreateForm(false);
          setDisplaySearchForm(false);
          setSweepstake(null);
        }}
      >
        Home
      </button>
      <div className="w-full max-w-xl bg-white p-6 rounded-2xl shadow-xl">
        {mainComponent()}
      </div>
    </div>
  );
};

export default App;