import { useEffect, useState } from "react";
import axios from "axios";

const defaultFormData = {
  market_id: "",
  market_name: "",
  method: "tiered",
  name: "",
  participants: ["", "", ""],
};

function CreateForm({ eventTypes, fetchMarkets, handleSubmitSuccess }) {
  const [formData, setFormData] = useState({ ...defaultFormData });
  const [selectedEventType, setSelectedEventType] = useState("");
  const [markets, setMarkets] = useState([]);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const getMarketCompetitionName = (marketId) => {
    const market = markets.find((m) => m.market_id === marketId);
    return market ? `${market.competition_name} - ${market.market_name}` : "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const payload = {
        ...formData,
        participant_names: formData.participants.filter((p) => p.trim() !== ""),
        competition: getMarketCompetitionName(formData.market_id),
      };

      const res = await axios.post(`/api/sweepstakes`, payload);

      // Sort participants by name in ascending order
      const sortedParticipants = res.data.participants.sort((a, b) =>
        a.name.localeCompare(b.name),
      );

      handleSubmitSuccess({
        ...res.data,
        participants: sortedParticipants, // Use sorted participants
      });

      setFormData({ ...defaultFormData }); // Reset form data
    } catch (err) {
      console.error("Error creating sweepstake:", err.stack);
      setError(err.message);
    }
  };

  useEffect(() => {
    if (!selectedEventType) {
      setMarkets([]);
      return;
    }
    fetchMarkets(selectedEventType)
      .then((data) => {
        setMarkets(data);
      })
      .catch((err) => {
        console.error("Error fetching markets:", err);
        setError("Failed to fetch markets for the selected event type.");
      });
  }, [selectedEventType]);

  const handleEventTypeChange = (e) => {
    const eventType = e.target.value;
    setSelectedEventType(eventType);
    setFormData((prev) => ({ ...prev, market_id: "" }));
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Create a Sweepstakes</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* # event type selection dropdown */}
        <label className="block font-medium mb-1">Event Type</label>
        <select
          name="event_type"
          value={formData.event_type}
          onChange={handleEventTypeChange}
          className="w-full p-2 border rounded"
          required
        >
          <option value="" selected>
            Select Event Type
          </option>
          {eventTypes.map((eventType) => (
            <option key={eventType.id} value={eventType.id}>
              {eventType.name}
            </option>
          ))}
        </select>
        {/* Market selection dropdown */}
        <label className="block font-medium mb-1">Market</label>
        <select
          name="market_id"
          value={formData.market_id}
          onChange={handleChange}
          className="w-full p-2 border rounded"
          required
        >
          <option key="empty" value="" selected>
            Select Market
          </option>
          {markets.map((market) => (
            <option key={market.market_id} value={market.market_id}>
              {market.competition_name} - {market.market_name}
            </option>
          ))}
        </select>
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
        {/* Participants List */}
        <div>
          <label className="block font-medium mb-1">Participants</label>
          {formData.participants.map((participant, index) => (
            <div key={index} className="flex items-center space-x-2 mb-2">
              <input
                type="text"
                value={participant}
                onChange={(e) => {
                  const newParticipants = [...formData.participants];
                  newParticipants[index] = e.target.value;
                  setFormData((prev) => ({
                    ...prev,
                    participants: newParticipants,
                  }));
                }}
                className="flex-1 p-2 border rounded"
                placeholder={`Participant ${index + 1}`}
                required
              />
              <button
                type="button"
                onClick={() => {
                  const updated = [...formData.participants];
                  updated.splice(index, 1);
                  setFormData((prev) => ({ ...prev, participants: updated }));
                }}
                className="text-red-500 hover:text-red-700"
                title="Remove"
              >
                ✕
              </button>
            </div>
          ))}
          <button
            type="button"
            onClick={() =>
              setFormData((prev) => ({
                ...prev,
                participants: [...prev.participants, ""],
              }))
            }
            className="mt-2 px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
          >
            + Add Participant
          </button>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Submit
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-100 rounded">❌ Error: {error}</div>
      )}
    </div>
  );
}

export default CreateForm;
