import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
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
    setEmotionAnalysis(state, emotionAnalysis) {
      state.emotionAnalysis = emotionAnalysis;
    }
  },
  actions: {

  },
  modules: {},
});