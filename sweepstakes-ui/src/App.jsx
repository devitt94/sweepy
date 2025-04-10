import React, { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    market_id: "",
    method: "tiered",
    name: "",
    participants: "",
  });

  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [expandedRow, setExpandedRow] = useState(null); // Track expanded row

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResponse(null);

    try {
      const payload = {
        ...formData,
        participant_names: formData.participants.split(",").map((p) => p.trim()),
      };

      const res = await axios.post("http://localhost:8000/sweepstakes", payload);

      // Sort participants by name in ascending order
      const sortedParticipants = res.data.participants.sort((a, b) =>
        a.name.localeCompare(b.name)
      );

      setResponse({
        ...res.data,
        participants: sortedParticipants, // Use sorted participants
      });
    } catch (err) {
      setError(err.message);
    }
  };

  const toggleRow = (index) => {
    setExpandedRow(expandedRow === index ? null : index);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-xl bg-white p-6 rounded-2xl shadow-xl">
        <h1 className="text-2xl font-bold mb-6">Create a Sweepstakes</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="market_id"
            placeholder="Market ID"
            value={formData.market_id}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
          <input
            type="text"
            name="name"
            placeholder="Sweepstake Name"
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
          <select
            name="method"
            value={formData.method}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="random">Random</option>
            <option value="tiered">Tiered</option>
            <option value="staggered">Staggered</option>
            <option value="fair">Fairest</option>
          </select>
          <textarea
            name="participants"
            placeholder="Participants (comma-separated)"
            value={formData.participants}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Submit
          </button>
        </form>

        {response?.participants && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">{response.name}</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full border rounded-lg">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 text-left">Name</th>
                    <th className="px-4 py-2 text-left">Equity</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {response.participants.map((p, index) => (
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
                                    <td className="px-4 py-2">{assignment.runner_name}</td>
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
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-100 rounded">
            ❌ Error: {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
