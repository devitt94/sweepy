import { useState, useEffect } from "react";
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
  const [loading, setLoading] = useState(true);
  const [sweepstakeHistory, setSweepstakeHistory] = useState([]);

  const refreshData = async () => {
    setLoading(true);
    try {
      await refreshSweepstake(sweepstake.id);
    } catch (error) {
      console.error("Error refreshing sweepstake:", error);
    }

    try {
      const history = await getSweepstakeHistory(sweepstake.id);
      setSweepstakeHistory(history);
    } catch (error) {
      console.error("Error fetching sweepstake history:", error);
    }

    setLoading(false);
  };

  useEffect(() => {
    refreshData();
  }, []);

  const closeHandler = () => {
    if (!window.confirm("Are you sure you want to close this sweepstake?")) {
      return;
    }

    closeSweepstake(sweepstake.id);
  };

  if (loading) {
    return (
      <div className="mt-6">
        <p className="text-gray-600">Loading sweepstake details...</p>
      </div>
    );
  }

  if (!sweepstakeHistory) {
    return (
      <div className="mt-6">
        <p className="text-red-600">
          Error loading sweepstake details. Please try again later.
        </p>
      </div>
    );
  }

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
        onClick={refreshData}
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
      <SweepstakeHistoryChart sweepstakeHistory={sweepstakeHistory} />
    </div>
  );
}

export default SweepstakeDetail;
