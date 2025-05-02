import React, { useState } from 'react';
import CreateForm from './components/CreateForm';
import Table from './components/Table';
import Menu from './components/Menu';

const App = () => {
  const [displayMenu, setDisplayMenu] = useState(true);
  const [displaySearchForm, setDisplaySearchForm] = useState(false);
  const [displayCreateForm, setDisplayCreateForm] = useState(false);
  const [sweepstake, setSweepstake] = useState(null);

  const handleApiResponse = (responseData) => {
    setSweepstake(responseData);
    setDisplayMenu(false);
    setDisplayCreateForm(false);
    setDisplaySearchForm(false);
  };

  const mainComponent = () => {
    if (displayMenu) {
      console.log("Rendering Menu");
      return <Menu setDisplayCreateForm={setDisplayCreateForm} setDisplayMenu={setDisplayMenu} setDisplaySearchForm={setDisplaySearchForm}/>;
    } else if (displayCreateForm) {
      console.log("Rendering Create Form");
      return <CreateForm handleSubmitSuccess={handleApiResponse} />;
    } else if (displaySearchForm) {
      console.log("Rendering Search Form");
      return <p>Not implemented yet!</p>
    } else if (sweepstake) {
      console.log("Rendering Table");
      return <Table data={sweepstake} />;
    }
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