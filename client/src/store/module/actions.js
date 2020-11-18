import { T } from "./types";
import axios from "axios";

const apiURL = "http://49.247.197.181:80";

export const actions = {
  [T.TEST]({ commit }, testParams) {
    commit(T.TEST, testParams);

    let api = axios.create();

    let formData = new FormData();

    formData.append("device", "test");

    axios
      .all([api.post(`${apiURL}/connect`, formData)])
      .then(responses => {
        console.log(responses);
      })
      .catch(error => {
        console.dir(error);
      });
  },
  [T.INIT_PROGRAM]({ commit }, deviceId) {
    let api = axios.create();
    let formData = new FormData();

    formData.append("device", deviceId);

    axios
      .all([api.post(`${apiURL}/connect`, formData)])
      .then(responses => {
        if (responses[0].status == 200) {
          commit(T.SET_DEVICEID, deviceId);
        } else {
          alert("디바이스 ID 설정에 실패하였습니다.");
        }
      })
      .catch(error => {
        alert("디바이스 ID 설정에 실패하였습니다.");
      });
  },
  [T.GET_EVENT]({ commit }, params) {
    let api = axios.create();

    axios
      .all([api.get(`${apiURL}/users/${params.deviceId}/event`)])
      .then(responses => {
        if (responses[0].status == 200) {
          params.cSuc(responses[0].data);
        } else {
          console.log(responses[0]);
          console.log("ERR");
        }
      })
      .catch(error => {
        console.log("ERR");
        console.log(error);
      });
  }
};
