import { percentifyProbability, stringifyScore } from "../utils/format";
import SortableTable from "./SortableTable";

function LeaderboardTable({ data }) {
  const allAssignments = data.participants
    .flatMap((p) =>
      p.assignments.map((a) => ({
        probability: a.implied_probability,
        player: a.name,
        score: a.score,
        participant: p.name,
      })),
    )
    .sort((a, b) => a.score - b.score);

  const columns = {
    participant: true,
    player: true,
    probability: true,
    score: data.tournament_id ? true : false,
  };

  const columnFormatters = {
    probability: (val) => percentifyProbability(val),
    score: (val) => stringifyScore(val),
  };

  return (
    <SortableTable
      sortableColumns={columns}
      data={allAssignments}
      columnFormatters={columnFormatters}
    />
  );
}

export default LeaderboardTable;
