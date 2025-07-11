import SweepstakesList from "./SweepstakesList";

function Home({
  setDisplayHome,
  setDisplayCreateForm,
  allSweepstakes,
  lookupSweepstake,
}) {
  const handleCreateButtonClick = () => () => {
    setDisplayHome(false);
    setDisplayCreateForm(true);
  };

  return (
    <div className="w-auto p-4">
      <button
        type="button"
        onClick={handleCreateButtonClick()}
        className="mb-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
      >
        Create New Sweepstakes
      </button>
      {allSweepstakes.length > 0 ? (
        <SweepstakesList
          sweepstakes={allSweepstakes}
          showSweepstakes={lookupSweepstake}
        />
      ) : (
        <p className="text-gray-500">
          No sweepstakes available. Please create one.
        </p>
      )}
    </div>
  );
}

export default Home;
