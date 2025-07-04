import SweepstakeTable from "./SweepstakeTable";
import SweepstakeHistoryChart from "./SweepstakeHistoryChart";

const SECONDS_IN_MINUTE = 60;
const SECONDS_IN_HOUR = 3600;
const SECONDS_IN_DAY = 86400;

function timeAgo(timestamp) {
  const now = new Date();
  const past = new Date(timestamp);
  const diff = Math.floor((now - past) / 1000);
  let normalizedDiff;
  let unit;

  if (diff < SECONDS_IN_MINUTE) {
    unit = "second";
    normalizedDiff = diff;
  } else if (diff < SECONDS_IN_HOUR) {
    unit = "minute";
    normalizedDiff = Math.floor(diff / SECONDS_IN_MINUTE);
  } else if (diff < SECONDS_IN_DAY) {
    unit = "hour";
    normalizedDiff = Math.floor(diff / SECONDS_IN_HOUR);
  } else {
    unit = "day";
    normalizedDiff = Math.floor(diff / SECONDS_IN_DAY);
  }

  if (normalizedDiff === 1) {
    return `${normalizedDiff} ${unit} ago`;
  } else {
    return `${normalizedDiff} ${unit}s ago`;
  }
}

function SweepstakeDetail({
  sweepstake,
  getSweepstakeHistory,
  refreshSweepstake,
  closeSweepstake,
}) {
  const refreshHandler = () => {
    refreshSweepstake(sweepstake.id);
  };

  const closeHandler = () => {
    if (!window.confirm("Are you sure you want to close this sweepstake?")) {
      return;
    }

    closeSweepstake(sweepstake.id);
  };

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">
        {sweepstake.name} (ID: {sweepstake.id})
      </h2>
      <p className="text-gray-600 mb-4">
        Competition: {sweepstake.competition} | Participants:{" "}
        {sweepstake.participants.length}
      </p>
      <button
        type="button"
        onClick={refreshHandler}
        className="mb-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        title="Refresh"
      >
        Refresh
      </button>
      <button
        type="button"
        onClick={closeHandler}
        className="mb-4 ml-2 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
        title="Close"
      >
        Close
      </button>
      <p className="text-gray-600 mb-4">
        Last refresh: {timeAgo(sweepstake.updated_at)}
      </p>
      <SweepstakeTable data={sweepstake} />
      <SweepstakeHistoryChart
        sweepstakeId={sweepstake.id}
        getSweepstakeHistory={getSweepstakeHistory}
      />
    </div>
  );
}

export default SweepstakeDetail;
