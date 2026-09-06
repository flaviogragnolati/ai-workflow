import assert from "node:assert/strict";
import {cliJson} from "./cli-result.mjs";

const rejection = {status: 1, signal: null, stdout: '{"outcome":"blocked"}', stderr: ""};
for (const status of [0, 1]) {
  for (const stdout of ["", rejection.stdout]) {
    const error = Object.assign(new Error("spawnSync denied"), {code: "EPERM"});
    assert.throws(() => cliJson({...rejection, status, stdout, error}, "private URL", 1), /private URL: subprocess execution failed \(EPERM/);
  }
}
assert.throws(() => cliJson({...rejection, signal: "SIGTERM"}, "private URL", 1), /private URL: subprocess terminated by SIGTERM/);
assert.throws(() => cliJson({...rejection, status: null}, "private URL", 1), /unexpected exit status/);
assert.throws(() => cliJson({...rejection, status: 0}, "private URL", 1), /unexpected exit status/);
for (const stdout of ["", " \n"]) {
  assert.throws(() => cliJson({...rejection, stdout}, "private URL", 1), /private URL: empty JSON response/);
}
assert.throws(() => cliJson({...rejection, stdout: "{"}, "private URL", 1), /private URL: malformed JSON response/);
assert.deepEqual(cliJson(rejection, "private URL", 1), {outcome: "blocked"});
console.log("q-tool-web-markdown subprocess diagnostics tests passed");
