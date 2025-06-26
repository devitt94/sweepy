
import React, { useState } from 'react';

function timeAgo(timestamp) {
  const now = new Date();
  const past = new Date(timestamp);
  const diff = Math.floor((now - past) / 1000);

  if (diff < 60) return `${diff} seconds ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
  if (diff < 2592000) return `${Math.floor(diff / 86400)} days ago`;

  // You can customize this further
  return past.toLocaleDateString(); // Fallback: display the date
}


function Table({data, refreshSweepstake, closeSweepstake}) {
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
            <h2 className="text-lg font-semibold mb-2">{data.name} (ID: {data.id})</h2>
             <button
                type="button"
                onClick={refreshHandler}
                className="mb-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
                title="Refresh"
            >Refresh</button>
            <button
                type="button"
                onClick={closeHandler}
                className="mb-4 ml-2 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
                title="Close"
            >Close</button>
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
                    <tr
                        className="cursor-pointer"
                        onClick={() => toggleRow(index)}
                    >
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
                                    {parseFloat(assignment.implied_probability*100).toFixed(2)}%
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
