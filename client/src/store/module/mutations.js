import { stat } from "fs";
import { T } from "./types";

export const mutations = {
  [T.TEST](state, string) {
    state.test = string;
  },
  [T.SET_DEVICEID](state, string) {
    state.deviceId = string;
  }
};
