import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    uuid:0,
    customerInfo: [],
    emotionAnalysis: null,
  },
  getters: {
    getCustomerInfo(state) {
      return state.customerInfo;
    },
    
    getEmotionAnalysis(state) {
      return state.emotionAnalysis;
    }
  },
  mutations: {
    setCustomerInfo(state, customerInfo) {
      state.customerInfo.push(customerInfo);
    },
    updateCustomerInfo(state, customerInfo) {
      state.customerInfo = customerInfo
    },
    setEmotionAnalysis(state, emotionAnalysis) {
      state.emotionAnalysis = emotionAnalysis;
    },
    deleteCustomerInfo(state, uuid) {
      for (var i = 0; i < state.customerInfo.length; i++){
        // console.log("삭제 인덱스 : " + i);
        // console.log("customeruuid : " + uuid);
        // console.log("stateuuid : " + state.customerInfo[i].uuid);
        if (uuid == state.customerInfo[i].uuid) {
          console.log("삭제 인덱스2 : " + i);
          state.customerInfo.splice(i, 1);
        }
      }
    }
  },
  actions: {

  },
  modules: {},
});