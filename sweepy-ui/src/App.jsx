import { useState, useEffect } from "react";
import CreateForm from "./components/CreateForm";
import Home from "./components/Home";
import SweepstakeDetail from "./components/SweepstakeDetail";
import ApiClient from "./Api";

const App = () => {
  const [error, setError] = useState(null);
  const [displayHome, setDisplayHome] = useState(true);
  const [displayCreateForm, setDisplayCreateForm] = useState(false);
  const [sweepstake, setSweepstake] = useState(null);
  const [allSweepstakes, setAllSweepstakes] = useState([]);
  const [eventTypes, setEventTypes] = useState([]);

  const apiClient = new ApiClient();

  const fetchAllSweepstakes = () => {
    apiClient
      .getAllSweepstakes()
      .then((data) => {
        setAllSweepstakes(data);
        setError(null);
      })
      .catch((error) => {
        setError("Failed to fetch sweepstakes");
      });
  };

  const fetchEventTypes = () => {
    apiClient
      .getEventTypes()
      .then((data) => {
        setEventTypes(data);
        setError(null);
      })
      .catch((error) => {
        setError("Failed to fetch event types");
      });
  };

  useEffect(() => {
    fetchEventTypes();
    fetchAllSweepstakes();
  }, []);

  const handleCreateApiResponse = (responseData) => {
    setError(null);
    setSweepstake(responseData);
    setDisplayHome(false);
    setDisplayCreateForm(false);
    fetchAllSweepstakes();
  };

  const lookupSweepstake = (id) => {
    apiClient
      .getSweepstake(id)
      .then((data) => {
        setError(null);
        setSweepstake(data);
        setDisplayHome(false);
        setDisplayCreateForm(false);
      })
      .catch((error) => {
        console.error("Error fetching sweepstake:", error);
        setError(`Could not find sweepstake with that ID (${id})`);
      });
  };

  const refreshSweepstake = async (id) => {
    apiClient
      .refreshSweepstake(id)
      .then((data) => {
        setError(null);
        setSweepstake(data);
      })
      .catch((error) => {
        console.error("Error refreshing sweepstake:", error);
        setError(`Failed to refresh sweepstake with ID ${id}`);
      });
  };

  const closeSweepstake = async (id) => {
    apiClient
      .closeSweepstake(id)
      .then(() => {
        setError(null);
        setSweepstake(null);
        fetchAllSweepstakes();
        setDisplayHome(true);
      })
      .catch((error) => {
        console.error("Error closing sweepstake:", error);
        setError(`Failed to close sweepstake with ID ${id}`);
      });
  };

  const getMarkets = (eventType) => {
    return apiClient
      .getMarkets(eventType)
      .then((data) => {
        setError(null);
        return data;
      })
      .catch((error) => {
        console.error("Error fetching markets:", error);
        setError(`Failed to fetch markets for event type ${eventType}`);
        return [];
      });
  };

  const getSweepstakeHistory = (sweepstakeId) => {
    return apiClient
      .getSweepstakeHistory(sweepstakeId)
      .then((data) => {
        setError(null);
        return data;
      })
      .catch((error) => {
        console.error("Error fetching sweepstake history:", error);
        setError(
          `Failed to fetch history for sweepstake with ID ${sweepstakeId}`,
        );
        return [];
      });
  };

  const mainComponent = () => {
    let component;
    if (displayHome) {
      component = (
        <Home
          setDisplayCreateForm={setDisplayCreateForm}
          setDisplayHome={setDisplayHome}
          allSweepstakes={allSweepstakes}
          lookupSweepstake={lookupSweepstake}
        />
      );
    } else if (displayCreateForm) {
      component = (
        <CreateForm
          eventTypes={eventTypes}
          fetchMarkets={getMarkets}
          handleSubmitSuccess={handleCreateApiResponse}
        />
      );
    } else if (sweepstake) {
      component = (
        <SweepstakeDetail
          sweepstake={sweepstake}
          getSweepstakeHistory={getSweepstakeHistory}
          refreshSweepstake={refreshSweepstake}
          closeSweepstake={closeSweepstake}
        />
      );
    }

    return (
      <div>
        {error && <p className="text-red-500">{error}</p>}
        {component}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <button
        className="absolute top-4 left-4 bg-blue-500 text-white px-4 py-2 rounded-lg"
        onClick={() => {
          setDisplayHome(true);
          setDisplayCreateForm(false);
          setSweepstake(null);
        }}
      >
        Home
      </button>
      <div className="mx-auto w-auto bg-white p-6 rounded-2xl shadow-xl">
        {mainComponent()}
      </div>
    </div>
  );
};

export default App;
