import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function SweepstakeHistoryChart({ sweepstakeHistory }) {
  const [chartData, setChartData] = useState([]);
  const [participantNames, setParticipantNames] = useState([]);

  const participants = sweepstakeHistory.participants;

  useEffect(() => {
    const allTimestamps = new Set();
    participants.forEach((p) =>
      p.history.forEach((h) => allTimestamps.add(h.timestamp)),
    );

    const sortedTimestamps = Array.from(allTimestamps).sort();

    const data = sortedTimestamps.map((timestamp) => {
      const entry = { timestamp: new Date(timestamp).getTime() }; // numeric timestamp
      participants.forEach((participant) => {
        const point = participant.history.find(
          (h) => h.timestamp === timestamp,
        );
        entry[participant.name] = point ? parseFloat(point.probability) : null;
      });
      return entry;
    });

    setChartData(data);
    setParticipantNames(participants.map((p) => p.name));
  }, [sweepstakeHistory]);

  const axisDateFormatter = (str) => {
    const date = new Date(str);
    return date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="mt-6">
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <XAxis
            dataKey="timestamp"
            type="number"
            domain={["auto", "auto"]}
            scale="time"
            tickFormatter={axisDateFormatter}
            interval="preserveStartEnd"
          />
          <YAxis
            domain={[0, 1]}
            tickFormatter={(v) => `${(v * 100).toFixed(1)}%`}
          />
          <Tooltip labelFormatter={(str) => new Date(str).toLocaleString()} />
          <Legend />
          {participantNames.map((name, index) => (
            <Line
              key={name}
              type="monotone"
              dataKey={name}
              stroke={COLORS[index % COLORS.length]}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

const COLORS = [
  "#8884d8",
  "#82ca9d",
  "#ff7300",
  "#ff0000",
  "#0088FE",
  "#00C49F",
];

export default SweepstakeHistoryChart;
