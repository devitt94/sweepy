import React, { useState } from "react";

const SortableTable = ({ sortableColumns, data, columnFormatters }) => {
  // columns = { name: true, score: true, probability: false }
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  const sortedData = React.useMemo(() => {
    let sortableData = [...data];
    if (sortConfig.key !== null && sortableColumns[sortConfig.key]) {
      sortableData.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "asc" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableData;
  }, [data, sortConfig, sortableColumns]);

  const requestSort = (key) => {
    if (!sortableColumns[key]) return; // ignore clicks if column not sortable
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  const getSortArrow = (key) => {
    if (!sortableColumns[key]) return ""; // no arrow if not sortable
    if (sortConfig.key !== key) return "↕";
    return sortConfig.direction === "asc" ? "↑" : "↓";
  };

  return (
    <table className="min-w-full border border-gray-300">
      <thead className="bg-gray-100">
        <tr>
          {Object.keys(sortableColumns).map((colKey) => (
            <th
              key={colKey}
              className={`px-4 py-2 text-left ${
                sortableColumns[colKey] ? "cursor-pointer" : ""
              }`}
              onClick={() => requestSort(colKey)}
            >
              {colKey.charAt(0).toUpperCase() + colKey.slice(1)}{" "}
              {getSortArrow(colKey)}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row, idx) => (
          <tr key={idx} className="border-t">
            {Object.keys(sortableColumns).map((colKey) => (
              <td key={colKey} className="px-4 py-2">
                {columnFormatters[colKey]
                  ? columnFormatters[colKey](row[colKey])
                  : row[colKey]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default SortableTable;
