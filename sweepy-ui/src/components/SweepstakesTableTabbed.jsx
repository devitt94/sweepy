import React, { useState } from "react";

import ParticipantTable from "./ParticipantTable";
import LeaderboardTable from "./LeaderboardTable";

const SweepstakeTableTabbed = ({ data }) => {
  const [activeTab, setActiveTab] = useState("table");

  const renderContent = () => {
    switch (activeTab) {
      case "participant":
        return <ParticipantTable data={data} />;
      case "leaderboard":
        return <LeaderboardTable data={data} />;
      default:
        return null;
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      {/* Tab Buttons */}
      <div className="flex border-b">
        <button
          onClick={() => setActiveTab("participant")}
          className={`px-4 py-2 ${
            activeTab === "participant"
              ? "border-b-2 border-blue-500 font-semibold"
              : ""
          }`}
        >
          Participants
        </button>
        <button
          onClick={() => setActiveTab("leaderboard")}
          className={`px-4 py-2 ${
            activeTab === "leaderboard"
              ? "border-b-2 border-blue-500 font-semibold"
              : ""
          }`}
        >
          Leaderboard
        </button>
      </div>

      {/* Tab Content */}
      <div className="mt-4">{renderContent()}</div>
    </div>
  );
};

export default SweepstakeTableTabbed;
