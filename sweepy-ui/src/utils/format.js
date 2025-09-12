export function stringifyScore(score) {
  if (score === null || score === undefined) {
    return "-";
  } else if (score === 0) {
    return "E";
  } else if (score > 0) {
    return `+${score}`;
  } else {
    return `${score}`;
  }
}

export function percentifyProbability(prob) {
  if (prob === null || prob === undefined) {
    return "-";
  } else {
    return `${(parseFloat(prob) * 100).toFixed(2)}%`;
  }
}
