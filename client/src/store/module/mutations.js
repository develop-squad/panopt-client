import { stat } from "fs";
import { T } from "./types";

export const mutations = {
  [T.TEST](state, string) {
    state.test = string;
  },
  [T.SET_DEVICEID](state, string) {
    state.deviceId = string;
  },

  [T.UPDATE_PROCESS](state, process) {
    // console.log("M - UPDATE_PROCESS");
    let thisProcess = state.processList.find(
      el => el.processId == process.processId
    );

    process.createdAt = thisProcess.createdAt;
    thisProcess = process;
  },
  [T.CREATE_PROCESS](state, process) {
    // console.log("M - CREATE_PROCESS");
    state.processList.push(process);
  },
  [T.DELETE_PROCESS](state, processId) {
    // console.log("M - DELETE_PROCESS");
    state.processList = state.processList.filter(
      el => el.processId !== processId
    );
  }
};
