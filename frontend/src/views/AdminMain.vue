<template>
  <v-container>
    <div class="mx-auto" max-width="1920" style="margin-top:50px;">
      <h2 class="adminTitle col-11 centerContent">
        현재 방문 고객 현황
        <span>현재 고객 수 : {{ getCustomerInfo.length }}</span>
      </h2>
      <v-slide-group class="my-slider" center-active dark>
        <v-slide-item v-for="customer in getCustomerInfo" :key="customer" v-slot="{ active, toggle }">
          <v-card :color="active ? '#192537' : '#192537'" class="ma-4" height="600" width="380" @click="toggle">
            <div class="fill-height imgBox">
              <div class="firstBox">
                <div class="col-6 customInfoBox">
                  <p class="imgArea">이미지영역</p>
                </div>
                <div class="col-6 customInfoBox">
                  <p>이름 : {{ customer.name }}</p>
                  <p>나이 : {{ customer.age }}세</p>
                </div>
              </div>

              <div class="secondBox">
                <p>관심상품 : {{ customer.interest }}</p>
                <p>
                  요구사항
                  <br />
                  {{ customer.requirements }}
                </p>

                <v-dialog v-model="satisfyDialog" width="500">
                  <template v-slot:activator="{ on, attrs }">
                    <button class="satisfiedBtn" v-bind="attrs" v-on="on" @click="goCamSatisfied(customer.uuid)">
                      => 만족도 확인
                    </button>
                  </template>

                  <v-card>
                    <chart :id="'recentSatisfy'" :labels="labels" :data="data"></chart>
                    <v-divider></v-divider>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="satisfyDialog = false">
                        닫기
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </div>
              <div class="thirdBox">
                <p>입장시간 : sadfdf</p>
                <p>퇴장시간 : 퇴장전</p>
              </div>
            </div>
          </v-card>
        </v-slide-item>
      </v-slide-group>
    </div>
  </v-container>
</template>
<script>
import { mapGetters } from 'vuex';
import Chart from '../components/Chart.vue';
import http from '../api/axios';
export default {
  components: {
    chart: Chart,
  },
  data() {
    return {
      customers: [],
      emotion: [],
      satisfyDialog: false,
      labels: ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise'],
      data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    };
  },
  computed: {
    ...mapGetters(['getCustomerInfo']),
  },
  methods: {
    goCamSatisfied(uuid) {
      console.log('uuid : ' + uuid);
      http
        .get(`/member/emotion/${uuid}`)
        .then((response) => {
          this.emotion = response.data;
          this.data[0] = this.emotion[this.emotion.length - 1].anger;
          this.data[1] = this.emotion[this.emotion.length - 1].contempt;
          this.data[2] = this.emotion[this.emotion.length - 1].disgust;
          this.data[3] = this.emotion[this.emotion.length - 1].fear;
          this.data[4] = this.emotion[this.emotion.length - 1].happiness;
          this.data[5] = this.emotion[this.emotion.length - 1].neutral;
          this.data[6] = this.emotion[this.emotion.length - 1].sadness;
          this.data[7] = this.emotion[this.emotion.length - 1].surprise;
          //   alert('구왁');
        })
        .catch(() => {
          alert('안데스산맥');
        });
    },
  },
};
</script>
<style scoped>
@import '../assets/css/adminMain.css';
.v-application p {
  margin: 0;
}
.secondBox p {
  margin-bottom: 16px;
}
</style>
