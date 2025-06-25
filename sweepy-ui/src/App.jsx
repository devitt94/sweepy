import { useState, useEffect } from 'react';
import CreateForm from './components/CreateForm';
import SweepstakesList from './components/SweepstakesList';
import Table from './components/Table';
import Menu from './components/Menu';
import ApiClient from './Api';

const App = () => {
  const [error, setError] = useState(null);
  const [displayMenu, setDisplayMenu] = useState(true);
  const [displaySearchForm, setDisplaySearchForm] = useState(false);
  const [displayCreateForm, setDisplayCreateForm] = useState(false);
  const [sweepstake, setSweepstake] = useState(null);
  const [allSweepstakes, setAllSweepstakes] = useState([]);

  const apiClient = new ApiClient();

  const fetchAllSweepstakes = () => {
    apiClient.getAllSweepstakes().then((data) => {
        setAllSweepstakes(data);
        setError(null);
      })
      .catch((error) => {
        setError('Failed to fetch sweepstakes');
      });
  };

  useEffect(() => {
    fetchAllSweepstakes();
  }, []);

  const handleCreateApiResponse = (responseData) => {
    setError(null);
    setSweepstake(responseData);
    setDisplayMenu(false);
    setDisplayCreateForm(false);
    setDisplaySearchForm(false);
    fetchAllSweepstakes();
  };

  const lookupSweepstake = (id) => {
    apiClient.getSweepstake(id)
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

    const refreshSweepstake = async (id) => {
        apiClient.refreshSweepstake(id)
          .then((data) => {
            setError(null);
            setSweepstake(data);
          })
          .catch((error) => {
            console.error('Error refreshing sweepstake:', error);
            setError(`Failed to refresh sweepstake with ID ${id}`);
          }); 
    };

    const closeSweepstake = async (id) => {
        apiClient.closeSweepstake(id)
          .then(() => {
            setError(null);
            setSweepstake(null);
            fetchAllSweepstakes();
            setDisplayMenu(true);
          })
          .catch((error) => {
            console.error('Error closing sweepstake:', error);
            setError(`Failed to close sweepstake with ID ${id}`);
          });
    };
    

  const mainComponent = () => {
    let component;
    if (displayMenu) {
      component = <Menu setDisplayCreateForm={setDisplayCreateForm} setDisplayMenu={setDisplayMenu} setDisplaySearchForm={setDisplaySearchForm}/>;
    } else if (displayCreateForm) {
      component = <CreateForm handleSubmitSuccess={handleCreateApiResponse} />;
    } else if (sweepstake) {
      component = <Table data={sweepstake} refreshSweepstake={refreshSweepstake} closeSweepstake={closeSweepstake}/>;
    } else if (displaySearchForm) {
      component = <SweepstakesList sweepstakes={allSweepstakes} showSweepstakes={lookupSweepstake}/>;
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