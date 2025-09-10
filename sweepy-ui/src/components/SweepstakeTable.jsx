import React, { useState } from "react";

function SweepstakeTable({ data }) {
  const [expandedRow, setExpandedRow] = useState(null); // Track expanded row

  const toggleRow = (index) => {
    setExpandedRow(expandedRow === index ? null : index);
  };

  const stringifyScore = (score) => {
    if (score === null || score === undefined) {
      return "-";
    } else if (score == 0) {
      return "E";
    } else if (score > 0) {
      return `+${score}`;
    } else {
      return `${score}`;
    }
  };

  const sortedParticipants = [...data.participants].sort((a, b) => {
    return parseFloat(b.equity) - parseFloat(a.equity);
  });

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border rounded-lg">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Equity</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedParticipants.map((p, index) => (
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
                          <th className="px-4 py-2 text-left">Score</th>
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
                            <td className="px-4 py-2">
                              {stringifyScore(assignment.score)}
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
  );
}

export default SweepstakeTable;
