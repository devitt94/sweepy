import React, { useState } from "react";

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

function Table({ data, refreshSweepstake, closeSweepstake }) {
  const [expandedRow, setExpandedRow] = useState(null); // Track expanded row

  const toggleRow = (index) => {
    setExpandedRow(expandedRow === index ? null : index);
  };

  const refreshHandler = () => {
    refreshSweepstake(data.id);
  };

  const closeHandler = () => {
    if (!window.confirm("Are you sure you want to close this sweepstake?")) {
      return;
    }

    closeSweepstake(data.id);
  };

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">
        {data.name} (ID: {data.id})
      </h2>
      <p className="text-gray-600 mb-4">
        Competition: {data.competition} | Participants:{" "}
        {data.participants.length}
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
        Last refresh: {timeAgo(data.updated_at)}
      </p>
      <div className="overflow-x-auto">
        <table className="min-w-full border rounded-lg">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">Name</th>
              <th className="px-4 py-2 text-left">Equity</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.participants.map((p, index) => (
              <React.Fragment key={index}>
                <tr className="cursor-pointer" onClick={() => toggleRow(index)}>
                  <td className="px-4 py-2">{p.name}</td>
                  <td className="px-4 py-2">
                    {(parseFloat(p.equity) * 100).toFixed(2)}%
                  </td>
                </tr>

                {/* Accordion for the expanded row */}
                {expandedRow === index && (
                  <tr>
                    <td colSpan="2" className="px-4 py-2 bg-gray-100">
                      <table className="w-full">
                        <thead>
                          <tr>
                            <th className="px-4 py-2 text-left">Runner</th>
                            <th className="px-4 py-2 text-left">Probability</th>
                          </tr>
                        </thead>
                        <tbody>
                          {p.assignments.map((assignment, idx) => (
                            <tr key={idx}>
                              <td className="px-4 py-2">{assignment.name}</td>
                              <td className="px-4 py-2">
                                {parseFloat(
                                  assignment.implied_probability * 100,
                                ).toFixed(2)}
                                %
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Table;
