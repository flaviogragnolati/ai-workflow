import assert from "node:assert/strict";

export function cliJson(result, operation, expectedStatus) {
  if (result.error) {
    throw new Error(`${operation}: subprocess execution failed (${result.error.code || "unknown"}: ${result.error.message})`, {cause: result.error});
  }
  if (result.signal) throw new Error(`${operation}: subprocess terminated by ${result.signal}`);
  assert.equal(result.status, expectedStatus, `${operation}: unexpected exit status; ${result.stderr || "no stderr"}`);
  if (!result.stdout?.trim()) throw new Error(`${operation}: empty JSON response`);
  try {
    return JSON.parse(result.stdout);
  } catch (cause) {
    throw new Error(`${operation}: malformed JSON response`, {cause});
  }
}
