import SweepstakesList from "./SweepstakesList";

function Home({ setDisplayHome, setDisplayCreateForm, allSweepstakes, lookupSweepstake }) {

    const handleCreateButtonClick = () => () => {
        setDisplayHome(false);
        setDisplayCreateForm(true);
    };
    
  return (
    <div className="container mx-auto p-4">
      <button 
        type="button" 
        onClick={handleCreateButtonClick()} 
        className="mb-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
      >
        Create New Sweepstakes
      </button>
      <SweepstakesList sweepstakes={allSweepstakes} showSweepstakes={lookupSweepstake}/>
    </div>
  );
}

export default Home;